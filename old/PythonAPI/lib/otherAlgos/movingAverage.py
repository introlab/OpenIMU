# -*- coding: utf-8 -*-
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
from math import sqrt
import numpy as np
#import matplotlib.pyplot as plt

class movingAverage(Algorithm):
    #This is the base threshold between each peak on the x axis
    spacing = 200
    
    def __init__(self):
        super(movingAverage, self).__init__()
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

        self.output.result = self.moving_average(data,self.spacing)

        return self.output


    def moving_average(self,data, N):

        V = np.ones((N,))/N

        x = np.convolve([i.get('x') for i in data], V, mode='valid')[(N-1):]
        y = np.convolve([i.get('y') for i in data], V, mode='valid')[(N-1):]
        z = np.convolve([i.get('z') for i in data], V, mode='valid')[(N-1):]

        temp = {"accelerometres": []}
        for i in range(1, min(len(x), len(y), len(z))):
            value = {"t": i, "x": x[i], "y": y[i], "z": z[i]}
            temp["accelerometres"].append(value)

        return temp
