from algorithm import Algorithm
class AlgoTest(Algorithm):
    def __init__(self):
        """
        At initialization, call the super of the algorithm with this syntax:
         super(AlgoName,self).__init__()
        Then, define the values of self.infos.description and self.infos.author.
        Then, initialize the keys of self.params with this synthax:
         self.params.foo = 0
         self.params.bar = "A string"
        Those are the default values of the parameters. If the url doesn't find those keys in the url, then those values
        will be used.
        """
        super(AlgoTest,self).__init__()

        self.description = "Algo Test Algorithm"
        self.author = "Remi Drolet"
