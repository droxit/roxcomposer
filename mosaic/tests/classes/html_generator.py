#!/usr/bin/env python3.6

from mosaic import base_service


class HtmlGenerator(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 5001,
                "name": "html_generator",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "INFO"
                }
            }
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.to_html()

    def to_html(self):
        received_text = self.msg
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

        self.logger.info('Msg sent: ' + html_string)
        return self.dispatch(html_string)


if __name__ == '__main__':
    service = HtmlGenerator()
