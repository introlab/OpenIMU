from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
from math import sqrt
import numpy as np

class frequencyfilter(Algorithm):
    #This is the basic template for all algorithm.
    #Feel free to check the algorithm.py in lib_openimu for additionnal info.
    def __init__(self):
        super(self.__class__, self).__init__()

        #Default information for the UI.
        self.description = "Frequency filter for data"
        self.author = "OpenIMU Team"
        self.details = "Can be used for low-pass, high-pass, band-pass and band-reject filter"

        #Params initialization
        self.params.uuid = 0
        self.infos.uuid = "Unique ID for the database"

        #After __init__, the params are passed throught a URL parser by algorithm.load()

    class LowPassFilter(object):
        def __init__(self,fL = 0.1, bL = 0.1):
            fc = fL  # Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
            b = bL  # Transition band, as a fraction of the sampling rate (in (0, 0.5)).
            N = int(np.ceil((4 / b)))
            if not N % 2: N += 1  # Make sure that N is odd.
            n = np.arange(N)

            #Compute the filter
            self.h = np.sinc(2 * fc * (np.arange(N) - (N - 1) / 2.))
            #Apply the Blackman window
            #Source : http://www.ijcset.com/docs/IJCSET13-04-08-030.pdf
            self.h *= np.blackman(N)
            self.h /= np.sum(self.h)

        def apply(self,data):
            return np.convolve(data, self.h)





    def run(self):
        """
            Template Algorithm
                Show an example of how to load the data from the database
                :return: self.output
        """
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        #self.output is were you return the result.
        #You can add as much subresult as you want, as long as the result is shown in JSON and that they have different name
        #EX :   self.output.result1 = 1
        #       self.output.result2 = {"test":"Hello World"}
        return self.output