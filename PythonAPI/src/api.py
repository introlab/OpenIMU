#!/usr/bin/env python
import sys

from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, abort,reqparse

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
api.add_resource(resources.InsertRecord, '/insertrecord','/insertrecord/concat/<string:uuid>')
api.add_resource(resources.InsertAlgorithmResults, '/insertalgorithmresults')
api.add_resource(resources.getRecords, '/records')
api.add_resource(resources.getAlgorithmResults, '/algoResults')
api.add_resource(resources.renameRecord, '/renamerecord/<string:uuid>')
api.add_resource(resources.GetData, '/data')
api.add_resource(resources.DeleteData, '/delete')
api.add_resource(resources.Algo,'/algo')
api.add_resource(resources.AlgoList,'/algolist')
api.add_resource(resources.Position,'/position')
api.add_resource(resources.TestInsert,'/testinsert')
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
