# -*- coding: utf-8 -*-
import numpy as np
from lib_openimu.algorithm import Algorithm
from lib_openimu import schemas
from bson.objectid import ObjectId
import json
import base64

class fft(Algorithm):
    """
    Please check the Algorithm File for information about how to code or use algorithm Object
    """
    def __init__(self):
        super(fft,self).__init__()
        self.description = "Transformé de Fourrier rapide"
        self.author = "L'équipe d'OpenIMU"
        self.name = "FFT"
        self.filename = "fft"
        self.details = "Fait la FFT sur chaque dimension, à travers le temps."

        self.params.uuid = 0
        self.infos.uuid = "Identifiant unique d'un enregistrement"
        self.possible.uuid = "Un identifiant ObjectID"

        self.params.bins = 1024
        self.infos.bins = "Nombre de columnes par dimensions."
        self.possible.bins = "Un chiffre de 1 à 2*N"

    def run(self):
        schema = schemas.Sensor(many=True)
        ref = self.database.db.accelerometres.find({'ref': ObjectId(self.params.uuid)})
        self.data, errors = schema.dump(ref)

        x = [snap.get('x') for snap in self.data]
        y = [snap.get('y') for snap in self.data]
        z = [snap.get('z') for snap in self.data]

        nbBins = self.params.bins
        x = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(x,nbBins)]
        y = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(y,nbBins)]
        z = [{'r':snap.real,'i':snap.imag} for snap in np.fft.fft(z,nbBins)]

        temp = {"accelerometres": []}
        for i in range(1, min(len(x), len(y), len(z))):
            value = {"x": x[i], "y": y[i], "z": z[i]}
            temp["accelerometres"].append(value)

        self.output.result = {"accelerometres": temp["accelerometres"]}

        return self.output

