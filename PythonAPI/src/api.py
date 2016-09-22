#!/usr/bin/env python
import sys

from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, abort

sys.path.append('..//lib')
from lib_openimu import conf, resources
from lib_openimu.shared import ma, mongo

# setup app, config, db
app = Flask(__name__)
app.config.from_object(conf)
ma.init_app(app)
mongo.init_app(app)
api = Api(app)


# Auth Routes
api.add_resource(resources.InsertRecord, '/insertrecord')
api.add_resource(resources.getRecords, '/records')
api.add_resource(resources.GetData, '/data')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
