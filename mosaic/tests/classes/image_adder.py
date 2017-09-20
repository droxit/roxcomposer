#!/usr/bin/env python3.6

from mosaic import base_service


class ImageAdder(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.to_html()

    def to_html(self):
        received_text = self.msg
        html_string = """
            <img src="../images/minions-yeah.jpg"></img>
        """

        self.logger.info('Msg sent: ' + received_text + '<br/>' + html_string)
        return self.dispatch(received_text + '<br/>' + html_string)


if __name__ == '__main__':
    service = ImageAdder()
