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

import logging
from google.appengine.ext import ndb
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(extensions=['jinja2.ext.autoescape'], loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

##creates a new fridge
class Family(ndb.Model):
    fridge_name = ndb.StringProperty(required=True)
    posts = ndb.StringProperty(repeated=True) ##To do more than one post

##creates a new person with access to a certain fridge
class Person(ndb.Model):
    fridge_key = ndb.KeyProperty(kind='Family')
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)

class User(ndb.Model):
    thing = ndb.KeyProperty()

class UserAccount(ndb.Model):
    fridge_list=ndb.StringProperty(repeated=True)


##manually creates a user in the database
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        user = users.get_current_user()
        if user:
            #Signed In
            greeting = (' Welcome, %s! (<a href="%s">sign out</a>)' %
                       #(user.user_id(), users.create_logout_url('/')))
                       (user.nickname(), users.create_logout_url('/')))

        else:
            #Signed Out and NEED to Sign In

            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
        self.response.write(greeting)

class NewUser(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/newUser.html')
        self.response.write(template.render())

class NewFridge(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/newFridge.html')
        self.response.write(template.render())

class FridgeHome(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        global fridges_list
        fridges_list = []

        global userProfile
        userProfile = UserAccount.get_by_id(user.email())

        if userProfile:
            fridges_list = userProfile.fridge_list
            logging.warning(fridges_list)
        else:
            new_user = UserAccount(id=user.email(), fridge_list=[])
            new_user.put()
            userProfile = UserAccount.get_by_id(user.email())


        fridge_nicknames = []

        if fridges_list != ['']:
            for fridge in fridges_list:
                unnamed_fridge = Family.get_by_id(int(fridge))
                logging.warning(unnamed_fridge)
                fridge_nicknames.append(str(unnamed_fridge.fridge_name))
                logging.warning(str(fridge_nicknames))

        fridge_dictionary = dict(zip(fridges_list, fridge_nicknames))
        logging.warning(fridge_dictionary)
        template = JINJA_ENVIRONMENT.get_template('templates/fridgeHome.html')
        self.response.write(template.render(fridge_dictionary = fridge_dictionary))
        ##self.response.write("<h2>" + user.email() + "</h2>")
    def post(self):
        fridge_to_join = str(self.request.get('join_fridge'))
        fridges_list.append(fridge_to_join)
        userProfile.fridge_list = fridges_list
        userProfile.put()
        self.get()



##this will post out the ID number for a family when a new fridge is created
 ##This is a global variable that we will use for the different posts on the fridge
global fridgeposts

fridgeposts = [] ##just so it works
class FamilyID(webapp2.RequestHandler):
    def post(self):
        nameforFID = self.request.get("fridge_name")
        nameforFID_key = (Family(fridge_name = nameforFID).put())
        template = jinja_environment.get_template('templates/FamilyID.html')
        self.response.write(template.render({'Family_ID': nameforFID_key.id()}))

    def get(self):
        user = users.get_current_user()

        userProfile = UserAccount.get_by_id(user.email())
        user_email = users.get_current_user().nickname()

        fridges_list = userProfile.fridge_list

        fridges_list.append((self.request.get('Family_ID')))

        userProfile.fridge_list = fridges_list
        userProfile.put()

        template = JINJA_ENVIRONMENT.get_template('templates/thankyou.html')
        self.response.write(template.render({'user_email': user_email}))

class PersonID(webapp2.RequestHandler):
    def post(self):
        fridge_key = ndb.Key(Family, int(self.request.get("fridge_key")))
        user_first = self.request.get("user_first")
        user_last = self.request.get("user_last")
        nameforPID_key = (Person(fridge_key = fridge_key, first_name = user_first, last_name = user_last).put())
        template = jinja_environment.get_template('templates/thankyou.html')
        self.response.write(template.render({'user_first': user_first, 'user_last': user_last}))

class FridgePage(webapp2.RequestHandler):
    def get(self):
        global current_FridgeID
        current_FridgeID = self.request.get('fridge')

        global current_fridge
        current_fridge = Family.get_by_id(int(current_FridgeID))

        global fridgeposts
        fridgeposts = current_fridge.posts

        fridge_name = current_fridge.fridge_name

        template = JINJA_ENVIRONMENT.get_template('templates/fridgePage.html')
        self.response.write(template.render(fridgeposts = fridgeposts, fridge_name = fridge_name, current_fridge = current_FridgeID))
    def post(self):
        new_post = self.request.get('post')
        fridgeposts.append(str(new_post))

        current_fridge.posts = fridgeposts
        current_fridge.put()

        fridge_name = current_fridge.fridge_name

        logging.info(fridgeposts)

        self.get()

class ThankYou(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()


        userProfile = UserAccount.get_by_id(user.email())
        user_email = users.get_current_user().nickname()

        fridges_list = userProfile.fridge_list
        fridges_list.append((self.request.get('Family_ID')))

        userProfile.fridge_list = fridges_list
        userProfile.put()

        template = JINJA_ENVIRONMENT.get_template('templates/thankyou.html')
        self.response.write(template.render({'user_email': user_email}))

class DeletePost(webapp2.RequestHandler):
    def get(self):
        current_fridge_ID = self.request.get('current_fridge')

        post_to_delete = self.request.get('post')
        current_fridge = Family.get_by_id(int(current_fridge_ID))
        logging.warning(current_fridge)

        current_list = current_fridge.posts

        post_to_delete.replace('+', ' ')
        post_to_delete.replace('%21', '!')
        str(post_to_delete)
        logging.warning(post_to_delete)

        #for n,i in enumerate(current_list):
        #    if i == '+':
        #        a[n] = ' '
        #    if i == '%21':
        #        a[n] = '!'

        current_list.remove(post_to_delete)
        current_fridge.posts = current_list
        current_fridge.put()

        template = JINJA_ENVIRONMENT.get_template('templates/deleted.html')
        self.response.write(template.render(fridge_id = current_fridge_ID))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Login', LoginHandler),
    ('/newUser', NewUser),
    ('/newFridge', NewFridge),
    ('/fridgeHome', FridgeHome),
    ('/FamilyID', FamilyID),
    ('/PersonID', PersonID),
    ('/Fridge', FridgePage),
    ('/fridgeHome', FridgeHome),
    ('/ThankYou', ThankYou),
    ('/deletePost', DeletePost),

], debug=True)
