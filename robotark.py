import os
import json
from datetime import datetime, date, time

import webapp2
from webapp2_extras import sessions

import jinja2

from google.appengine.api import search
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'jhsdfln454toucre8n84r83yy',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.globals = {'isinstance': isinstance, 'str': str}

CATEGORIES = {
    'mechanics': {
        'general': 'general',
        'pneumatics': [
            'theory',
            'datasheets'
        ],
        'gearbox': 'gearbox',
        'drivetrain': 'drivetrain'
    },
    'electronics': {
        'datasheets': [
            'components',
            'sensors',
            'cots'
        ],
        'wiring': 'wiring',
        'controlsystem': [
            'crio',
            'roborio',
            'arduino',
            'others'
        ],
        'sensoring': 'sensoring',
        'theory': [
            'begginers',
            'advanced'
        ]
    },
    'programming': {
        'c': [
            'general',
            'windriver',
            'sensoring',
            'examples',
            'fullsystem'
        ],
        'labview': [
            'basics',
            'cv',
            'signalanalysis',
            'sensoring',
            'examples',
            'fullsystem'
        ],
    },
    'cad': {
        'autocad': 'autocad',
        'inventor': 'inventor',
        'solidworks': 'solidworks',
        'models': [
            'robots',
            'gearbox',
            'drivetrain',
            'others'
        ],
        'others': 'others'
    },
    'team': [
        'scouting',
        'sponsors',
        'chairmans',
        'events',
        'websites'
    ]
}


index = search.Index(name="posts")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ndb.Key):
            o = o.get(o)
        if isinstance(o, ndb.Model):
            return o.to_dict()
        elif isinstance(o, (datetime, date, time)):
            return str(o)


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class BaseUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class MainPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        content = {
            'user': user,
            'users': users
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("index.html").render(content))


class AboutPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        content = {
            'user': user,
            'users': users
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("about.html").render(content))


class UploadPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return
        upload_url = blobstore.create_upload_url('/upload_handler')
        content = {
            'upload_url': upload_url,
            'user': user,
            'users': users
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("upload.html").render(content))


class UploadHandler(BaseUploadHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(401)
            self.response.write('Not authorized')
        post = search.Document(
            fields=[
                search.TextField(name='poster_id', value=user.user_id()),
                search.TextField(name='poster_name', value=user.nickname()),
                search.TextField(name='author', value=self.request.get('author')),
                search.TextField(name='title', value=self.request.get('title')),
                search.TextField(name='subtitle', value=self.request.get('subtitle')),
                search.TextField(name='url', value=self.request.get('subsubcategory')),
                search.TextField(name='file_key', value=str(self.get_uploads()[0].key()))
            ])
        index.put(post)
        self.redirect('/')


class FileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, file_key):
        blob_info = blobstore.BlobInfo.get(file_key)
        if not blob_info:  # blobstore.get(file_key):
            self.error(404)
        else:
            self.send_blob(blob_info, save_as=True)
            # self.send_blob(file_key)


class CategoryHandler(BaseHandler):
    def get(self):
        path = self.request.path
        posts = index.search('url: "' + path + '"')
        category = list(path.split('/'))
        print category
        nested = None
        if CATEGORIES.get(category[1]):
            nested = CATEGORIES.get(category[1])
            for c in category[2:]:
                print 'loooooooooooooop'
                if isinstance(nested, str):
                    pass
                elif isinstance(nested, list):
                    nested = nested[nested.index(c)]
                else:
                    nested = nested.get(c)
            print nested
        else:
            print 'invalid category'

        content = {
            'posts': posts,
            'user': users.get_current_user,
            'users': users,
            'category': category,
            'nested': nested,
            'base': path
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("view.html").render(content))


class SearchPage(BaseHandler):
    def get(self):
        posts = index.search(self.request.get('category') + ': "' + self.request.get('query') + '"')
        nested = None
        category = "Search results"
        content = {
            'posts': posts,
            'user': users.get_current_user,
            'users': users,
            'nested': nested,
            'search': True,
            'query': self.request.get('query')
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("view.html").render(content))


class MePage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return
        content = dict(user=user, users=users)
        self.response.write(JINJA_ENVIRONMENT.get_template("me.html").render(content))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadPage),
    ('/about', AboutPage),
    ('/search', SearchPage),
    ('/me', MePage),
    ('/file/([^/]+)?', FileHandler),
    ('/upload_handler', UploadHandler),
    ('/.*', CategoryHandler)
], config=config, debug=True)
