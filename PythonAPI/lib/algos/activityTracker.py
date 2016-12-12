# -*- coding: utf-8 -*-
from math import sqrt
from bson.objectid import ObjectId
import numpy
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas


class activityTracker(Algorithm):
    """
    Activity Tracker Algorithm
    Author : OpenIMU Team

    Simple Activity Tracker algorithm that check the accelerometer data and calculate the
    percentage of the magntude of the data that is higher than a threshold
    """
    data = None

    def __init__(self):
        super(activityTracker,self).__init__()

        self.description = "Algorithme du temps d'activité "
        self.author = "L'équipe d'OpenIMU"
        self.name = "Temps d'activité"
        self.filename = "activityTracker"
        self.details = (
                        "À partir des données de l'enregitrement on calcule la magnitude sur les données brutes. On resort le pourcentage des données qui dépasse un seuil"
                        )

        self.params.uuid = 0
        self.infos.uuid = "Identifiant unique d'un enregistrement"
        self.possible.uuid = "Un identifiant ObjectId"


    def run(self):
        """
        Algorithm du temps d'activité
        Étape 1 : Importer les données provenant de la base de données
        Étape 2 : Calculer la magnitude des données
        Étape 3 : Calculer la différence de la magnitude des données
        Étape 4 : Calcule le pourcentage de la différence de la magnitude qui dépasse le seuil donné en paramètre
        :return: self.output
        """
        threshold = 100
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': self.params.uuid})
        acc, errors = schema.dump(ref)
        self.data = acc

        x = [sqrt(snap.get('x') ** 2 + snap.get('y') ** 2 + snap.get('z') ** 2)
             for snap in self.data]
        diff = numpy.diff(x)

        total = 0
        for n in diff:
            if abs(n) > threshold:
                total = total + 1

        self.output.result = 100*total/len(diff)
        self.output.threshold = threshold
        self.output.maximum = max(diff)
        self.output.minimum = min(diff)
        self.output.size = len(diff)
        self.output.execute_time = self.timer
        return self.output.result

