"""
 Will contain sqlite driver
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import libopenimu.models.Recordset

class DataSet:
    def __init__(self):
        self.name = None
        self.description = None
        self.creation_date = None
        self.upload_date = None
        self.author = None
        self.recordSets = []
