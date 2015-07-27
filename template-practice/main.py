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
import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))#this little bit sets jinja's relative directory to match the directory name(dirname) of the current __file__, in this case, helloworld.py

class MainHandler(webapp2.RequestHandler):
    def get(self):
        name_var = self.request.get('chosen_name', default_value='World!')
        greeting = self.request.get('chosen_greeting', default_value='Howdy, ')
        language = self.request.get('hl')
        message = 'How are you?'
        if language == "en-US" or language == 'en':
            message = "How are you?"
        elif language == "fr-FR" or language == "fr":
            message = "Comment allez-vous?"
            greeting = 'Bonjour, '
        else:
            pass
        template = jinja_environment.get_template('hello.html')
        self.response.out.write(template.render({'name': name_var, 'greeting': greeting, 'how_are_you': message}))


"""class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')"""

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
