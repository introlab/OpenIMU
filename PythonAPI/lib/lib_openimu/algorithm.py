#Author : Remi Drolet
#Base Class for all Algorithm in the algos subfolder
#USAGE :
#   -Make sure that the name of the module and the name of the class in the module is exactly the same
#PARAM :
#

from resources import getRecords
import json,unicodedata

class Algorithm(object):
    _params = {}
    _output = {}
    _database = None

    _information = ""
    _author = ""

    @property
    def information(self):
        return self._information

    @information.setter
    def information(self, value):
        self._information = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def database(self):
        return self._database
    @database.setter
    def database(self,db):
        self._database=db

    @property
    def infos(self):
        return self._infos
    @infos.setter
    def infos(self, value):
        self._infos = value

    @property
    def params(self):
        return self._params
    @params.setter
    def params(self, value):
        self._params = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    def __init__(self):
        """
        At initialization, call the super of the algorithm with this syntax:
         super(AlgoName,self).__init__()
        Then, define the values of self.infos.description and self.infos.author.
        Then, initialize the keys of self.params with this synthax:
         self.params.foo = 0
         self.params.bar = "A string"
        Those are the default values of the parameters. If the url doesn't find those keys in the url, then those values
        will be used.
                """
        self._params = Dictionnary()
        self._output = Dictionnary()
        pass
    # load function :
    #   This method should be called first to parse the request.args arguments
    #   Unused request keys are ignored
    def load(self,args = {}):
        for key in self.params:
            temp = args.get(key).encode('utf8')
            try:
                x = int(temp)
            except (TypeError, ValueError):
                x = temp
            self.params[key] = x
        return self.params

    def run(self):
        raise NotImplementedError('Implement this function')

class Dictionnary(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

class Information(object):
    def __init__(self):
        pass


