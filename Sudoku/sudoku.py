#sudoku evolutionary algorithm

import random
import time
import copy


#a group/population of candidates for one sample of the puzzle
class Pop:

    #initialisation for population
    def __init__(self):
        self.candidates = []

    #updates the fitness for all candidates in the population
    def popFitnessUpdate(self):
        #iterate through each candidate
        for i in self.candidates:
            i.updateFitness()


    #creates a full population
    def createPops(self, popSize, givenGrid):
        self.candidates = []
        #create a random seed
        randomSeed = time.time() 
        random.seed(randomSeed)
        #iterates for given amount defining size of pop
        for i in range(popSize):
            #temporary candidate to work with
            tempCand = Candidate()
            #find available spaces and fill
            for column in range(9):
                for row in range(9):
                    #checks if values are empty to fill
                    if givenGrid.values[column][row] == ".":
                        tempCand.data[column][row] = str(random.randint(1,9))
                    #otherwise fills with known value
                    else:
                        tempCand.data[column][row] = str(givenGrid.values[column][row])
            #add to candidates
            self.candidates.append(tempCand)


    #sorts the list of candidates by fitness 
    def sort(self):
        self.candidates.sort(key = lambda x:x.fitness)

    #goes through all candidates and decides which mutation path they should take, best doesnt change, first 5 go through 'beneficial' mutation, rest random mutation type
    def mutateAll(self, mutationBound, given):
        for i in range(1, len(self.candidates)):

            #checks if candidate should mutate or not according to mutationBound, by comparing to randomly generated val
            if mutationBound < random.uniform(0,1):
                if i <= 5:
                    #swap a repeated value into a non-existant value in the row
                    self.candidates[i].mutate2(given)
                else:
                    #randomly decides which mutation method to do
                    randChoice = random.uniform(0,1)
                    if randChoice < 0.3:
                        #swap a repeated value into a non-existant value in the row
                        self.candidates[i].mutate2(given)
                    elif randChoice < 0.6:
                        #swaps two random values in row or column
                        self.candidates[i].mutate1(given)
                    else:
                        #randomises a row
                        self.candidates[i].mutate3(given)
            self.candidates[i].updateFitness()

        return self.candidates





