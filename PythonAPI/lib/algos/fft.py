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
        self.description = "Fast Fourier Transform Algorithm"
        self.author = "OpenIMU Team"
        self.details = "<B>NOT WORKING</B>"
        self.params.uuid = 0
        self.infos.uuid = "Unique Id of the data"


    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        x = np.array(self.data)
        y = np.fft(x)
        return y

