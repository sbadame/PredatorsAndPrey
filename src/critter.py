import numpy
import predpreyalgorithm as ppa

PREDATOR = "predator"
PREY = "prey"

#Give it a set of input sensory data, it outputs a move.
#Naive implementation that currently just runs on python
class Critter:

    def __init__(self, mask, type="No type defined"):
        self.choices = ppa.getSetting("choices")
        self.status = {"hunger":0}
        self.type = type
        self.pdfmatrix = ppa.best_pred if self.type == PREDATOR else ppa.best_prey
        self.mask = mask

    #
    # Given a set of inputs this function will return
    # All of the moves that should be attemped in the
    # order that they should be attempted
    #
    def getMoves(self, senses):
        pdf = self.getHistogram(senses).copy() #This is a numpy array
        moves = []
        while len(moves) < 7: #Keep going until the pdf is empty
            if pdf.sum() < 0 :
                raise Exception("Error sum < 0: pdf=%s, sum=%d " % (pdf, pdf.sum()) )
            if pdf.sum() == 0:
                moves += filter(lambda m: m not in moves, range(7) )
                break
            r = numpy.random.randint(pdf.sum()) #Pick a random number
            sum = 0 #Track how high we are
            for i,probability in enumerate(pdf): #For every i from 0 -> len(pdf) and every probability in the pdf
                sum += probability
                if r < sum:
                    moves.append(i)
                    pdf[i] = 0
                    break
        return moves

    def generatePDF(self):
        return numpy.random.random_integers(low=1,high=255,size=7).astype(numpy.uint8)

    def _getHungerChunk(self):
        hunger = self.status["hunger"]
        for i, chunk in enumerate(ppa.getSetting("hungerchunks")):
            if hunger <= chunk:
                return i
        return len(ppa.getSetting("hungerchunks"))

    def getHistogram(self, senses):
        input = senses + (self._getHungerChunk(),)
        if input not in self.mask:
            if input not in self.pdfmatrix:
                pdf = self.generatePDF()
                self.pdfmatrix[input] = pdf
                return pdf
            else:
                return self.pdfmatrix[input]
        else:
            return self.mask[input]

    def getStatus(self, name):
        return self.status[name]

    def setStatus(self, name, value):
        self.status[name] = value

    def incrementStatus(self, name, value):
        self.status[name] += value

    def resetStatus(self):
        for key in self.status:
                self.status[key] = 0
        self.status["hunger"] = 0

if __name__ == "__main__":
    s = Critter({},{}, PREDATOR)
    input = (3, 4, 5)
    s.getMove(input)
#    s.save(open("critters/deniz.predator", "w"))

    c = Critter({}, {}, PREY)
#    c.load(open("critters/deniz.predator", "r"))

    c.setStatus("hunger", c.getStatus("hunger")/2)
    c.getMove((3, 4, 5))
    print("Histogram: %s" % c.getHistogram((3,4,5)))

    #for m in c.getMutations(2, 0.5, (6, 6, 6), 0.3): print(m.pdfmatrix)
    results = [ 0 for _ in range(c.choices)]
    for _ in range(10000):
        r = c.getMove(input)
        results[r] = results[r] + 1
    for x in results: print(x/100.0) 