#single candidate and subsequent solution class
class Candidate:

    #initialisation
    def __init__(self):
        self.data = [["0" for val in range(9)] for val2 in range(9)]
        self.fitness = 0

    #updates the fitness of the candidate
    #check each value, if duplicates in row or column or block (+1 to fitness for each dupe)
    def updateFitness(self):
        rowTotal = 0
        columnTotal = 0
        blockTotal = 0


        #iterate through grid to count occurrences of values
        for column in range(9):
            for row in range(9):
                #current value being checked
                currentVal = self.data[column][row]

                #create row, column and block lists
                #column is column
                columnList = self.data[column]
                #row is as follows
                rowList = []
                #nth element in each column, n is row
                for i in range(9):
                    rowList.append(self.data[i][row])
                #block is calculated with blockNum
                block = []
                #finds start row for block calc
                blockNumRow = 3*int(row/3) 
                #start column for blovk calcs
                blockNumColumn =  3*int(column/3)
                for i in range(3):
                    #length of row + i
                    #length of column + i
                    block.append(self.data[blockNumColumn][blockNumRow + i])
                    block.append(self.data[blockNumColumn + 1][blockNumRow + i])
                    block.append(self.data[blockNumColumn + 2][blockNumRow + i])

                #check row of self for dupe values, call function(row, value), see if currentVal 
                if self.checkRowForDupe(rowList,currentVal) == True:
                    rowTotal += 1
                #check column of self for dupe values
                if self.checkColumnForDupe(columnList, currentVal) == True:
                    columnTotal += 1
                #calc which block (0-8), from top left, read to the right then down

                #check block of self for dupe values
                if self.checkBlockForDupe(block, currentVal) == True:
                    blockTotal += 1

        #calc fitness based off of totals
        self.fitness = rowTotal+columnTotal+blockTotal


    #checks a row for duplicates, row is a list and compares each element to value
    def checkRowForDupe(self, row, value):
        count = 0
        #check each element of row
        for i in row:
            #if the element is the same as value increase count by one
            if i == value:
                count += 1
        #if there are more than 2 instances of value then return True (there are duplicates)
        if count > 1:
            return True
        #if there are no duplicates ruturn false
        return False

    #checks a column for dupes, works same as prev, column is a list
    def checkColumnForDupe(self, column, value):
        count = 0
        #check each element of column
        for i in column:
            #if the element is the same as value increase count by one
            if i == value:
                count += 1
        #if there are more than 2 instances of value then return True (there are duplicates)
        if count > 1:
            return True
        #if there are no duplicates ruturn false
        return False

    #same as prev, block is a list
    def checkBlockForDupe(self, block, value):
        count = 0
        #check each element of row
        for i in block:
            #if the element is the same as value increase count by one
            if i == value:
                count += 1
        #if there are more than 2 instances of value then return True (there are duplicates)
        if count > 1:
            return True
        #if there are no duplicates ruturn false
        return False

    '''MUTATION METHODS - 
    randomly swap 2 values in row/column, except given
    if dupes in row, change one to none existant val in row
    completely randomise row, except given
    swap 2 random locations, not best
    '''


    #randomly swap two values in row/column
    def mutate1(self, board):
        #randomly generate row or column index
        RorCIndex = random.randint(0,8)
        #decide column or row
        RorC = random.randint(1,2)    
        #generate two random indexes in the list to swap, check if they don't overlap with given
        randIndex1 = random.randint(0,8)
        randIndex2 = random.randint(0,8)
        while True:
            if RorC == 1:
                #if values defined by given regenerate randomIndex vals
                if board.values[RorCIndex][randIndex1] == ".":
                    if board.values[RorCIndex][randIndex2] == ".":
                        break
                    else:
                        randIndex2 = random.randint(0,8)
                else:
                    randIndex1 = random.randint(0,8)
            else:
                if board.values[randIndex1][RorCIndex] == ".":
                    if board.values[randIndex2][RorCIndex] == ".":
                        break
                    else:
                        randIndex2 = random.randint(0,8)
                else:
                    randIndex1 = random.randint(0,8)
        #switch the two   
        if RorC == 1:
            #for row
            #print(f"mutating row {RorCIndex+1}, swapping {self.data[RorCIndex][randIndex1]} with {self.data[RorCIndex][randIndex2]}")
            temp = self.data[RorCIndex][randIndex1]
            self.data[RorCIndex][randIndex1] = self.data[RorCIndex][randIndex2]
            self.data[RorCIndex][randIndex2] = temp
        else:
            #for column
            #print(f"mutating column {RorCIndex+1}, swapping {self.data[randIndex1][RorCIndex]} with {self.data[randIndex2][RorCIndex]}")
            temp = self.data[randIndex1][RorCIndex]
            self.data[randIndex1][RorCIndex] = self.data[randIndex2][RorCIndex]
            self.data[randIndex2][RorCIndex] = temp


    #find duplicate in row and changes it to a value that doesnt exist in the row
    def mutate2(self, board):
        #generate random row index to work with
        randIndex = random.randint(0,8)
        #dictionary to count instances
        countVals = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0}
        #get row and count instances of values
        for i in range(9):
            countVals[self.data[randIndex][i]] += 1
        #creates a list of the values that appear more than once
        repeatVals = []
        nonExistantVals = []
        for i in range(len(countVals)):
            if countVals[str(i+1)] > 1:
                repeatVals.append(i+1)
            elif countVals[str(i+1)] == 0:
                nonExistantVals.append(i+1)
        #catches error if row is good
        if repeatVals == []:
            return
        else:
            #selects a random value that appears more than once, and one that doesnt appear at all
            target2Replace = random.choice(repeatVals)
            newVal = random.choice(nonExistantVals)
            #replace a value that appears more than once in the row, which is not given, with one that doesnt appear
            for i in range(9):
                if self.data[randIndex][i] == str(target2Replace) and board.values[randIndex][i] == ".":
                    #print(f"mutated row {randIndex}, changed to {newVal}")
                    self.data[randIndex][i] = str(newVal)
                    break

    #re-randomise row content
    def mutate3(self, board):
        #generate random list index
        randIndex = random.randint(0,8)
        #print(f"mutating row {randIndex+1}")
        #go through row, check if element is from given, otherwise randomise
        for i in range(len(self.data[randIndex])):
            if board.values[randIndex][i] == ".":
                self.data[randIndex][i] = str(random.randint(1,9))

    #prints data attibute, more nicely formatted
    def printData(self):
        for i in self.data:
            print(i)
    
    #copies data attribute, returns as a list
    def copyData(self):
        tempList = []
        for i in self.data:
            tempList.append(i)
        #print(tempList)
        return tempList


#  #######
# / <| |> \ 
# |  <->  |
#  \__|__/    inherited from Candidate, current board with given data
class Board(Candidate):

    def __init__(self,values):
        self.values = values



#use alt rows from parents
class BreedCandidates():

    #takes two 'parent' candidates and breeds them together, creating two children candidates which are a combination of the parents 'genes'
    def crossover(self, a, b, crossoverBound):
        #create temp child candidates
        childA = Candidate()
        childB = Candidate()
        #get data from parent candidates
        aData = a.copyData()
        bData = b.copyData()
        #checks if they should breed according to some predefined probability
        if random.uniform(0,1) < crossoverBound:
            for i in range(9):
                #takes alternating rows from either parent
                if i%2 == 0:
                    childA.data[i] = aData[i]
                    childB.data[i] = bData[i]
                else:
                    childA.data[i] = bData[i]
                    childB.data[i] = aData[i]
            return childA, childB
        #if probability not reached returns parents as children
        else:
            childA.data = aData
            childB.data = bData
            return childA, childB

            


