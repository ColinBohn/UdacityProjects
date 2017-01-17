import os
import re
import string
import hmac
import webapp2
import jinja2
from passlib.hash import sha512_crypt
from google.appengine.ext import db


######
# CONSTANTS
######
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                           autoescape=True)
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
COOKIE_SECRET = "eRRyaiI6Z8a3EI2yxYU80mzw9D3EXJuh"


######
# PAGE RENDERING HELPERS
######
def render_template_string(template, **params):
    t = JINJA.get_template(template)
    return t.render(params)


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class PageHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_string(self, template, **params):
        return render_template_string(template, **params)

    def render(self, template, **kw):
        self.write(self.render_string(template,
                   logged_in_user=self.cookie_user(), **kw))

    def cookie_user(self):
        cookie = self.request.cookies.get("user")
        if cookie:
            split = cookie.split('|')
            if split[1] == hmac.new(COOKIE_SECRET, split[0]).hexdigest():
                return split[0]
        return None

    def load_post(self, post_id):
        params = dict()
        params['post'] = Post.get_by_id(int(post_id))
        if not params['post']:
            self.error(404)
            return
        params['user'] = self.cookie_user()
        params['likes'] = Like.all().ancestor(params['post'])
        params['liked'] = Like.all().ancestor(params['post']) \
            .filter("username = ", params['user']).count()
        params['owner'] = False
        if params['user'] == params['post'].author:
            params['owner'] = True
        return params

    def load_comments(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        comments = Comment.all().ancestor(key)
        return comments


######
# DATASTORE CLASSES
######
class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_template_string("post.html", p=self)


class User(db.Model):
    username = db.StringProperty(required=True)
    hash = db.StringProperty(required=True)
    email = db.EmailProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class Comment(db.Model):
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)


class Like(db.Model):
    username = db.StringProperty(required=True)


######
# AUTHENTICATION HELPERS
######
def hash_pw(password):
    return sha512_crypt.encrypt(password)


def check_pw(password, hash):
    return sha512_crypt.verify(password, hash)


def create_cookie(self, user):
    hash = hmac.new(COOKIE_SECRET, user).hexdigest()
    self.response.headers.add_header('Set-Cookie',
                                     str("user=%s|%s" % (user, hash)))


def delete_cookie(self):
    self.response.headers \
        .add_header('Set-Cookie',
                    "user=; expires=Thu, 01 Jan 1970 00:00:00 GMT")


######
# PAGE HANDLERS
######
class BlogFront(PageHandler):
    def get(self):
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts)


