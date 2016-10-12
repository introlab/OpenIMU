from math import sqrt
from bson.objectid import ObjectId
import numpy
from algorithm import Algorithm
from  lib_openimu import schemas
import resources


class activityTracker(Algorithm):
    def __init__(self):
        self.data = None
        pass
    def test(self):
        return {'Hello' : 'world'}
    def load(self,database,request):
            uuid = request.args.get('uuid')
            schema = schemas.Sensor(many=True)
            ref = database.db.accelerometres.find({'ref': ObjectId(request.args.get('uuid'))})
            acc, errors = schema.dump(ref)

            x = []
            localmax = max(acc,key=lambda item:item['t'])['t']/1000.
            for snap in acc:
                if (localmax - snap['t']/1000.) < 100000000:
                    x.append(snap)

            self.data =x
            return self.data
    def run(self):
        x = [sqrt(snap.get('x') ** 2 + snap.get('y') ** 2 + snap.get('z') ** 2)
             for snap in self.data]
        diff = numpy.diff(x)
        total = 0
        for n in diff:
            if abs(n) > 20:
                total = total + 1

        self.output['activitypercent'] = 100*total/len(diff)
        print self.output
        return self.output