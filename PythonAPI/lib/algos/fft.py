import numpy as np
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId

class fft(Algorithm):
    """
    Please check the Algorithm File for information about how to code or use algorithm Object
    """
    def __init__(self):
        super(fft,self).__init__()
        self.description = "Fast Fourrier Transform Algorithm"
        self.author = "OpenIMU Team"

        self.params.uuid = 0
        self.infos.uuid = "Unique Id of the data"


    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        x = [snap.get('x') for snap in self.data]
        xArray = np.array(x)
        fftx = np.fft.fft(xArray)
        array = np.array.tostring
        return self.output

