import os
import re
import string
import webapp2
import jinja2
from google.appengine.ext import db

# Define our constants
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape = True)

def render_template_string(template, **params):
    t = JINJA.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_string(self, template, **params):
        return render_template_string(template, **params)

    def render(self, template, **kw):
        self.write(self.render_string(template, **kw))

        

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        render_template_string("post.html", p = self)
    
class BlogFront(BlogHandler):
    def get(self):
        posts = Post.all().order('-created') #TODO: How do I add a limit to this?
        self.render('front.html', posts = posts)
        
class BlogPost(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        
        if not post:
            self.error(404)
            return
        
        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")
        
    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')
        
        if title and content:
            p = Post(title = title, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        
        else:
            error = "Please enter both a title and content!"
            self.render("newpost.html", title=title, content=content, error=error)
            
app = webapp2.WSGIApplication([
    ('/', BlogFront),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)', BlogPost),
    ('/blog/newpost', NewPost),
], debug=True)