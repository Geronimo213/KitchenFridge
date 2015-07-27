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
import logging

jinja_environment =jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))#this little bit sets jinja's relative directory to match the directory name(dirname) of the current __file__, in this case, helloworld.py

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Do. Or do not. There is no try.')

class CountHandler(webapp2.RequestHandler):
    def get(self):
        i = 0
        for i in range(i, 101):
            self.response.write(" " + str(i))

"""class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/obiwan.html')
        self.response.out.write(template.render())
        logging.info('Judge me by my logs, do you?')
        '''n = 10
        if IsPrime(n) == True:
            self.response.write('%d is prime' %(n))
        else:
            self.response.write('%d is not prime' %(n))

def IsPrime(n):
    for possible_factor in range(2, n):
        if n % possible_factor == 0:
            return False
        else:
            return True

'''class MainHandler(webapp2.RequestHandler):
    def get(self):
        message = 'Help me, Obi-Wan Kenobi. '
        message = message + 'You\'re my only hope. '
        message = message + '2'
        if True:
            self.response.write('Your overconfidence is your weakness.')
        else:
            self.response.write('Your faith in your friends is yours.')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        sentence = 'Hello, world!'
        self.response.write(TalkLikeAJedi(sentence))
def TalkLikeAJedi(sentence):
    sentence = sentence.strip().rstrip('.!')
    sentence = sentence[0].lower() + sentence[1:]
    sentence = 'Patience: ' + sentence + ', my youg padawan.'
    return sentence'''"""

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/count', CountHandler)
], debug=True)
