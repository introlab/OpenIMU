from scipy.fftpack import fft, ifft
import numpy as np
def run(a):
    x = np.array(a)
    y = fft(x)
    return y
def invert(a):
    x = ifft(a)
    return x
