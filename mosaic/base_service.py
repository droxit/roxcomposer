#!/usr/bin/env python3.6

from mosaic.communication import mosaic_message
from mosaic.monitor import basic_monitoring
from mosaic.service_loader import load_class
import socket
import sys
from mosaic import exceptions
from mosaic.config import configuration_loader


# The BaseService class yields a full working base microservice, which is able to communicate over mosaic messages
# with other services. To test it out just create a service which inherits from this BaseService class. Simply use the
# dispatch and listen (listen_to) functions to communicate with other services. The communication follows a
# predefined pipeline structure. That means every service whih is listed in a pipeline will get and send a message in
# the defined direction.
class BaseService:
    def __init__(self, params):

        if params is None:
            raise exceptions.ParameterMissing('BaseService.__init__() - params is None.')
        #load config f
        elif 'service_key' in params:
            # service name as param
            # load the config from services.json
            cfg = configuration_loader.MosaicConfig()
            self.params = cfg.get_item(params['service_key'])
        else:
            # there isn't a configuration file
            # the config will be loaded by the passed params directly
            self.params = params

        if self.params is None:
            raise exceptions.ParameterMissing('BaseService.__init__() - params is None.')

        # buffer size to read a msg in specified byte chunks
        self.BUFFER_SIZE = 1024

        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1

        required_params = [
            'ip',
            'port',
            'name'
        ]
        for param in required_params:
            if param not in self.params:
                raise exceptions.ParameterMissing('BaseService.__init__() - "' + param + '" is required in params.')

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
        self.logger = LoggingClass(self.params['name'], **logger_params)

        # initialize monitoring
        monitoring_params = {
            'filename': 'monitoring.log'
        }
        if 'monitoring' in self.params:
            monitoring_params = self.params['monitoring']
        self.monitoring = basic_monitoring.BasicMonitoring(**monitoring_params)

        self.mosaic_message = mosaic_message.Message()

    # need to be overwritten by inhertied classes.
    def on_message(self, msg):
        pass

    # send a mosaic protobuf message to the next service in the pipeline.
    def dispatch(self, msg):
        self.mosaic_message.set_content(msg)

        if 'services' not in self.mosaic_message.get_services_as_dict():
            return
        elif len(self.mosaic_message.get_services_as_dict()['services']) <= 1:
            return

        me = self.mosaic_message.pop_service()
        message_id = self.mosaic_message.get_message_id()

        next_service = self.mosaic_message.get_services_as_dict()['services'][0]
        next_service_id = next_service['id'].split(':')
        address_tuple = (next_service_id[0], next_service_id[1])

        self.mosaic_message = mosaic_message.Utils.serialize(self.mosaic_message.get_protobuf_msg())

        try:
            connection = socket.create_connection(address_tuple)
            connection.send(self.mosaic_message)
            self.monitoring.msg_dispatched(
                service_id=self.get_service_id(),
                message_id=message_id
            )

            resp = connection.recv(self.BUFFER_SIZE)
            self.logger.debug(resp)
            connection.close()
        except OSError as e:
            self.logger.error(e)
            return False

        return resp

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
            self.logger.critical(e)
            sys.exit(1)

        try:
            while 1:
                connection, sender_address = s.accept()
                self.logger.debug('Accepted connection from: ' + sender_address[0] + ':' + str(sender_address[1]))
                data = connection.recv(self.BUFFER_SIZE)

                msg_received = mosaic_message.Utils.deserialize(data)
                try:
                    self.mosaic_message = mosaic_message.Message(msg_received)

                    self.monitoring.msg_received(
                        service_id=self.get_service_id(),
                        message_id=self.mosaic_message.get_message_id()
                    )

                    if self.mosaic_message.is_empty_pipeline():
                        self.monitoring.msg_reached_final_destination(
                            service_id=self.get_service_id(),
                            message_id=self.mosaic_message.get_message_id()
                        )

                    self.logger.debug('MosaicMessage received: ' + self.mosaic_message.__str__())
                except exceptions.InvalidMosaicMessage as e:
                    self.logger.error(e)
                    continue

                self.on_message(self.mosaic_message.get_content_as_dict()['body'])
                connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
                connection.close()

                if not data:
                    break
        except OSError as e:
            self.logger.error(e)

    # this function is usually called by services, to receive a message out of the pipeline object posted as part of
    # the mosaic protobuf message.
    def listen(self):
        self.listen_to(self.params['ip'], self.params['port'])

    # set the content of the message currently handled by the service. @data should be a (json) string.
    def set_content(self, data):
        return mosaic_message.Message.set_content(self.mosaic_message, data)

    # get the content of the message currently handled by the service in protobuf format. To get a more usable message
    # use the get_contant_as_dict function.
    def get_content(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)['body']

    # get the content of the message curerntly handled by the service as a dicitionary. Remember that the dict only
    # yields a representation of the actual message. So if you actually want to manipulate values in the message you
    # have to set the changed values manually in the protobuf message.
    def get_content_as_dict(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)

    # get the currently handled message as a protobuf object
    def get_protobuf_message(self):
        return mosaic_message.Message.get_protobuf_msg(self.mosaic_message)

    # get the currently handled message as a python dictionary
    def get_protobuf_message_as_dict(self):
        return mosaic_message.Message.get_protobuf_msg_as_dict(self.mosaic_message)

    # get current service id
    def get_service_id(self):
        return self.params['ip'] + ':' + str(self.params['port'])
