#!/usr/bin/env python3.6

from mosaic import base_service


class HtmlGenerator(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                'ip': '127.0.0.1',
                'port': 5001
            }
        super().__init__(params)
        self.recv_pipeline_msg()

    def on_message(self, msg):
        self.mosaic_message = msg
        print(self.mosaic_message.get_protobuf_msg_as_dict())
        self.to_html()

    def to_html(self):
        received_text = self.mosaic_message.get_content_as_dict()['body']
        html_string = """
            <!doctype html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>droxIT - mosaic</title>
                        <style>
                            body {margin: 3em;}
                            header {background: #eee; padding: 1em;}
                            article {padding: 2em;}
                        </style>
                    <body>
                        <header><h1>MOSAIC - DEMO</h1></header>
                        <article>
                            """ + received_text + """
                        </article>
                    </body>
                </html>
        """

        self.mosaic_message.set_content(html_string)
        return self.send()

if __name__ == '__main__':
    service = HtmlGenerator()
