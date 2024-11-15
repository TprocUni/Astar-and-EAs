#A* algorithm
import random

class Puzzle:

    def __init__(self, state):
        self.state = state

    #creates puzzle state
    def puzzleConfig(puzString):
        puzzle = []
        #splits the values up in a 2d list
        for i in range(9):
            temp = puzString.split(" ")
            puzzle.append(temp)
        return puzzle

    #manhattan distance heuristic
    def f(self,targetPuz,prevNodeLevel):
        #calc h value - the heuristic
        h = 0
        f = prevNodeLevel
        for i in range(3):
            for j in range(3):
                #find current value at location specified by loop
                currentVal = self.copy()[i][j]
                #find location of value in target 
                y1,x1 = targetPuz.find(currentVal)
                manhattanDistance = abs(i-y1) + abs(j-x1)
                f += manhattanDistance
        return f


    #calculates heuristic values using misplaced tiles heuristic
    def f2(self,targetPuz,prevNodeLevel):
        #calc h value - the heuristic
        h = 0
        for i in range(3):
            for j in range(3):
                #checks if tile is misplaced and that it isn't "_"
                if targetPuz.state[i][j] != self.state[i][j] and self.state[i][j] != "_":
                    h += 1

        #g is the level of the node (current node)
        f = h + prevNodeLevel
        return f


    #prints the puzzle state to the screen
    def printPuz(self):
        for i in self.state:
            print (f" {i[0]} , {i[1]} , {i[2]} ")
        print("\n")

    #finds a given symbol 
    def find(self, symbol):
        #iterate through all positions
        for x in range(len(self.state)):
            for y in range(len(self.state[x])):
                #checks if same, and if so returns x and y coords
                if self.state[x][y] == symbol:
                    return x,y
        #if not present returns illegal location and error message is printed
        print(f"error, {symbol} not present")
        return -1,-1  

    #copies puzzle configuation
    def copy(self):
        contents = []
        #iterates through all values
        for i in self.state:
            tempList = []
            for j in range (3):
                #copies to smaller temp list which is used to populate the 2d array
                tempList.append(i[j])
            contents.append(tempList)
        return contents

    #swaps two tiles
    def swap(self, initial, target):
        #places known value where "_" is, then replaces known value with "_"
        self.state[initial[0]][initial[1]] = self.state[target[0]][target[1]]
        self.state[target[0]][target[1]] = "_"



class node:
    #current node information 
    def __init__(self, data, level, fValue):
        self.level = level
        self.data = data
        self.f = fValue

    #create a list of offspring puzzles  
    def createOffspring(self):
        offspring = []
        x,y = self.data.find("_")
        #generates a list of theoretical positions surrounding the "_"
        possiblePos = [[x-1,y],[x+1,y],[x,y+1],[x,y-1]]
        #checks said positions validity
        possiblePos = self.checkNewPos(possiblePos)
        #iterates through the theoretical positions, and if they were deduced to be invalid, ignores them, otherwise updates and creates puzzle
        for i in possiblePos:
            if i is not None:
                #create new puzzle state and append to offspring
                tempPuz = Puzzle(self.data.copy())
                #swap '_' with target
                tempPuz.swap([x,y],i)
                offspring.append(tempPuz)

        return offspring


    #checks if the positions generated fall within the bounds of the 3x3 grid
    def checkNewPos(self,possiblePos):
        validPos = []
        for i in possiblePos:
            #checks its lies within x and y 0-2 (inclusive)
            if i[0] < 0 or i[0] > 2 or i[1] < 0 or i[1] > 2:
                #if it doesnt returns none value which can be disounted further down the line
                validPos.append(None)
            else:
                validPos.append(i)
        return validPos
        


def main():
    #welcome message
    print('''
    --------------------WELCOME--------------------
    This is an implementation of the A* algorithm, 
    using either the misplaced tile heuristic, man-
    hattan distance, or a combination of the two!
    
    ''')
    #nodes that have been selected due to good f value
    selectedNodes = []
    #nodes being worked on currently and need selection
    workingNodes = []
    #asks user which heurisitc they want to use
    chosenH = 1
    chosenH = int(input("Which heuristic would you like to use:\n1. Misplaced tiles\n2. Manhattan distance\n3. both!!\n(default is manhattan distance)\n"))
    #starting puzzle states
    startVal = [["7","2","4"],["5","_","6"],["8","3","1"]]
    targetVal = [["_","1","2"],["3","4","5"],["6","7","8"]]
    #transform starting values into puzzles
    startPuz = Puzzle(startVal)
    targetPuz = Puzzle(targetVal)
    #transform starting state into node, target will happen later, dependant on chosen heuristic
    if chosenH == 1:
        SF = startPuz.f2(targetPuz,0)
    elif chosenH == 3:
        SF = startPuz.f2(targetPuz,0) + startPuz.f(targetPuz,0)
    else:
        SF = startPuz.f(targetPuz,0)
    startNode = node(startPuz, 0, SF)
    startPuz.printPuz()
    #add start node to beginning of selected node
    selectedNodes.append(startNode)
    #loop stuff
    beans = True
    g = 0
    while beans:
        #create list of offspring based off of most recent node
        workingNode = selectedNodes[-1]
        offspring = workingNode.createOffspring()
        #find best choice

        #transform offspring into nodes
        for i in offspring:
            if chosenH == 1:
                #find f value for each offspring, depending on heuristic chosen
                fVal = i.f2(targetPuz,workingNode.level)
            elif chosenH == 3:
                fVal = i.f2(targetPuz,workingNode.level) + i.f(targetPuz,0)
            else:
                fVal = i.f(targetPuz,workingNode.level)
            #adds the developed offspring puzzles into working
            workingNodes.append(node(i,workingNode.level+1,fVal))
        #check if node puzzle state has existed in selected nodes previously
        for i in workingNodes:
            for j in selectedNodes:
                if j.data.copy() == workingNodes[0].data.copy():
                    #work on this see why not bouncing properly 
                    workingNodes[0].f += random.randint(0,7)*100 
            #sorts list so smallest value always first, ensuring repeated states are beened   
            workingNodes.sort(key = lambda x:x.f)
                    


        #select random from best options, this helps avoid loops as the first selected option of equally weighted choices will continue to oscillate between two
        #nodes if neither garner a better f value.
        #^tests

        #gets node with smallest f value
        selectedNode = workingNodes[0]        


        #nice formatting
        print("----------------------------------------------")
        selectedNode.data.printPuz()
        print(selectedNode.level)
        print(f"with fVal of: {selectedNode.f}\n")
        print("----------------------------------------------")



        # add selectedNode to selectedNodes, check if same as targetPuz
        selectedNodes.append(selectedNode)
        #checks if current state is same as target, prints to screen number of iterations and type of heuristic used
        currentConfig = selectedNode.data.copy()
        if currentConfig == targetVal:
            if chosenH == 1:
                print(f"matched in {selectedNodes[-1].level} moves, using misplaced tiles")
            elif chosenH == 3:
                print(f"matched in {selectedNodes[-1].level} moves, using both heuristics")
            else:
                print(f"matched in {selectedNodes[-1].level} moves, using manhattan distance")
            beans = False
        #empty workingNodes
        workingNodes = []

        #implementing limit - explained logic in answers
        if workingNode.level > 362880:
            print("maximum number of moves reached, every possible state has been tested")
            beans = False


#main
main()