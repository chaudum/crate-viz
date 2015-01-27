# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"

import os
import sys
import json
import argparse

from crate import client

from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.web import Application, StaticFileHandler, RequestHandler


class StaticHandler(StaticFileHandler):

    def get_absolute_path(self, root, path):
        full_path = os.path.join(root, path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            return os.path.join(full_path, 'index.html')
        return full_path


class HistoryHandler(RequestHandler):

    def prepare(self):
        db = client.connect('127.0.0.1:4200')
        self.cursor = db.cursor()

    def get(self):
        self.cursor.execute('select ts from cluster_viz order by ts desc limit 1')
        res = self.cursor.fetchone()
        self.cursor.execute('select ts, name, load, num_shards, disk_bytes from cluster_viz where ts = ? order by name', res)
        res = self.cursor.fetchall()
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(res))


def main():
    parser = argparse.ArgumentParser(description='Development Server')
    parser.add_argument('path', metavar='path', type=str)
    parser.add_argument('--port', dest='port', type=int, default='8080', help='server port')
    args = parser.parse_args()
    parse_command_line()
    app = Application([
        (r"/data.json$", HistoryHandler),
        (r"/(.*)", StaticHandler, {"path": args.path}),
    ], debug=True)
    app.listen(args.port)
    IOLoop.instance().start()
