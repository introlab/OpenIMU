"""
    This is a simple matlab .mat data importer.
"""

import scipy.io as sio


def load_mat_file(filename):
    print("loading: ", filename)
    mat_contents = sio.loadmat(filename)
    return mat_contents
