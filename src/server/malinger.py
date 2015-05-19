#!/usr/bin/python
#encoding:utf-8

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options, parse_command_line
from util.log.log import runtime_log
from util.conf.conf import get_conf
import router
import os

logger = runtime_log()
conf = get_conf()

port = int(conf.get("global", "port"))
debug_mode = int(conf.get("global", "server_debug_mode"))

settings = {
        "debug":debug_mode,
    }

define("port", default=port, help="malinger listen port")

def main():
    parse_command_line()
    logger.info("start malinger server at %s" % options.port)
    app = tornado.web.Application(router.url_map, **settings)
    server = tornado.httpserver.HTTPServer(app)

    server.bind(options.port)
    server.start(1 if debug_mode else 5)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()