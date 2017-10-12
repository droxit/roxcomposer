#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Creation:    16.08.2013
# Last Update: 15.01.2017
#
# Copyright (c) 2013-2017 by Georg Kainzbauer <http://www.gtkdb.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#


#
# import required modules
#
from email.mime.text import MIMEText
import smtplib
import sys
import json
from mosaic import base_service


class SentMail(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 7001,
                "name": "sent_mail",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "INFO"
                },
                # declaration of the default mail settings
                #
                # mail address of the sender
                # fully qualified domain name of the mail server
                # username for the SMTP authentication
                # password for the SMTP authentication
                # use TLS encryption for the connection
                "smtp": {
                    "sender": "villarroya@droxit.de",
                    "smtpserver": "smtp.office365.com",
                    "smtpusername": "villarroya@droxit.de",
                    "smtppassword": "XXXXXXXXX",
                    "usetls": True
                },
                "mail": {
                    "subject": "Mosaic-Demo: Test",
                    "recipient": "info@droxit.de"
                }
            }

        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.sendmail(self.params['mail']['recipient'], self.params['mail']['subject'], msg)

    #
    # function to send a mail
    #
    #    def sendmail(recipient, subject, content):
    def sendmail(self, recipient, subject, content):

        # generate a RFC 2822 message
        msg = MIMEText(content)
        msg['From'] = self.params['smtp']['sender']
        msg['To'] = recipient
        msg['Subject'] = subject

        # open SMTP connection
        server = smtplib.SMTP(self.params['smtp']['smtpserver'])

        # start TLS encryption
        if self.params['smtp']['usetls']:
            server.starttls()

        # login with specified account
        if self.params['smtp']['smtpusername'] and self.params['smtp']['smtppassword']:
            server.login(self.params['smtp']['smtpusername'], self.params['smtp']['smtppassword'])

        self.logger.info('msg sented: ' + content + 'from: ' + self.params['smtp']['sender'] + ' to:' + recipient)

        # send generated message
        server.sendmail(self.params['smtp']['sender'], recipient, msg.as_string())

        # close SMTP connection
        server.quit()


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    #no parameters use default params
    #service = SentMail(params)

    #use service_key
    serv_params = {'service_key':'sent_mail.params'}
    service = SentMail(serv_params)
