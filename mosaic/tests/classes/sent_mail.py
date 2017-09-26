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
                }
            }
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
            self.msg = msg
            # self.logger.info('######msg received: ' + msg)
            self.sendmail('marta@villarroya.info','Mosaic-Demo: Test', msg)

    #
    # function to send a mail
    #
    #    def sendmail(recipient, subject, content):
    def sendmail(self, recipient, subject, content):

        #
        # declaration of the default mail settings
        #

        # mail address of the sender
        sender = 'villarroya@droxit.de'

        # fully qualified domain name of the mail server
        smtpserver = 'smtp.office365.com'

        # username for the SMTP authentication
        smtpusername = 'villarroya@droxit.de'

        # password for the SMTP authentication
        smtppassword = 'XXXXXX'

        # use TLS encryption for the connection
        usetls = True


        # generate a RFC 2822 message
        msg = MIMEText(content)
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # open SMTP connection
        server = smtplib.SMTP(smtpserver)

        # start TLS encryption
        if usetls:
            server.starttls()

        # login with specified account
        if smtpusername and smtppassword:
            server.login(smtpusername, smtppassword)

        self.logger.info('###################### sent Mail: ' + content + 'from: ' + sender + ' to:' + recipient)

        # send generated message
        server.sendmail(sender, recipient, msg.as_string())

        # close SMTP connection
        server.quit()




if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    service = SentMail(params)

