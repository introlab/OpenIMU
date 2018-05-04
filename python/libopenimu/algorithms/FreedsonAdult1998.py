from libopenimu.algorithms.BaseAlgorithm import BaseAlgorithmFactory


class FreedsonAdult1998Factory(BaseAlgorithmFactory):
    def __init__(self):
        super(BaseAlgorithmFactory, self).__init__()
        pass

    def create(self, params: dict):
        return None

    def params(self):
        return dict()

    def name(self):
        return 'FreedsonAdult1998Factory'


# Factory init
def init():
    return BaseAlgorithmFactory.register_factory(FreedsonAdult1998Factory())



