#Does the work
import random
from predpreymap import Map
import copy
from critter import Critter
import critter
import mutate

try:
    import psyco
    psyco.full()
except ImportError:
    import sys
    sys.stderr.write("Install Python Psyco For Increased Performance.\nAlgo\n")

best_pred = {}
best_prey = {}

DEFAULT_SETTINGS = {"mapsize":20, "vegpercent":0.05, "preypercent":0.02, "predpercent":0.01, "sight":10, "plantbites":3, "maxhunger":20, "pdfpercent":0.01, "inputranges":(10,7,10,7,10,7,20), "mutationincrement":0.3}

def reverse(direction):
    if direction == 0:
        return 0
    if direction <= 3:
        direction += 3
    else:
        direction -= 3
    return direction

def left(direction):
    if direction == 0:
        return 0
    if direction == 1:
        return 6
    else:
        return direction - 1

def right(direction):
    if direction == 0:
        return 0
    if direction == 6:
        return 1
    else:
        return direction + 1

#This converts for example "Move towards predator" to "Move left"
#sensorydata holds the data from the map
#move holds a direction like "Move towards predator"
def directionConverter(sensorydata):
    toPred = sensorydata[1]
    toPrey = sensorydata[3]
    toPlant = sensorydata[5]

    toPred = 0 if toPred == None else toPred
    toPrey = 0 if toPrey == None else toPrey
    toPlant = 0 if toPlant == None else toPlant
    allpossiblemoves = [toPred,  toPrey,  toPlant,
     reverse(toPred), reverse(toPrey), reverse(toPlant),
     left(toPred),    left(toPrey),    left(toPlant),
     right(toPred),   right(toPrey),   right(toPlant), 0  ]
    return allpossiblemoves

def getAMove(critter, world, settings):
        if world.getCritterXY(critter) == None:
                raise Exception("Critter isn't on the map!")
        senses = world.getSensoryData(critter, settings["sight"])
        dirconv = directionConverter(senses)
        validmoves = list(set(dirconv))
        while len(validmoves) > 0:
                destinationTile = None
                directionMove = -1
                while destinationTile == None or directionMove == -1 or directionMove == None or directionMove not in validmoves:
                        move = critter.getMove(senses)
                        directionMove = dirconv[move]
                        destinationTile = world.getCritterDest(critter, directionMove)
                if directionMove in validmoves:
                        validmoves.remove(directionMove)
                else:
                        raise Exception("%d not in %s"%(directionMove, validmoves))
                yield destinationTile, directionMove

def preyMakeMove(prey, settings, world):
        for destinationTile, directionMove in getAMove(prey, world, settings):
                critterOnTile = world.getCritterAt(destinationTile)
                if critterOnTile == None:
                        world.moveCritter(prey, directionMove)
                        if world.isPlant(destinationTile): 
                                #isPlant bites for me
                                prey.setStatus("hunger", 0)
                        return
                elif critterOnTile.type == critter.PREY:
                        continue
                elif critterOnTile.type == critter.PREDATOR:
                        world.removeCritter(prey)
                        critterOnTile.setStatus("hunger", 0)
                        return
                else:
                     raise Exception("There is a prey case that is not accounted for: " + critterOnTile)

def predMakeMove(pred, settings, world):
        for destinationTile, directionMove in getAMove(pred, world, settings):
                critterOnTile = world.getCritterAt(destinationTile)
                if critterOnTile == None:
                        world.moveCritter(pred, directionMove)
                        return
                elif critterOnTile.type == critter.PREY:
                        world.removeCritter(critterOnTile)
                        pred.setStatus("hunger", 0)
                        return
                elif critterOnTile.type == critter.PREDATOR:
                        continue                        
                else:
                     raise Exception("There is a predator case that is not accounted for: " + critterOnTile)

