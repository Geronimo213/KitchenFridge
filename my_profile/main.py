#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about_me.html')
        self.response.out.write(template.render())

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('favorites.html')
        self.response.out.write(template.render())
class MailHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.out.write(template.render())
    def post(self):
        fromaddrs = 'lopez.geronimo213@gmail.com'
        toaddrs = self.request.get('email')
        msg = self.request.get('user_name') + ": " + self.request.get('user_message')
        subject = "Contact Form"

        headers = "\r\n".join(["from: " + fromaddrs,
                       "subject: " + subject,
                       "to: " + toaddrs,
                       "mime-version: 1.0",
                       "content-type: text/html"])

        content = headers + "\r\n\r\n" + msg

        username = 'lopez.geronimo213@gmail.com'
        password = 'aioplk4231'

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddrs, toaddrs, content)
        server.quit()
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about_me.html', AboutHandler),
    ('/favorites.html', FavoritesHandler),
    ('/index.html', MainHandler),
    ['/contact.html' MailHandler]
], debug=True)
