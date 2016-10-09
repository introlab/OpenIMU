from collections import defaultdict
import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort,reqparse
from lib_openimu import  conf
import algos.activityTracker
import algos
from shared import mongo
import schemas
import numpy
from math import sqrt


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
        uuid = request.args.get('uuid')
        if uuid is None:
            abort(401,message='enter valid uuid')
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

class DeleteData(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        if uuid is None:
            abort(401,message='enter valid uuid')
        res1 = mongo.db.accelerometres.delete_many({'ref':ObjectId(uuid)})
        res2 = mongo.db.gyrometres.delete_many({'ref':ObjectId(uuid)})
        res3 = mongo.db.magnetometres.delete_many({'ref':ObjectId(uuid)})
        res4 = mongo.db.record.delete_many({'_id':ObjectId(uuid)})
        result = res1.deleted_count+res2.deleted_count+res3.deleted_count+res4.deleted_count
        return 'Affected ' + str(result)     + ' entries.'

class TestInsert(Resource):
    def get(self):
        snaps = []
        amp = 100
        fs = 20

        uudi = ObjectId('57ed3f20e0034625e8fa61f1')
        dict = [
            {'x': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'y': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'z': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             't': r,
             'ref': uudi
            } for r in range(1, fs)]
        schema = schemas.Sensor(many=True)
        result, _ = schema.load(dict)

        mongo.db.accelerometres.insert(result)
        return 1


class Tracker_Activity(Resource):
    def get(self):
        schema = schemas.Sensor(many=True)
        accelerometres,errors = schema.dump(mongo.db.accelerometres.find())

        total = algos.activityTracker.run(accelerometres)
        #activity = algos.activity_tracker()
        #activity.getInput()
        #activity.run()
        response = total
        return response


class Algo(Resource):
    def get(self):
        modulename = 'algos.'+request.args.get('filename')
        print(modulename)
        my_module = __import__(modulename, globals(), locals(), ['ActivityTracker'], -1)
        my_object = my_module.ActivityTracker()
        print(my_object.test())

        #my_class = getattr(module,'Test').object

        instance = my_object.test()

        return instance