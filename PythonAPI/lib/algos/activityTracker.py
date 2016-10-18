from math import sqrt
from bson.objectid import ObjectId
import numpy
from algorithm import Algorithm
from  lib_openimu import schemas


class activityTracker(Algorithm):
    data = None
    def test(self):
        return {'Hello' : 'world'}

    def __init__(self):
        super(activityTracker,self).__init__()
        self.params.threshold = 0
        self.params.uuid = 0

    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        acc, errors = schema.dump(ref)
        self.data = acc
        x = [sqrt(snap.get('x') ** 2 + snap.get('y') ** 2 + snap.get('z') ** 2)
             for snap in self.data]
        diff = numpy.diff(x)
        total = 0
        for n in diff:
            if abs(n) > self.params.threshold:
                total = total + 1

        return 100*total
