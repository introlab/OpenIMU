from scipy.fftpack import fft, ifft
import numpy as np
from algorithm import Algorithm

class Fft(Algorithm):
    def __init__(self):
        pass
    def run(self,a):
        x = np.array(a)
        y = fft(x)
        return y
    def invert(self,a):
        x = ifft(a)
        return x
