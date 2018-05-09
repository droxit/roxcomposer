import sys
import json
import time
from roxcomposer import base_service


class DelayService(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 4007,
                "name": "delay_service",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "DEBUG"
                }
            }
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg, msg_id):
        self.msg = msg
        time.sleep(1)
        return self.dispatch(msg)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    service = DelayService(params)
