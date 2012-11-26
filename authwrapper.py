from slstracker import app
import sys
class AuthWrapper(object):
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        environ['REMOTE_USER'] = sys.argv[2]
        environ['fullname'] = sys.argv[2]
        return self.app(environ, start_response)

application = AuthWrapper(app)
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', int(sys.argv[1]), application, use_reloader=True, use_debugger=True, use_evalex=True)
