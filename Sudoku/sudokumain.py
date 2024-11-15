import sudoku as s
import random
import copy


#gets given sudoku grid
def processGrid(filename):
    #Open file
    f = open(filename, "r")
    #Iterate through lines and store
    grid = []
    for i in f:
        for j in i:
            if (j != " " and j != "\n" and j != "!" and j != "-"):
                grid.append(j)
    n = 9
    return [grid[i:i+n] for i in range(0, len(grid), n)]



def main(popSize, grid):
    foundSolution = False
    currentCands = s.Pop()
    givenGrid = s.Board(processGrid(grid))
    currentCands.createPops(popSize,givenGrid)
    currentCands.popFitnessUpdate()
    count = 0
    tempCount = 0
    bestFVal = 0
    while foundSolution == False:
        # create candidates
        print("---------------------------------------------------------------------------------------------------------------------------")
        #evaluate candidate fitnesses
 


        #mutate based on some prerequisite.
        #given prerequisite - increase chance of mutation over time, until chance hits one
        #when the population has been optimised, mutate entire pop
        #f = all(element.fitness == currentCands.candidates[0].fitness for element in currentCands.candidates)



        #mutate 20% of best and 20% of worst with mutate2, add to list
        fittest = copy.deepcopy(currentCands.candidates[0:int(popSize/muteVal)])
        weakest = copy.deepcopy(currentCands.candidates[-int(popSize/muteVal):])
        for i in fittest:
            i.mutate2(givenGrid)
        for i in weakest:
            i.mutate2(givenGrid)

        newCands = fittest+weakest
        del currentCands.candidates[-len(newCands):]
        for i in newCands:
            currentCands.candidates.append(i)



        #select/order candidate
        currentCands.sort()


        #check if any are good, end loop and ...
        if currentCands.candidates[0].fitness == 0:
            print(f"it took {count} iterations")
            foundSolution = True
            break


        #check if 50% are same, randomise all except 1 if so
        fitnesses = []
        for i in currentCands.candidates:
            fitnesses.append(i.fitness)
        if fitnesses.count(fitnesses[0]) > len(fitnesses)/2 + 1:
            #randomise first half and second half
            fittest = copy.deepcopy(currentCands.candidates[0:int(popSize/2)-1])
            weakest = copy.deepcopy(currentCands.candidates[-int(popSize/2)+1:])
            combined = fittest + weakest
            del currentCands.candidates[-len(combined):]
            for i in combined:
                for j in range(5):
                    i.mutate3(givenGrid)
                currentCands.candidates.append(i)
            currentCands.sort()
        

            

        #breed candidates
        #get the best 20% of cands
        bestCands = currentCands.candidates[0:int(popSize/breedVal)]
        #remove worst 20% of cands

        currentCands.candidates = currentCands.candidates[0:4*int(popSize/breedVal)]

        #repopulate bottom 20% with offspring from best 20%
        for i in range(int(popSize/(breedVal))):
            childA, childB = breedMachine(bestCands, 1.1)
            currentCands.candidates.append(random.choice([childA,childB]))
            #currentCands.candidates.append(childB)


        if count%50 == 0: 
            print(f"iteration: {count}, list length is {len(currentCands.candidates)}, fitness of {currentCands.candidates[0].fitness}")
            currentCands.candidates[0].printData()




        printPop(currentCands)

        #helps algorithm overcome local minima

        #counts instances of one val being 1st
        if currentCands.candidates[2].fitness == bestFVal:
            tempCount += 1
        else:
            bestFVal = currentCands.candidates[2].fitness
            tempCount = 0

        if tempCount == 250:
            fittest = copy.deepcopy(currentCands.candidates[0:int(popSize/3)])
            weakest = copy.deepcopy(currentCands.candidates[-int(popSize/3):])
            del currentCands.candidates[-(len(fittest+weakest)):]
            for i in range(len(fittest)):
                childA, childB = breedMachine(fittest+weakest,1.1)
                currentCands.candidates.append(childA)
                currentCands.candidates.append(childB)

        
        if tempCount > 500:
            print("regerating cands")
            tempCand = currentCands.candidates[0]
            currentCands.createPops(popSize, givenGrid)
            currentCands.candidates[0] = tempCand
            currentCands.popFitnessUpdate()
            tempCount = 0


        if count == 5000:
            foundSolution =True
        
        count += 1


def breedMachine(selectCands, crossoverBound):
    #randomly select two from valid candidates
    #check if cands are different
    different = False
    '''
    sdsdf
    sdf
    sdf
    sdf
    sdfs
    df
    needs fixing
    '''
    while different == False:
        parentA = selectCands[random.randint(0, len(selectCands)-1)]
        parentB = selectCands[random.randint(0, len(selectCands)-1)]
        if parentA != parentB:
            different = True
    #initialise breedMachine
    breedMachine = s.BreedCandidates()
    #breed
    childA, childB = breedMachine.crossover(parentA, parentB, crossoverBound)
    childA.updateFitness()
    childB.updateFitness()
    #print(f"parent A has fitness of {parentA.fitness}\n parent B has fitness of {parentB.fitness}\n\nchild A has fitness of {childA.fitness}\nchild B has fitness of {childB.fitness}")
    #return children
    return childA, childB

#prints fitness of all cands
def printPop(pop):
    print("fitness")
    for i in pop.candidates:
        print (i.fitness)



breedVal = 5
muteVal = 5


popSizeChoice = input("select population size:\n1. 10\n2. 100\n3. 1000\n4. 10000\n")
while popSizeChoice not in ["1","2","3","4"]:
    popSizeChoice = input("select population size:\n1. 10\n2. 100\n3. 1000\n4. 10000\n")
if popSizeChoice == "1":
    popSize = 10
elif popSizeChoice == "2":
    popSize = 100
elif popSizeChoice == "3":
    popSize = 1000
elif popSizeChoice == "4":
    popSize = 10000

gridChoice = input("select population size:\n1. Grid1\n2. Grid2\n3. Grid3\n")
while gridChoice not in ["1","2","3"]:
    gridChoice = input("select population size:\n1. Grid1\n2. Grid2\n3. Grid3\n")
if gridChoice == "1":
    grid = "Grid1.ss"
elif gridChoice == "2":
    grid = "Grid2.ss"
elif gridChoice == "3":
    grid = "Grid3.ss"

main(popSize,grid)