class Signup(PageHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        elif User.all().filter("username = ", username).count():
            params['error_username'] = "Please try a different username."
            have_error = True
        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if email and not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            if email:
                u = User(username=username, hash=hash_pw(password),
                         email=email)
            else:
                u = User(username=username, hash=hash_pw(password))

            u.put()
            create_cookie(self, username)
            self.redirect('/welcome')


class Welcome(PageHandler):
    def get(self):
        if self.cookie_user():
            self.render('welcome.html')
        else:
            self.redirect('/signup')


class Login(PageHandler):
    def get(self):
        self.render("login-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        params = dict(username=username)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        if have_error:
            self.render('login-form.html', **params)
        else:
            user = db.GqlQuery("SELECT * FROM User WHERE username = :1",
                               username).get()
            if user and check_pw(password, user.hash):
                create_cookie(self, username)
                self.redirect('/welcome')
            else:
                params['login_error'] = True
                self.render('login-form.html', **params)


class Logout(PageHandler):
    def get(self):
        delete_cookie(self)
        self.redirect('/login')


class BlogPost(PageHandler):
    def get(self, post_id):
        pd = self.load_post(post_id)
        c = self.load_comments(post_id)

        self.render("permalink.html", post=pd['post'], owner=pd['owner'],
                    user=pd['user'], likes=pd['likes'], liked=pd['liked'],
                    comments=c)


class NewPost(PageHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        # TODO: Authenticate new posts
        title = self.request.get('subject')
        content = self.request.get('content')
        if not self.cookie_user():
            self.redirect('/login')
        else:
            if title and content:
                p = Post(title=title, content=content,
                         author=self.cookie_user(), likes=0)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))

            else:
                error = "Please enter both a title and content!"
                self.render("newpost.html", subject=title, content=content,
                            error=error)


class EditPost(PageHandler):
    def get(self, post_id):
        pd = self.load_post(post_id)
        self.render("newpost.html", subject=pd['post'].title,
                    content=pd['post'].content)

    def post(self, post_id):
        title = self.request.get('subject')
        content = self.request.get('content')
        pd = self.load_post(post_id)

        if not pd['user']:
            self.redirect('/login')

        if title and content:
            if pd['owner']:
                pd['post'].title = title
                pd['post'].content = content
                pd['post'].put()
                self.redirect('/blog/%s' % str(pd['post'].key().id()))
            else:
                self.response.out.write("You cannot edit someone else's post!")

        else:
            error = "Please enter both a title and content!"
            self.render("newpost.html", title=title, content=content,
                        error=error)


class DeletePost(PageHandler):
    def get(self, post_id):
        pd = self.load_post(post_id)

        if not pd['user']:
            self.redirect('/login')

        if pd['owner']:
            pd['post'].delete()
            self.redirect('/blog')
        else:
            self.response.out.write("You cannot delete someone else's post!")


class LikePost(PageHandler):
    def get(self, post_id):
        pd = self.load_post(post_id)

        if not pd['user']:
            self.redirect('/login')

        if pd['owner']:
            self.response.out.write("You cannot like your own post!")
        elif pd['user']:
            if not pd['liked']:
                l = Like(username=pd['user'], parent=pd['post'])
                l.put()
                self.redirect('/blog/%s' % str(pd['post'].key().id()))
            else:
                self.response.out.write("You have already liked this post!")
        else:
            self.response.out.write("You do not have permission to like!")


class UnlikePost(PageHandler):
    def get(self, post_id):
        pd = self.load_post(post_id)

        if not pd['user']:
            self.redirect('/login')

        if pd['owner']:
            self.response.out.write("You cannot dislike your own post!")
        elif pd['user']:
            if pd['liked']:
                l = Like.all().ancestor(pd['post']) \
                    .filter("username = ", pd['user'])
                l[0].delete()
                self.redirect('/blog/%s' % str(pd['post'].key().id()))
            else:
                self.response.out.write("You haven't liked this post!")
        else:
            self.response.out.write("You do not have permission to like!")


class NewComment(PageHandler):
    def post(self, post_id):
        pd = self.load_post(post_id)
        content = self.request.get('content')

        if pd['owner']:
            self.response.out.write("You cannot comment on your own post!")

        elif self.cookie_user():
            c = Comment(content=content, author=self.cookie_user(),
                        parent=pd['post'])
            c.put()
            self.redirect('/blog/%s' % str(pd['post'].key().id()))

        else:
            self.response.out.write("You must be logged in to comment!")


class EditComment(PageHandler):
    def get(self, post_id, comment_id):
        p = Post.get_by_id(int(post_id))
        c = Comment.get_by_id(int(comment_id), p)
        if self.cookie_user() == c.author:
            self.render("editcomment.html", content=c.content)
        else:
            self.response.out.write("You do not have permission to edit!")

    def post(self, post_id, comment_id):
        content = self.request.get('content')

        if content:
            p = Post.get_by_id(int(post_id))
            c = Comment.get_by_id(int(comment_id), p)
            if self.cookie_user() == c.author:
                c.content = content
                c.put()
                self.redirect('/blog/%s' % str(post_id))
            else:
                self.response.out.write("You cannot edit this comment!")

        else:
            error = "Please enter content!"
            self.render("editcomment.html", content=content, error=error)


class DeleteComment(PageHandler):
    def get(self, post_id, comment_id):
        p = Post.get_by_id(int(post_id))
        c = Comment.get_by_id(int(comment_id), p)
        if self.cookie_user() == c.author:
            c.delete()
            self.redirect('/blog/%s' % str(post_id))
        else:
            self.response.out.write("You cannot delete this comment!")


######
# URL ROUTING
######
app = webapp2.WSGIApplication([
    ('/', BlogFront),
    ('/signup/?', Signup),
    ('/welcome/?', Welcome),
    ('/login/?', Login),
    ('/logout/?', Logout),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)/?', BlogPost),
    ('/blog/new/?', NewPost),
    ('/blog/edit/([0-9]+)/?', EditPost),
    ('/blog/delete/([0-9]+)/?', DeletePost),
    ('/blog/like/([0-9]+)/?', LikePost),
    ('/blog/unlike/([0-9]+)/?', UnlikePost),
    ('/comment/new/([0-9]+)/?', NewComment),
    ('/comment/edit/([0-9]+)/([0-9]+)/?', EditComment),
    ('/comment/delete/([0-9]+)/([0-9]+)/?', DeleteComment)
], debug=True)
