import numpy as num
import lib_openimu.resources as ressource

class Input_Database:
    n = num.array([0])
    def __init__(self):
        None
    def loadArray(self,a):
        print(" Loading Input Array")
        self.n = num.array(a)
    def getInput(self):
        return self.n
