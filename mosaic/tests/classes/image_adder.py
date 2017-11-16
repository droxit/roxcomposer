import sys
import json
from mosaic import base_service


class ImageAdder(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 6001,
                "name": "image_adder",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "DEBUG"
                }
            }
        super().__init__(params)

        self.image = None
        if 'image' in params:
            self.image = params['image']
        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.to_html()

    def to_html(self):
        received_text = self.msg
        html_string = ''
        if self.image is not None:
            html_string = "\n<img src=\"" + self.image + "\">"

        return self.dispatch(received_text + '<br/>' + html_string)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    # service = ImageAdder(params)
    # use service_key
    serv_params = {'service_key': 'image_adder.params'}
    service = ImageAdder(serv_params)
