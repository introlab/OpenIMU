from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
import datetime
import numpy as np

class frequencyfilter(Algorithm):
    #Feel free to check the algorithm.py in lib_openimu for additionnal info.

    class Filter(object):
        f = 0.1
        b = 0.1
        n = None
        h = None
        def __init__(self,f = 0.1,b = 0.1):
            self.f = f
            self.b = b
            self._create_filter()

        def _create_filter(self):
            N = int(np.ceil((4 / self.b)))
            if not N % 2: N += 1  # Make sure that N is odd.
            self.n = np.arange(N)
            # Compute the filter
            self.h = np.sinc(2 * self.f * (self.n - (N - 1) / 2.))
            # Apply window.
            self.h *= np.blackman(N)
            # Normalize to get unity gain.
            self.h /= np.sum(self.h)

        def apply(self,data):
            return np.convolve(data,self.h)

    class HighPass(Filter):
        def __init__(self,f = 0.1, b = 0.1):
            super(self.__class__, self).__init__(f,b)
            # Spectral inversion for high pass filter from lowpass filter
            self.h = -self.h
            self.h[(int(np.ceil((4 / self.b))) - 1) / 2] += 1

    class LowPass(Filter):
        pass

    valid_type = ["lowpass","highpass"]

    def __init__(self):
        super(self.__class__, self).__init__()

        #Default information for the UI.
        self.description = "Frequency filter for data"
        self.author = "OpenIMU Team"
        self.details = "Can be used for low-pass, high-pass, band-pass and band-reject filter"

        #Params initialization
        self.params.uuid = 0
        self.infos.uuid = "Unique ID for the database"

        self.params.type = None
        self.infos.type = "Type of filter : lowpass or highpass"

        self.params.cutoff = 0.1
        self.infos.cutoff =  "Cutoff frequency as a fraction of the sampling rate (between 0 and 0.5)"

        self.params.transition = 0.1
        self.infos.transition = "Transition band, as a fraction of the sampling rate (Between 0 and 0.5)"

        #After __init__, the params are passed throught a URL parser by algorithm.load()

    def before_run(self):
        self.output.runtime_start = str(datetime.datetime.now())
        if self.params.type not in self.valid_type:
            raise NameError("Type <" + self.params.type + "> not in " + str(self.valid_type))

    def run(self):
        """
            Template Algorithm
                Show an example of how to load the data from the database
                :return: self.output
        """
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        filter = None
        if self.params.type == "lowpass":
            print "Hello"
            filter = self.LowPass()


        #self.output is were you return the result.
        #You can add as much subresult as you want, as long as the result is shown in JSON and that they have different name
        #EX :   self.output.result1 = 1
        #       self.output.result2 = {"test":"Hello World"}
        return self.output



