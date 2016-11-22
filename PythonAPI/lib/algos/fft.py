import numpy as np
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
import json
import base64

class fft(Algorithm):
    """
    Please check the Algorithm File for information about how to code or use algorithm Object
    """
    def __init__(self):
        super(fft,self).__init__()
        self.description = "Fast Fourier Transform Algorithm"
        self.author = "OpenIMU Team"
        self.details = "FFT on each dimensions though time."
        self.params.uuid = 0
        self.infos.uuid = "Unique Id of the data"
        self.params.bins = 1024
        self.infos.bins = "Number of bins per dimensions. Default is 1024"


    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        x = [snap.get('x') for snap in self.data]
        y = [snap.get('y') for snap in self.data]
        z = [snap.get('z') for snap in self.data]

        nbBins = self.params.bins
        x = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(x,nbBins)]
        y = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(y,nbBins)]
        z = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(z,nbBins)]

        self.output.result = {'x':x,'y':y,"z":z}
        return self.output

