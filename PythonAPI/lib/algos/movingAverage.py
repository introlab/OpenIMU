# -*- coding: utf-8 -*-
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
from math import sqrt
import numpy as np
#import matplotlib.pyplot as plt

class stepCounter(Algorithm):
    #This is the base threshold between each peak on the x axis
    spacing = 14

    def __init__(self):
        super(stepCounter, self).__init__()
        self.description = "Moyenne Mobile"
        self.author = "L'équipe d'OpenIMU"
        self.name = "moyenne mobile"
        self.filename = "movingAverage"
        self.details = "Calcul la moyenne sur une plage."
        self.dispType = "2d_graph"
        self.params.uuid = 0
        self.infos.uuid = "Identifiant unique d'un enregistrement"
        self.possible.uuid = "Un identifiant ObjectId"

    def run(self):
        """
        Algorithme pour  un compteur de pas
        Étape 1 : Importer les données de l'enregistrement provenant de la base de données
        Étape 2 : Calculater la moyenne mobile sur les données
        Étape 3 : Identifier les sommets séparer par un certain intervale et une limite
        :return: Rien par défaut, mais self.ouput et quand même utile à retourner
        """
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': str(self.params.uuid)})
        data, errors = schema.dump(ref)

        if len(data)/2 < self.spacing : self.spacing = round(len(data)/2 - 1)

        return self.moving_average(data,self.spacing)


    def moving_average(self,data, N):
        magnetude = [sqrt(i.get('x')**2 + i.get('y')**2 + i.get('z')**2)
                         for i in data]

        V = np.ones((N,))/N

        result = np.convolve(magnetude, V, mode='valid')[(N-1):]
        return result
