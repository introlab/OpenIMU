from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
from math import sqrt
import numpy as np

class template(Algorithm):
    #This is the basic template for all algorithm.
    #Feel free to check the algorithm.py in lib_openimu for additionnal info.
    def __init__(self):
        super(self.__class__, self).__init__()

        #Default information for the UI.
        self.description = "Template Algorithm"
        self.author = "OpenIMU Team"
        self.details = "You can copie this file to start a new Algo."

        #Params initialization
        self.params.uuid = 0
        self.infos.uuid = "Unique ID"

        #After __init__, the params are passed throught a URL parser by algorithm.load()

    def run(self):
        """
            Template Algorithm
                Show an example of how to load the data from the database
                :return: self.output
        """
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        #self.output is were you return the result.
        #You can add as much subresult as you want, as long as the result is shown in JSON and that they have different name
        #EX :   self.output.result1 = 1
        #       self.output.result2 = {"test":"Hello World"}
        return self.output