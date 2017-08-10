#!/usr/bin/env python3.6

from mosaic.communication import mosaic_message
import socket

if __name__ == '__main__':
    mosaic_msg = mosaic_message.Message()
    mosaic_msg.add_service('127.0.0.1', 5001)
    mosaic_msg.add_service('127.0.0.1', 4001)

    address_tuple = ('127.0.0.1', 5001)
    print(mosaic_msg.get_protobuf_msg_as_dict())
    mosaic_msg = mosaic_message.Utils.serialize(mosaic_msg.get_protobuf_msg())

    connection = socket.create_connection(address_tuple)
    connection.send(mosaic_msg)

    # resp = connection.recv(1024)
    connection.close()
