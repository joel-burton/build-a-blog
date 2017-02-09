import os
import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                        autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blog(db.Model):
    title = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(Handler):

    def render_blog(self, title="", entry="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

        self.render('newpost.html', title=title, entry=entry, error=error, blogs=blogs)


    def get(self):
        self.render_blog()


    def post(self):
        title = self.request.get('title')
        entry = self.request.get('entry')


        if title and entry:
            b = Blog(title = title, entry = entry)
            b.put()

            self.redirect('/')

        else:
            error = "Your new blog post needs a title and an entry!"
            self.render_blog(title, entry, error)








app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
