
"""
    Base class for every data importer
    @authors Dominic Létourneau
    @date 18/04/2018

"""

import threading
from libopenimu.tools.timing import timing


@timing
def load_worker(importer, filename):
    print('load_worker starting')
    result = importer.load(filename)
    importer.loaded_callback(result)
    print('load worker done')


class BaseImporter:
    def __init__(self):
        print('BaseImporter')

    def async_load(self, filename):
        print('will call load on importer with filename: ', filename)
        t = threading.Thread(target=load_worker, args=[self, filename])
        t.start()
        return t

    def load(self, filename):
        print('Nothing to do in BaseImporter.load')
        pass

    def loaded_callback(self, result):
        print('loaded callback result len', len(result))
