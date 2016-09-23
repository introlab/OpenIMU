from Tracker import input_database as input

class Activity_Tracker:
    newInput = None
    def __init__(self):
        print("INIT Activity Time Tracker")
        self.newInput = input.Input_Database()
    def loadInput(self,input):
        self.newInput.loadArray(input)
    def getInput(self):
        return self.newInput.getInput()