from marshmallow import fields, Schema, post_dump
import math

class Record(Schema):
    name = fields.Str()
    format = fields.Str()
    position = fields.Str()
    comment = fields.Str()
    parent_id = fields.Str()
    _id = fields.UUID()

class ParameterInfo(Schema):
    name = fields.Str();
    description = fields.Str();
    value = fields.Str();
    defaultValue = fields.Str();

class AlgorithmInfo(Schema):
    name = fields.Str();
    filename = fields.Str();
    author = fields.Str();
    description = fields.Str();
    details = fields.Str();
    id = fields.Str();
    parameters = fields.Nested(ParameterInfo, many=True);

class AlgorithmResults(Schema):
    value = fields.Int(as_string = False);
    executionTime = fields.Float(as_string = False);
    resultName = fields.Str();
    date = fields.Str();
    startTime = fields.Str();
    endTime = fields.Str();
    measureUnit = fields.Str();
    algorithmId = fields.Str();
    algorithmName = fields.Str();
    algorithmParameters = fields.Nested(ParameterInfo, many=True);
    recordId = fields.Str();
    recordImuPosition = fields.Str();
    recordImuType = fields.Str();
    recordName = fields.Str();

class Sensor(Schema):
    x = fields.Float(as_string = False)
    y = fields.Float(as_string = False)
    z = fields.Float(as_string = False)
    t = fields.Int(as_string = False)
    ref = fields.Str()

class RecordRequest(Schema):
    record = fields.Nested(Record)
    accelerometres = fields.Nested(Sensor, many=True)
    magnetometres = fields.Nested(Sensor, many=True)
    gyrometres = fields.Nested(Sensor, many=True)

class TimeFilter(Schema):
    beginDateTime = fields.DateTime(as_string = False)
    endDateTime = fields.DateTime(as_string=False)

class DataSort(Schema):
    sortedColumn = fields.String()
    # Sort: 1 = Ascending, 2 = Descending, Any other values = No sort.
    sortDirection = fields.Int(as_string= False)

class DataRequestWithOptions(Schema):
    timeFilter = fields.Nested(TimeFilter)
    sort = fields.Nested(DataSort)
    recordId = fields.UUID()

class Position(Schema):
    _id = fields.Str(required=True, error_messages={'required': 'name is required.'})

class Uuid(Schema):
    valeuruuid = fields.UUID()