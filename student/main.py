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
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Student(ndb.Model):
    name = ndb.StringProperty(required = True)
    school = ndb.StringProperty(required = True)
    age = ndb.IntegerProperty(required = True)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/form.html')
        self.response.write(template.render())
    def post(self):
        user_name = self.request.get('name')
        user_school = self.request.get('school')
        user_age = self.request.get('age')
        student = Student(name = user_name, school = user_school, age = int(user_age) )
        student_key = student.put()
        self.response.write(user_name + "<br>" + user_school + "<br>" + user_age)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
