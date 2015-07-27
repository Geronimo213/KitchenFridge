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
import random
import logging

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class RollHandler(webapp2.RequestHandler):
    def get(self):
        number_of_rolls = 1
        #roll1 = random.randint(1, 6)
        #roll2 = random.randint(1, 6)
        roll_limit = int(self.request.get('n'))


        while number_of_rolls <= roll_limit:
            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            self.response.write('Roll %d --- %d, %d. <br>' %(number_of_rolls, roll1, roll2))
            number_of_rolls += 1

        """while roll1 != 6 or roll2 != 6:
            if roll1 == 1 and roll2 == 1:
                self.response.write('Rolled %d %d . Snake eyes!<br>' %(roll1, roll2))
                roll1 = random.randint(1, 6)
                roll2 = random.randint(1, 6)
                number_of_rolls += 1
            else:
                self.response.write('Rolled %d %d <br>' %(roll1, roll2))
                roll1 = random.randint(1, 6)
                roll2 = random.randint(1, 6)
                number_of_rolls += 1
        self.response.write('Rolled %d %d . It took %d tries.<br>' %(roll1, roll2, number_of_rolls))
        self.response.write(self.request.get('n'))"""

class CheckHandler(webapp2.RequestHandler):
    def get(self):
        n = self.request.get('n')
        if n.isdigit():
            if IsPrime(int(n)) == True:
                self.response.write('%s is prime' %(n))
            else:
                self.response.write('%s is not prime' %(n))

        else:
            self.response.write('To check whether a number is prime, please add ?n=YOUR NUMBER HERE to the end of the address bar.')

def IsPrime(n):
    for possible_factor in range(2, n):
        if n % possible_factor == 0:
            return False
    return True

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/roll', RollHandler),
    ('/check', CheckHandler)
], debug=True)
