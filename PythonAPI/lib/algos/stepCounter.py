from algorithm import Algorithm
from  lib_openimu import schemas
from bson.objectid import ObjectId
from math import sqrt
import numpy as np





class stepCounter(Algorithm):
    def __init__(self):
        super(stepCounter, self).__init__()
        self.description = "Algo Test Algorithm"
        self.author = "OpenIMU Team"

        self.params.uuid = 0
        self.params.windowsize = 10

    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        data, errors = schema.dump(ref)

        filtereddata = self.moving_average(data)
        peaks = self.find_peaks(filtereddata,spacing = self.params.windowsize)

        # If you have imported matplotlib, you can decomment the following section. It block the cpu.
        #t = np.linspace(0, 1, len(filtereddata))
        #plt.plot(t,filtereddata)
        #plt.plot(t[peaks],filtereddata[peaks],'ro')
        #plt.show()
        
        self.output.result = len(peaks)

        return self.output

    def moving_average(self,data):
        magnetude = [sqrt(i.get('x')**2 + i.get('y')**2 + i.get('z')**2)
                         for i in data]
        N = self.params.windowsize
        return  np.convolve(magnetude, np.ones((N,))/ N,mode='valid')[(N-1):]

    def find_peaks(self,data,spacing = 1, limit = None):

        """Finds peaks in `data` which are of `spacing` width and >=`limit`.
        :param data: values
        :param spacing: minimum spacing to the next peak (should be 1 or more)
        :param limit: peaks should have value greater or equal
        :return:
        """
        len = data.size
        x = np.zeros(len + 2 * spacing)
        x[:spacing] = data[0] - 1.e-6
        x[-spacing:] = data[-1] - 1.e-6
        x[spacing:spacing + len] = data
        peak_candidate = np.zeros(len)
        peak_candidate[:] = True
        for s in range(spacing):
            start = spacing - s - 1
            h_b = x[start: start + len]  # before
            start = spacing
            h_c = x[start: start + len]  # central
            start = spacing + s + 1
            h_a = x[start: start + len]  # after
            peak_candidate = np.logical_and(peak_candidate, np.logical_and(h_c > h_b, h_c > h_a))

        ind = np.argwhere(peak_candidate)
        ind = ind.reshape(ind.size)
        if limit is not None:
            ind = ind[data[ind] > limit]
        return ind

