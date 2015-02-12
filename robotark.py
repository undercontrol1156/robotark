# -*- coding: utf-8 -*-

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
from google.appengine.api import mail

config = {}
# Yay sending secret keys to GitHub
config['webapp2_extras.sessions'] = {
    'secret_key': 'jhsdfln454toucre8n84r83yy',
}

message = mail.EmailMessage(sender="RobotArk <robotark@eternal-empire-750.appspotmail.com>",
                            subject="Novo post a ser revisado", to="Time <robotica.1156@gmail.com>")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.globals = {'isinstance': isinstance, 'str': str, 'list': list}


CATEGORIES = {
    'mechanics': {
        'general': 'general',
        'pneumatics': [
            'theory',
            'datasheets'
        ],
        'gearbox': 'gearbox',
        'drivetrain': 'drivetrain',
        'design': 'design'
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
        # Bug or someone trying to hack us
        if not user:
            self.error(401)
            self.response.write('Not authorized')
            return
        if self.request.get('link'):
            print "got url"
            file_key = self.request.get('link')
        else:
            print "got file"
            file_key = '/file/' + str(self.get_uploads()[0].key())
        if self.request.get('stage'):
            stage = self.request.get('stage')
        else:
            stage = "public"
        post = search.Document(
            fields=[
                search.TextField(name='poster_id', value=user.user_id()),
                search.TextField(name='poster_name', value=user.nickname()),
                search.TextField(name='author', value=self.request.get('author')),
                search.TextField(name='title', value=self.request.get('title')),
                search.TextField(name='subtitle', value=self.request.get('subtitle')),
                search.TextField(name='url', value=self.request.get('subsubcategory')),
                search.TextField(name='file_key', value=file_key),
                search.TextField(name='private', value=stage)
            ])
        if self.request.get('stage') == 'staged':
            message.body = 'O usuário %s postou um novo arquivo. Vá a robotark.org/review para revisar' % user.nickname()
        message.send()
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
        posts = index.search('url: "' + path + '" AND private = "public"')
        category = list(path.split('/'))
        print category
        nested = None
        # Don't ask me what's going on here
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
        # EODM (End of dark magic)
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
        posts = index.search(self.request.get('category') + ': ' + self.request.get('query') + ' AND private = "public"')
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


class ShortLinkHandler(BaseHandler):
    def get(self, id):
        post = [index.get(id)]
        content = {
            'posts': post,
            'user': users.get_current_user,
            'users': users
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("view.html").render(content))


class StatsPage(BaseHandler):
    def get(self):
        data = index.get_range().results
        print data
        team = [t.fields[2].value.split(' ')[0] for t in data]
        output = []
        for t in set(team):
            output.append([t, team.count(t)])
        content = {
            'data': json.dumps(output),
            'user': users.get_current_user,
            'users': users
        }
        self.response.write(JINJA_ENVIRONMENT.get_template("stats.html").render(content))


class DeleteHandler(BaseHandler):
    def post(self):
        if users.is_current_user_admin():
            try:
                index.delete(self.request.get('id'))
                self.redirect('/')
            except search.Error:
                self.error(404)
                print 'no such Document'
        else:
            self.error(403)


class MePage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url())
            return
        content = dict(user=user, users=users)
        self.response.write(JINJA_ENVIRONMENT.get_template("me.html").render(content))


class ReviewPage(BaseHandler):
    def get(self):
        if users.is_current_user_admin():
            posts = index.search('private = "staged"')
            category = "Review"
            content = {
                'posts': posts,
                'user': users.get_current_user,
                'users': users,
                'review': True
            }
            self.response.write(JINJA_ENVIRONMENT.get_template("view.html").render(content))
        else:
            self.error(403)
            return


class ApproveHandler(BaseHandler):
    def post(self):
        if users.is_current_user_admin():
            doc_id = self.request.get('id')
            post = index.get(doc_id)
            post.fields[7] = search.TextField(name='private', value="public")
            index.put(post)
            self.redirect('/review')
        else:
            self.error(403)


# class MigrateDebug(BaseHandler):
#    def get(self):
#        if users.is_current_user_admin():
#            for p in index.get_range().results:
#                p.fields.append(search.TextField(name='private', value="public"))
#                index.put(p)


# # # # # # # # # # # # BEGIN API # # # # # # # # # # # # # #
#                  TODO: Develop API                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadPage),
    ('/link/([^/]+)?', ShortLinkHandler),
    ('/about', AboutPage),
    ('/search', SearchPage),
    ('/delete', DeleteHandler),
    ('/me', MePage),
    ('/review', ReviewPage),
    ('/approve', ApproveHandler),
    ('/stats', StatsPage),
    ('/file/([^/]+)?', FileHandler),
    ('/upload_handler', UploadHandler),
    ('/.*', CategoryHandler)
], config=config, debug=True)
