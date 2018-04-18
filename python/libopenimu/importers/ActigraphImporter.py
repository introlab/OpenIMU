
"""
    Actigraph data importer
    @authors Dominic Létourneau
    @date 18/04/2018

"""

from libopenimu.importers.BaseImporter import BaseImporter
import libopenimu.importers.actigraph as actigraph


class ActigraphImporter(BaseImporter):
    def __init__(self):
        super().__init__()
        print('Actigraph Importer')

    def load(self, filename):
        print('ActigraphImporter loading:', filename)
        result = actigraph.gt3x_importer(filename)
        return result
