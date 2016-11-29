from timeit import default_timer as timer
import datetime
import warnings

class Algorithm(object):
    """
    Author : Remi Drolet
    Base Class for all Algorithm in the algos subfolder
    IMPORTANT :
        -Make sure that the name of the module and the name of the class in the module is exactly the same
        -ex:
            Name file : AlgoTest.py
            Class AlgoTest(Algorithm):
            ...
    PARAM :
        -Call the _init of the super(algoname,self).__init__
        -Define the self.description and self.author
        -Params are initialize in the __init__ of your class, you can have as much params as you like
        ex:
            File name : AlgoTest.py
            class AlgoTest(Algorithm):
                def __init__(self):
                    super(AlgoTest, self).__init__()
                    self.description = "Algo Test Algorithm"
                    self.author = "OpenIMU Team"
                    self.params.uuid = 0
    USAGE :
        -To call any Algo, you need to make a HTTP GET Request to the Python API.
        -According to the default resources.py, you need to call:
            localhost:5000/algo?filename=AlgoTest&uuid=example8e0034624ac0d90d4
        -The algo resource will do three things :
            -Create an Algorithm defined by the the filename url argument
            -Call Algorithm.load function which parse the url to Algorithm.params
            -Call Algorithm.run function, where you define how the Algorithm . Add your result to the Algorithm.output
             property.
            -Everything in Algorithm.output is returned by the HTTP GET Request.

    """

#Property List
    _params = {}
    _infos = {}
    _output = {}
    _request = {}
    _database = None


    _information = ""
    _author = ""
    _details = ""

# Property Getter and Setter
    @property
    def timer(self):
        temp = timer()
        diff = temp - self._time
        self._time = timer()
        return diff

    @property
    def information(self):        return self._information
    @information.setter
    def information(self, value):        self._information = value

    @property
    def author(self):        return self._author
    @author.setter
    def author(self, value):        self._author = value

    @property
    def details(self):        return self._details
    @details.setter
    def details(self, value):        self._details = value

    @property
    def database(self):        return self._database
    @database.setter
    def database(self,db):        self._database=db

    @property
    def infos(self):        return self._infos
    @infos.setter
    def infos(self, value):        self._infos = value

    @property
    def params(self):        return self._params
    @params.setter
    def params(self, value):        self._params = value

    @property
    def request(self):        return self._request
    @request.setter
    def request(self, value):        self._request = value

    @property
    def output(self):        return self._output
    @output.setter
    def output(self, value):        self._output = value

    def __init__(self):
        """
        At initialization, call the super of the algorithm with this syntax:
         super(AlgoName,self).__init__()
        Then, define the values of self.description and self.author.
        Then, initialize the keys of self.params with this synthax:
         self.params.foo = 0
         self.params.bar = "A string"
        Those are the default values of the parameters. If the url doesn't find those keys in the url, then those values
        will be used.
                """
        self._time = timer()
        self._infos = Dictionnary()
        self._params = Dictionnary()
        self._output = Dictionnary()
        self._request = Dictionnary()
        pass

    def before_run(self):
        self.output.runtime_start = str(datetime.datetime.now())
        warnings.warn('default Implementation of before_run')

    # This function need to be overloaded by the algorithm.
    def after_run(self):
        self.output.request = {}
        for key in self.request:
            self.output.request[key] = self.request[key]
        self.output.runtime = self.timer
        warnings.warn('default Implementation of after_run')

    def load(self,args = {}):
        """
        load function :
           This method should be called first to parse the request.args arguments
           Unused request keys are ignored
        :param args: Arguments of the HTTP Request
        :return: The self.params object that contain every Args parsed of the URL
        """

        for key in self.params:
            temp = args.get(key).encode('utf8')
            try:
                x = int(temp)
            except (TypeError, ValueError):
                x = temp
            self.params[key] = x

        for key in args:
            self.request[key] = args.get(key)

        return self.params

    def run(self):
        """
        This is where you define how your algorithm operate.
        :return: Nothing by default, but don't forget to put your result in self.output
        """
        raise NotImplementedError('Implement this function')

class Dictionnary(dict):
    """
    Default Object for Parameters.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__



