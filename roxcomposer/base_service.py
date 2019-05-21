# encoding: utf-8
#
# The BaseService class yields a full working base microservice, which is able to communicate over roxcomposer messages
# with other services. To test it out just create a service which inherits from this BaseService class. Simply use the
# dispatch and listen (listen_to) functions to communicate with other services. The communication follows a
# predefined pipeline structure. That means every service which is listed in a pipeline will get and send a message in
# the defined direction.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#


import socket
import threading
import time
import traceback

from roxcomposer import exceptions
from roxcomposer.communication import roxcomposer_message
from roxcomposer.config import configuration_loader
from roxcomposer.service_loader import load_class


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

            cfg = configuration_loader.ROXcomposerConfig(config_file)
            self.params = cfg.get_item(params['service_key'])
        else:
            # there isn't a configuration file
            # the config will be loaded by the passed params directly
            self.params = params

        # buffer size to read a msg in specified byte chunks
        self.BUFFER_SIZE = 4096

        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1

        self.msg_reception_time = 0

        # initialize logger
        logger_params = {
            'level': 'INFO'
        }
        if 'logging' in self.params:
            logger_params = self.params['logging']

        logger_class = 'roxcomposer.log.basic_logger.BasicLogger'
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

        # Read service parameters

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

        # Validate service parameters

        if not isinstance(self.params['ip'], str):
            self.logger.critical('BaseService.__init__() - "ip" in params is not a string.')
            raise exceptions.ConfigError('BaseService.__init__() - "ip" in params is not a string.')
        if not isinstance(self.params['port'], int):
            self.logger.critical('BaseService.__init__() - "port" in params is not an int.')
            raise exceptions.ConfigError('BaseService.__init__() - "port" in params is not an int.')

        try:
            socket.inet_aton(self.params['ip'])
        except socket.error:
            self.logger.critical('BaseService.__init__() - "ip" in params is not a valid IP address.')
            raise exceptions.ConfigError('BaseService.__init__() - "ip" in params is not a valid IP address.')

        # initialize monitoring
        monitoring_params = {
            'filename': 'monitoring.log'
        }
        if 'monitoring' in self.params:
            monitoring_params = self.params['monitoring']

        monitor_class = 'roxcomposer.monitor.basic_monitoring.BasicMonitoring'
        if 'monitor_class' in monitoring_params:
            monitor_class = monitoring_params['monitor_class']
        MonitoringClass = load_class(monitor_class)
        self.monitoring = MonitoringClass(**monitoring_params)

        self.logger.info('started', **self.params)
        self.roxcomposer_message = roxcomposer_message.Message()

    # need to be overwritten by inhertied classes.
    def on_message(self, msg, msg_id, parameters=None):
        pass

    # need to be overwritten by inherited classes. This funciton gets the whole message object as a ROXcomposerMessage.
    # If you just need the payload's message, please user on_message instead.
    def on_message_ext(self, extended_msg):
        pass

    # send a roxcomposer protobuf message to the next service in the pipeline.
    def dispatch(self, msg):
        processing_time = time.time() * 1000 - self.msg_reception_time
        if self.roxcomposer_message.has_empty_pipeline():
            self.monitoring.msg_reached_final_destination(
                service_name=self.params['name'],
                message_id=self.roxcomposer_message.id,
                processing_time=processing_time,
                total_processing_time=int(time.time() * 1000) - self.roxcomposer_message.created
            )
            return

        self.roxcomposer_message.set_payload(msg)

        # check next destination
        next_service = self.roxcomposer_message.peek_service()
        message_id = self.roxcomposer_message.id

        address_tuple = (next_service.ip, next_service.port)

        wiremsg = self.roxcomposer_message.serialize()

        try:
            connection = socket.create_connection(address_tuple)
            connection.sendall(wiremsg)
            self.monitoring.msg_dispatched(
                service_name=self.params['name'],
                message_id=message_id,
                destination=next_service.encodeId(),
                processing_time=processing_time
            )
            connection.close()
            return True
        except OSError as err:
            self.monitoring.msg_error(
                service_name=self.params['name'],
                message_id=message_id,
                destination=next_service.encodeId(),
                processing_time=processing_time,
                description='unable to dispatch message'
            )
            self.logger.error(str(err) + "\n" + traceback.format_exc())
            return False

    # receive roxcomposer protobuf messages sent to a
    # socket running on the specified ip and port. To
    # handle the received message please implement the
    # on_message function in your inherited service.
    def listen_to(self, ip, port):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # s.setblocking(0)
            s.bind((ip, port))
            s.listen()
        except OSError as err:
            self.logger.critical(str(err) + "\n" + traceback.format_exc())
            raise err

        try:
            while 1:
                connection, sender_address = s.accept()
                self.logger.debug('Accepted connection from: ' + sender_address[0] + ':' + str(sender_address[1]))
                data = connection.recv(self.BUFFER_SIZE)
                packet_len = roxcomposer_message.get_packet_len(data)

                while len(data) < packet_len:
                    chunk = connection.recv(self.BUFFER_SIZE)
                    if chunk != b'':
                        data += chunk
                    else:  # socket on the other end broke down
                        self.logger.warn('the sending socket from {} seems to have broken down'.format(sender_address))
                        connection.close()
                        break

                # if the connection was closed before - see above - this throws an exception, so we catch it
                try:
                    connection.close()
                except:
                    pass

                try:
                    self.roxcomposer_message = roxcomposer_message.Message.deserialize(data)
                except Exception as err:
                    errmsg = 'unable to deserialize roxcomposer message {}'.format(err)
                    self.logger.error(err)
                    self.monitoring.msg_error(
                        service_name=self.params['name'],
                        message_id='unknown',
                        description=errmsg
                    )
                    continue

                self.monitoring.msg_received(
                    service_name=self.params['name'],
                    message_id=self.roxcomposer_message.id
                )

                try:
                    me = self.roxcomposer_message.pop_service()
                except IndexError:
                    self.logger.warn('Received message with empty pipeline - any additional parameters meant for this service are lost')
                    me = roxcomposer_message.Service(ip, port)

                self.logger.debug('ROXcomposerMessage received: ' + self.roxcomposer_message.__str__())

                self.msg_reception_time = time.time() * 1000
                self.logger.debug('Received parameters: ' + str(me.parameters))
                self.on_message(self.roxcomposer_message.payload, self.roxcomposer_message.id, me.parameters)
                self.on_message_ext(self.roxcomposer_message)

                if not data:
                    break
        except Exception as err:
            self.logger.critical(str(err) + "\n" + traceback.format_exc())
            raise err

    # this function is usually called by services, to receive a message out of the pipeline object posted as part of
    # the roxcomposer protobuf message.
    def listen(self):
        self.listen_to(self.params['ip'], self.params['port'])

    def listen_thread(self):
        t = threading.Thread(target=self.listen)
        t.start()

    # get current service id
    def get_service_id(self):
        return self.params['ip'] + ':' + str(self.params['port'])