def calcscore(x):
    predpdf, pred_mask = x[0]
    preypdf, prey_mask = x[1]

    settings = x[2] if len(x) > 2 else DEFAULT_SETTINGS
    mapsize = settings["mapsize"] if "mapsize" in settings else 20
    vegpercent = settings["vegpercent"] if "vegpercent" in settings else 0.5
    plantbites = settings["plantbites"] if "plantbites" in settings else 3
    preypercent = settings["preypercent"] if "preypercent" in settings else 0.1
    predpercent = settings["predpercent"] if "predpercent" in settings else 0.1
    maxhunger = settings["maxhunger"] if "maxhunger" in settings else 20
    sight = settings["sight"] if "sight" in settings else 20

    hooker = x[3] if len(x) > 3 else None

    world = Map(mapsize, vegpercent,plantbites)
    for _ in range(int((mapsize**2)*predpercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(predpdf, pred_mask, critter.PREDATOR))

    for _ in range(int((mapsize**2)*preypercent)):
        world.setCritterAt(world.getRandomUntakenTile(), Critter(preypdf, prey_mask, critter.PREY))

    score = 0
    while len(world.getPredators()) > 0 and len(world.getPreys()) > 0:
        score += 1
        critters = world.getPredators() + world.getPreys()
        random.shuffle(critters)
        if critters == None:
                raise Exception("Critter cannot be none!!")
        for c in critters:
                if world.getCritterXY(c) == None: continue
                c.incrementStatus("hunger", 1)
                if c.type == critter.PREY:
                        preyMakeMove(c, settings, world)
                elif c.type == critter.PREDATOR:
                        predMakeMove(c, settings, world)
                else:
                        raise Exception("Something that is not a critter is in the map: " + c)
                if c.getStatus("hunger") >= settings["maxhunger"] and world.getCritterXY(c) != None:
                        world.removeCritter(c)
                if hooker != None:
                        hooker(world, score)

    if hooker != None:
        hooker(world, score)

    return score

def __printProgress(num, total):
    width = 40
    s = "%d/%d [" % (num, total)
    completecount = (float(num)/total)*40
    for i in range(40):
        if i < completecount:
            s = s + "="
        else:
            s = s + "-"
    s = s + "]\r"
    print s,
    import sys
    sys.stdout.flush()

def __clearProgress():
    print (" "*80) + "\n",
    import sys
    sys.stdout.flush()


def roundprogress(map, score):
        pass
        #print("Progress at %s" % score)
    #   for critter in map.critters: print("%s at %s hunger:%s" % (critter.type, map.critters[critter], critter.getStatus("hunger")))


def getCalcScoreArgs(preds, preys, bpred, bprey, settings):
    bpreyclones = [ (bprey, {}) for _ in preds]
    bpredclones = [ (bpred, {}) for _ in preys]
    settingsclones = [settings] * max(len(preds),len(preys))
    preds = zip( [bpred]*len(preds), preds)
    preys = zip( [bprey]*len(preys), preys)
    predArgs = zip( preds, bpreyclones, settingsclones[:len(preds)])
    preyArgs = zip(bpredclones, preys, settingsclones[:len(preys)])
    return predArgs, preyArgs

def getResults(predArgs, preyArgs):
    return map(calcscore, predArgs) if len(predArgs) > 1 else [0], map(calcscore, preyArgs) if len(preyArgs) > 1 else [0]

def getMultiProcessedResults(predArgs, preyArgs):
    #Now comes the multiprocessing magic...
    import multiprocessing
    from multiprocessing import Pool
    pool = Pool()
    predResults = pool.map_async(calcscore, predArgs, 20000) if len(predArgs) > 1 else None
    preyResults = pool.map_async(calcscore, preyArgs, 20000) if len(preyArgs) > 1 else None
    return predResults.get() if predResults else [0], preyResults.get() if preyResults else [0]


def mutate(gens, pred_clones_per_gen, prey_clones_per_gen, settings=DEFAULT_SETTINGS, progress=__printProgress): 
    global best_pred, best_prey, calcscore
    import mutate

    for i in range(gens):
        progress(i, gens) #Update the progress

        #creats the masks. Masks hold the difference between the original critter and the new mutated one.
        predmasks, preymasks = mutate.createMasks(((best_pred, pred_clones_per_gen), (best_prey, prey_clones_per_gen)), settings)

        predmasks.append({}) #This is how we add the best_pred to the mix. The best_pred has an empty mask
        preymasks.append({}) #This is how we add the best_prey to the mix. The best_prey has an empty mask

        predArgs, preyArgs = getCalcScoreArgs(predmasks, preymasks, best_pred, best_prey, settings)

        #predpdfscores, preypdfscores = getMultiProcessedResults(predArgs, preyArgs)
        predscores, preyscores = getResults(predArgs, preyArgs)

        #Pickout the best mask
        best_pred_mask = predmasks[predscores.index(max(predscores))]
        best_prey_mask = preymasks[preyscores.index(max(preyscores))]

        #Merge the mask into the best pdf
        for k,v in best_pred_mask.iteritems(): best_pred[k] = v
        for k,v in best_prey_mask.iteritems(): best_prey[k] = v


if __name__ == "__main__":
    gens = input("How many generations?")
    preds = input("How many predator clones per generation?")
    preys = input("How many preys clones per generation?")
    mutate(gens, preds, preys)
    __clearProgress()
