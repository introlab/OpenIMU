from collections import defaultdict
import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort
from lib_openimu import  conf
from algos.fft import run, invert
from shared import mongo
import schemas
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
        result = []
        for datum in accelerometres:
            datum['ref'] = uuid

        mongo.db.accelerometre.insert(accelerometres)
#---------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        gyrometres,errors = schema.dump(data['gyrometres'])
        result = []
        for datum in gyrometres:
            datum['ref'] = uuid

        mongo.db.gyrometres.insert(gyrometres)
#---------------------------------------------------------------
        schema = schemas.Sensor(many=True)
        magnetometres,errors = schema.dump(data['magnetometres'])
        result = []
        for datum in magnetometres:
            datum['ref'] = uuid

        mongo.db.magnetometres.insert(magnetometres)
#---------------------------------------------------------------
        return str(uuid)
