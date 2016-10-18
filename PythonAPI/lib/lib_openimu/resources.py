from collections import defaultdict
import datetime as dt
from flask import jsonify, request, make_response
from flask_restful import Resource, Api, abort,reqparse
from lib_openimu import  conf
import algos
from shared import mongo
import schemas
import numpy
from math import sqrt
from bson.objectid import ObjectId
import os

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
        return schema.dump(mongo.db.record.find())
        
class getDataWithOptions(Resource):
    def get(self):
        schemaDataRequestWithOptions = schemas.DataRequestWithOptions()
        dataRequestWithOptions, dataRequestWithOptionsErrors = schemaDataRequestWithOptions.load(request.json)
        if dataRequestWithOptionsErrors:
            abort(401, message=str(dataRequestWithOptionsErrors))

        # Retrieve Filter
        timeFilterSchema = schemas.TimeFilter()
        timeFilterData, timeFilterErrors = timeFilterSchema.load(dataRequestWithOptions['timeFilter'])
        if timeFilterErrors:
            abort(401, message=str(timeFilterErrors))

        # Retrieve Sort
        sortSchema = schemas.DataSort()
        sortData, sortErrors = sortSchema.load(dataRequestWithOptions['sort'])
        if sortErrors:
            abort(401, message=str(sortErrors))

        # Retrieve UUID
        uuidData, uuidErrors = schemaDataRequestWithOptions.load(dataRequestWithOptions['recordId'])
        if uuidErrors:
            abort(401, message='enter valid uuid')
            return

        recordSchema = schemas.Record()

        # Build request
        #  No filter, no sort. Just return all the record matching the UUID
        if (timeFilterData is None) & (sortData is None):
            return recordSchema.dump(mongo.db.record.find({}, {'name': 1, '_id': uuidData}))

        # Filter and Sort the record that matches the UUID
        if (timeFilterData is not None) & (sortData is not None):
            start = timeFilterData['beginDateTime']
            end = timeFilterData['endDateTime']
            if sortData['sortedDirection'] == 1:
                return recordSchema.dump(
                    mongo.db.record.find({}, {'_id': uuidData, 'date':{'$lt': end, '$gte': start}}).sort(sortData['sortedColumn'], mongo.ASCENDING))
            elif sortData['sortedDirection'] == 2:
                return recordSchema.dump(
                    mongo.db.record.find({}, {'_id': uuidData, 'date':{'$lt': end, '$gte': start}}).sort(sortData['sortedColumn'], mongo.DESCENDING))
            else:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData, 'date':{'$lt': end, '$gte': start}}))

        # Filter only the record that matches the UUID
        if (timeFilterData is not None) & (sortData is None):
            start = timeFilterData['beginDateTime']
            end = timeFilterData['endDateTime']
            return recordSchema.dump(mongo.db.record.find({'_id': uuidData, 'date':{'$lt': end, '$gte': start}}))

        # Sort only the record that matches the UUID
        if (timeFilterData is None) & (sortData is not None):
            if sortData['sortedDirection'] == 1:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}).sort(sortData['sortedColumn'], mongo.ASCENDING))
            elif sortData['sortedDirection'] == 2:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}).sort(sortData['sortedColumn'], mongo.DESCENDING))
            else:
                return recordSchema.dump(mongo.db.record.find({'_id': uuidData}))

class GetData(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        if uuid is None:
            abort(401,message='enter valid uuid')
            return
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

        uuid = ObjectId('57ed3f20e0034625e8fa61f1')
        dict = [
            {'x': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'y': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             'z': int(amp*numpy.sin (2*numpy.pi*r/fs)),
             't': r,
             '_id': uuid
            } for r in range(1, fs)]
        schema = schemas.Sensor(many=True)
        result, _ = schema.load(dict)

        mongo.db.accelerometres.insert(result)
        return str(uuid)

class Algo(Resource):
    def get(self):
        modulename = 'algos.'+request.args.get('filename')

        my_module = __import__(modulename, globals(), locals(), [request.args.get('filename')], -1)
        my_class = getattr(my_module,request.args.get('filename'))
        instance = my_class()
        instance.database = mongo
        instance.load(request.args)
        return instance.run()

class Params(Resource):
    def get(self):
        modulename = 'algos.'+request.args.get('filename')
        my_module = __import__(modulename, globals(), locals(), [request.args.get('filename')], -1)
        my_class = getattr(my_module,request.args.get('filename'))
        instance = my_class()
        instance.load(request.args)
        return str(instance.params.keys())


class AlgoList(Resource):
    def get(self):
        files = [os.path.splitext(file)[0]
                for file in os.listdir("../lib/algos")
                 if (file.endswith(".py") and not file.startswith('__'))
                ]

        return files

class Position(Resource):
    def get(self):
        schema = schemas.Position(many=True)
        positions,errors = schema.dump(mongo.db.position.find())
        if errors:
            abort(401, message=str(errors))
        return positions

    def post(self):
        schema = schemas.Position()
        position, errors = schema.load(request.json)
        if errors:
            abort(401, message=str(errors))
        mongo.db.position.insert(position)
        return

    def delete(self):
        name = request.args.get('pos')
        if name is None:
            abort(401,message='enter valid name')
        res = mongo.db.position.delete_many({'name':name})
        return 'Affected ' + str(res.deleted_count) + ' entries.'
