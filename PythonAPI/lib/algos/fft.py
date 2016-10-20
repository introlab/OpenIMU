#from scipy.fftpack import fft, ifft
import numpy as np
from algorithm import Algorithm

class fft(Algorithm):
    def __init__(self):

        pass
    def run(self,a):
        x = np.array(a)
        y = np.fft(x)
        return y

