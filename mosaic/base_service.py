# encoding: utf-8
#
# The BaseService class yields a full working base microservice, which is able to communicate over mosaic messages
# with other services. To test it out just create a service which inherits from this BaseService class. Simply use the
# dispatch and listen (listen_to) functions to communicate with other services. The communication follows a
# predefined pipeline structure. That means every service which is listed in a pipeline will get and send a message in
# the defined direction.
#
# devs@droxit.de
#
# Copyright (c) 2017 droxIT GmbH
#


import socket
from mosaic.communication import mosaic_message
from mosaic.service_loader import load_class
from mosaic import exceptions
from mosaic.config import configuration_loader


class BaseService:
    def __init__(self, params):

        if params is None:
            raise exceptions.ParameterMissing('BaseService.__init__() - params is None.')
        # load config f
        elif 'service_key' in params:
            # service name as param
            # load the config from services.json

            config_file = None
            if 'config_file' in params:
                config_file = params['config_file']

            cfg = configuration_loader.MosaicConfig(config_file)
            self.params = cfg.get_item(params['service_key'])
        else:
            # there isn't a configuration file
            # the config will be loaded by the passed params directly
            self.params = params

        # if self.params is None:
        #     #logger need the service name
        #     self.params['name'] = 'not defined'
        #     self.logger.critical('BaseService.__init__() - params is None.')
        #     raise exceptions.ParameterMissing('BaseService.__init__() - params is None.')
        # elif 'name' not in self.params:
        #     # service name as param
        #     # load the config from services.json
        #     self.params['name'] = 'not defined'
        #     self.logger.critical('BaseService.__init__() - name is undefined')

        # buffer size to read a msg in specified byte chunks
        self.BUFFER_SIZE = 4096

        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1

        # initialize logger
        logger_params = {
            'filename': 'pipeline.log',
            'level': 'INFO'
        }
        if 'logging' in self.params:
            logger_params = self.params['logging']

        logger_class = 'mosaic.log.basic_logger.BasicLogger'
        if 'logger_class' in logger_params:
            logger_class = logger_params['logger_class']
        LoggingClass = load_class(logger_class)

        if 'name' not in self.params:
            # service name as param
            # load the config from services.json
            self.params['name'] = 'not defined'
            self.logger = LoggingClass(self.params['name'], **logger_params)
            self.logger.critical('BaseService.__init__() - name is undefined')
            raise exceptions.ParameterMissing('BaseService.__init__() - service name is missing.')

        self.logger = LoggingClass(self.params['name'], **logger_params)

        if self.params is None:
            # logger need the service name
            self.params['name'] = 'not defined'
            self.logger.critical('BaseService.__init__() - params is None.')
            raise exceptions.ParameterMissing('BaseService.__init__() - params is None.')

        required_params = [
            'ip',
            'port',
            'name'
        ]
        for param in required_params:
            if param not in self.params:
                self.logger.critical('BaseService.__init__() - "' + param + '" is required in params.')
                raise exceptions.ParameterMissing('BaseService.__init__() - "' + param + '" is required in params.')

        # initialize monitoring
        monitoring_params = {
            'filename': 'monitoring.log'
        }
        if 'monitoring' in self.params:
            monitoring_params = self.params['monitoring']

        monitor_class = 'mosaic.monitor.basic_monitoring.BasicMonitoring'
        if 'monitor_class' in monitoring_params:
            monitor_class = monitoring_params['monitor_class']
        MonitoringClass = load_class(monitor_class)
        self.monitoring = MonitoringClass(**monitoring_params)

        self.logger.info({'msg': 'started', 'effective_params': self.params})
        self.mosaic_message = mosaic_message.Message()

    # need to be overwritten by inhertied classes.
    def on_message(self, msg):
        pass

    # need to be overwritten by inherited classes. This funciton gets the whole message object as a MosaicMessage.
    # If you just need the payload's message, please user on_message instead.
    def on_message_ext(self, extended_msg):
        pass

    # send a mosaic protobuf message to the next service in the pipeline.
    def dispatch(self, msg):
        self.mosaic_message.set_payload(msg)

        if self.mosaic_message.has_empty_pipeline():
            return

        next_service = self.mosaic_message.pop_service()
        message_id = self.mosaic_message.id

        address_tuple = (next_service.ip, next_service.port)

        wiremsg = self.mosaic_message.serialize()

        try:
            connection = socket.create_connection(address_tuple)
            connection.sendall(wiremsg)
            self.monitoring.msg_dispatched(
                service_name=self.params['name'],
                message_id=message_id,
                destination=next_service.encodeId()
            )
            connection.close()
        except OSError as e:
            self.logger.critical(e.strerror + ' - ' + str(e.__traceback__))
            raise e

    # receive mosaic protobuf messages sent to a socket running on the specified ip and port. To handle the received
    # message please implement the on_message funtion in your inherited service.
    def listen_to(self, ip, port):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # s.setblocking(0)
            s.bind((ip, port))
            s.listen()
        except OSError as e:
            self.logger.critical(e.strerror + ' - ' + str(e.__traceback__))
            raise e

        try:
            while 1:
                connection, sender_address = s.accept()
                self.logger.debug('Accepted connection from: ' + sender_address[0] + ':' + str(sender_address[1]))
                data = connection.recv(self.BUFFER_SIZE)
                packet_len = mosaic_message.get_packet_len(data)

                while len(data) < packet_len:
                    data += connection.recv(self.BUFFER_SIZE)

                try:
                    self.mosaic_message = mosaic_message.Message.deserialize(data)
                except Exception as e:
                    errmsg = 'unable to deserialize mosaic message {}'.format(e)
                    self.logger.error(e)
                    self.monitoring.msg_error(
                        service_name=self.params['name'],
                        message_id='unknown',
                        description=errmsg
                    )
                    continue

                self.monitoring.msg_received(
                    service_name=self.params['name'],
                    message_id=self.mosaic_message.id
                )

                if self.mosaic_message.has_empty_pipeline():
                    self.monitoring.msg_reached_final_destination(
                        service_name=self.params['name'],
                        message_id=self.mosaic_message.id
                    )

                self.logger.debug('MosaicMessage received: ' + self.mosaic_message.__str__())

                self.on_message(self.mosaic_message.payload)
                self.on_message_ext(self.mosaic_message)

                if not data:
                    break
        except OSError as e:
            self.logger.critical(e.strerror + ' - ' + str(e.__traceback__))
            raise e

    # this function is usually called by services, to receive a message out of the pipeline object posted as part of
    # the mosaic protobuf message.
    def listen(self):
        self.listen_to(self.params['ip'], self.params['port'])

    # get current service id
    def get_service_id(self):
        return self.params['ip'] + ':' + str(self.params['port'])
