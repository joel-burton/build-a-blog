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




class MainHandler(Handler):
    def get(self):
        self.render('newpost.html')

    def post(self):
        title = self.request.get('title')
        entry = self.request.get('entry')
        error = ""


        if title and entry:
            self.redirect('/')

        else:
            error = "Your new blog post needs a title and an entry!"
            self.render('newpost.html', title=title, entry=entry, error=error)








app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
