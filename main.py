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
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

##creates a new fridge
class Family(ndb.Model):
    fridge_name = ndb.StringProperty(required=True)

##creates a new person with access to a certain fridge
class Person(ndb.Model):
    fridge_key = ndb.KeyProperty(kind='Family')
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)

##manually creates a user in the database
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/newUser.html')
        self.response.write(template.render())


class NewFridge(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/newFridge.html')
        self.response.write(template.render())


##this will post out the ID number for a family when a new fridge is created
class FamilyID(webapp2.RequestHandler):
    def post(self):
        nameforFID = self.request.get("fridge_name")
        nameforFID_key = (Family(fridge_name = nameforFID).put())
        template = jinja_environment.get_template('templates/FamilyID.html')
        self.response.write(template.render({'Family_ID': nameforFID_key.id()}))

class PersonID(webapp2.RequestHandler):
    def post(self):
        fridge_key = ndb.Key(Family, int(self.request.get("fridge_key")))
        user_first = self.request.get("user_first")
        user_last = self.request.get("user_last")
        nameforPID_key = (Person(fridge_key = fridge_key, first_name = user_first, last_name = user_last).put())
        template = jinja_environment.get_template('templates/thankyou.html')
        self.response.write(template.render({'user_first': user_first, 'user_last': user_last}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newFridge', NewFridge),
    ('/FamilyID', FamilyID),
    ('/PersonID', PersonID),
], debug=True)
