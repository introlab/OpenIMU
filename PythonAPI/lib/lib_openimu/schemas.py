from marshmallow import fields, Schema, post_dump
import math

class Record(Schema):
    name = fields.Str()
    date = fields.Date()
    format = fields.Str()
    _id = fields.UUID()

class Sensor(Schema):
    x = fields.Float(as_string = False)
    y = fields.Float(as_string = False)
    z = fields.Float(as_string = False)
    t = fields.Int(as_string = False)
    ref = fields.UUID()

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