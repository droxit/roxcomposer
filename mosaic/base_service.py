#!/usr/bin/env python3.5

from mosaic.communication import service_com_pb2


class BaseService:
    def __init__(self):
        self.mosaic_message = service_com_pb2.MosaicMessage()
        pipeline = service_com_pb2.Pipeline()

        service = pipeline.services.add()
        service.id = 'baseService-111elf'
        parameter = service.parameters.add()
        parameter.serviceParams = 'troll=lol'

        payload = service_com_pb2.Payload()
        payload.firstNumber = 2
        payload.secondNumber = 2

        self.mosaic_message.pipeline.CopyFrom(pipeline)
        self.mosaic_message.payload.CopyFrom(payload)

    def get_mosaic_message(self):
        return self.mosaic_message
