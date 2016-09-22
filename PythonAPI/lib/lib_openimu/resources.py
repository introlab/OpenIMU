from collections import defaultdict
import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort
from lib_openimu import  conf
from algos.fft import run, invert
from shared import mongo
import schemas
from bson.objectid import ObjectId

class InsertRecord(Resource):
    def post(self):
        schema = schemas.RecordRequest()
        data, errors = schema.load(request.json)
        if errors:
            abort(401, message=str(errors))
#---------------------------------------------------------------
        schema = schemas.Record()
        record,errors = schema.dump(data['record'])
        if errors:
            abort(401, message=str(errors))

        uuid = mongo.db.record.insert(record)
#---------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        accelerometres,errors = schema.dump(data['accelerometres'])
        if errors:
            abort(401, message=str(errors))
        for datum in accelerometres:
            datum['ref'] = uuid

        mongo.db.accelerometres.insert(accelerometres)
#---------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        gyrometres,errors = schema.dump(data['gyrometres'])
        if errors:
            abort(401, message=str(errors))
        for datum in gyrometres:
            datum['ref'] = uuid

        mongo.db.gyrometres.insert(gyrometres)
#---------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        magnetometres,errors = schema.dump(data['magnetometres'])
        if errors:
            abort(401, message=str(errors))
        for datum in magnetometres:
            datum['ref'] = uuid

        mongo.db.magnetometres.insert(magnetometres)
#---------------------------------------------------------------
        return str(uuid)

class getRecords(Resource):
    def get(self):
        schema = schemas.Record(many=True)
        return schema.dump(mongo.db.record.find({},{'name':1,'_id':1}))

class GetData(Resource):
    def get(self):
        uuid = request.args.get('uuid', '')

        schema = schemas.Record()
        record,errors = schema.dump(mongo.db.record.find_one({'_id': ObjectId(uuid)}))
        #if errors:
        #    abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        accelerometres,errors = schema.dump(mongo.db.accelerometres.find({'ref': ObjectId(uuid)}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        magnetometres,errors = schema.dump(mongo.db.magnetometres.find({'ref': ObjectId(uuid)}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        gyrometres,errors = schema.dump(mongo.db.gyrometres.find({'ref': ObjectId(uuid)}))
        if errors:
            abort(401, message=str(errors))
#--------------------------------------------------------------
        schema = schemas.RecordRequest()
        result,errors = schema.load(dict([('record', record), ('accelerometres', accelerometres), ('magnetometres', magnetometres), ('gyrometres',gyrometres)]))
        #if errors:
            #abort(401, message=str(errors))
        return result
