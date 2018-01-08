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
import os
import webapp2
import jinja2

import json
import logging

from google.appengine.ext import ndb
from models.story import Entry

#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape=True)#Important Autoescape
load_first_time = True

#creates a parent key on old db models
#def blog_key(name = 'default'):
#    return db.Key.from_path('blogs', name)

def defaultList():
    thelist = ["Ir al gym",
         "Pagar el agua",
         "Cita con Cata",
         "Comprar huevos",
         "Leer un librio",
         "Pasar el trapito" ]
    for e in thelist:
        en=Entry(title=e)
        en.put()

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render (self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        global load_first_time
        if(load_first_time):
            ndb.delete_multi(
                Entry.query().fetch(keys_only=True))
            defaultList()
            load_first_time=False
        q = Entry.query().order(-Entry.created)
        logging.info("Count="+str(q.count(100)))
        entries = q.fetch(q.count(100))
        #logging.info(json.dumps(entries))
        self.render("content.html", entries = entries)
        #story = Story.get_or_insert('story id or so',title='Supe/r/ funny story')
        #params = {'story':story}
        #self.render("content.html",**params)

class VoteHandler(Handler):
    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        story = ndb.Key(Story, data['storyKey']).get()
        story.vote_count += 1
        story.put()
        self.write(json.dumps(({'story': story.to_dict()})))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vote/', VoteHandler)
], debug=True)
