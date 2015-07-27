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
        krebs = Family(fridge_name = 'Krebs\' Fridge')
        krebs_key = krebs.put()
        carly = Person(fridge_key = krebs_key, first_name = 'Carly', last_name = 'Krebs')
        carly.put()
        self.response.write('Hello world!')

##this will post out the ID number for a family when a new fridge is created
class FamilyID(webapp2.RequestHandler):
    def post(self):
        template = jinja_environment.get_template('templates/FamilyID.html')
        self.response.write(template.render({'Family_ID': krebs_key.id()}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/FamilyID', FamilyID),
], debug=True)
