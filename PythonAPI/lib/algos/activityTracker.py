from math import sqrt
from bson.objectid import ObjectId
import numpy
from algorithm import Algorithm
from  lib_openimu import schemas


class activityTracker(Algorithm):
    data = None

    def __init__(self):
        super(activityTracker,self).__init__()

        self.description = "Activity Time Tracker Algorithm"
        self.author = "OpenIMU Team"

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

        self.output.result = 100*total/len(diff)
        self.output.threshold = self.params.threshold
        self.output.maximum = max(diff)
        self.output.minimum = min(diff)
        self.output.size = len(diff)
        return True
