# -*- coding: utf-8 -*-
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
        self.description = "Coquille vide d'un algorithme"
        self.author = "L'éuipe d'OpenIMU"
        self.name = "Example"
        self.filename = "template"
        self.details = "Se fichier est la base de la structure d'un algorithme."

        #Params initialization
        self.params.uuid = 0
        self.infos.uuid = "Identifiant unique d'un enregistrement"

        #After __init__, the params are passed throught a URL parser by algorithm.load()

    def run(self):
        """
            Coquille vide d'un algorithme
                Donne un exemple de la façon de charger des données provenant de la base de données
                :return: self.output
        """
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': str(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        #self.output Est l'endroit où votre résultats devrais être renvoyer.
        #Vous pouvez ajouter autant de sous-résultat tant que les résultat sont afficher dans le JSON et qu'ils ont un nom différent
        #EX :   self.output.result1 = 1
        #       self.output.result2 = {"test":"Hello World"}
        return self.output