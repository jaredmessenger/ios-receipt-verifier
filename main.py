import os

from tornado import web, httpclient, httpserver, ioloop, escape
from tornado.options import define, options

import request_handler

# override the port in command line with -port=8001
define("port", default=8000, help="Run on port 8000", type=int)

class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/game/(.*)', request_handler.MainHandler),
            (r'/status', request_handler.StatusCheckHandler),
            ]
        
        settings = dict()
        
        web.Application.__init__(self, handlers, **settings)

def main(*args, **kwargs):
    options.parse_command_line()
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()