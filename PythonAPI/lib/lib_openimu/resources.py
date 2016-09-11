from collections import defaultdict
import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort
from lib_openimu import  conf
from shared import mongo

class Hello(Resource):
    def get(self):
        d = datetime.datetime(2010, 11, 12, 12)
        data = mongo.db.accelerometre.find().sort("time")
        result = ""
        for datum in data:
            result+=str(datum)
        return result
