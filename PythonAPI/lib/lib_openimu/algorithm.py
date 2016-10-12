#Author : Remi Drolet
#Base Class for all Algorithm in the algos subfolder
#USAGE :
#   -Make sure that the name of the module and the name of the class in the module is exactly the same

from resources import getRecords

class Algorithm(object):

    def __init__(self): pass
    # load function :
    #   This method should be called first to load the data
    def load(self,uudi):
        raise NotImplementedError('Implement this function')

    def run(self):
        raise NotImplementedError('Implement this function')


