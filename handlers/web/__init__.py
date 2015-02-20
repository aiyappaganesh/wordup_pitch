import webapp2
from .web_request_handler import WebRequestHandler
from .index import HomePage

app = webapp2.WSGIApplication([
    ('/', HomePage)
])