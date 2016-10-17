#Author : Remi Drolet
#Base Class for all Algorithm in the algos subfolder
#USAGE :
#   -Make sure that the name of the module and the name of the class in the module is exactly the same
#PARAM :
#

from resources import getRecords
import json

class Algorithm(object):
    _params = None
    _database = None

    @property
    def database(self):
        return self._database
    @database.setter
    def database(self,db):
        self._database=db

    @property
    def params(self):
        return self._params
    @params.setter
    def param(self, value):
        self._params = value

    def __init__(self):
        self._params = Params()
        pass
    # load function :
    #   This method should be called first to load the data
    def load(self,args = {}):
        for key in self.params:
            self.params[key] = args.get(key)
        print self.params
        return 1
        #raise NotImplementedError('Implement this function')

    def run(self):
        raise NotImplementedError('Implement this function')

class Params(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    #def __init__(self,*args, **kwargs):
    #    super(Params, self).__init__(*args, **kwargs)
    #    self.__dict__ = self


#}

