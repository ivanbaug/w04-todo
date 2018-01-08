from google.appengine.ext import ndb

class Entry(ndb.Model):
    title = ndb.StringProperty(required=True)
    #vote_count = ndb.IntegerProperty(default = 0)
    is_done = ndb.BooleanProperty(default = False)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    def render(self):
        #self._render_text = self.content.replace('\n', '<br>')
        #return render_str("post.html", p = self)
        return None
