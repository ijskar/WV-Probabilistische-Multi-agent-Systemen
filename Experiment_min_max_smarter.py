import operator
from itertools import *
from random import *
import re
from MAS import *

size = 9

actionCaseList = []
actionCaseList.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NX is X+1"]))
actionCaseList.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NX is X+1", "NY is Y+1"]))
actionCaseList.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NX is X+1", "NY is Y-1"]))
actionCaseList.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NX is X-1"]))
actionCaseList.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NX is X-1", "NY is Y+1"]))
actionCaseList.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NX is X-1", "NY is Y-1"]))
actionCaseList.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,X,NY)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NY is Y+1"]))
actionCaseList.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NY is Y+1", "NX is X+1"]))
actionCaseList.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NY is Y+1", "NX is X-1"]))
actionCaseList.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,X,NY)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NY is Y-1"]))
actionCaseList.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NY is Y-1", "NX is X+1"]))
actionCaseList.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NY is Y-1", "NX is X-1"]))

failCondition = "\t( member(at(R1,X,Y),State)," \
                "\n\tmember(at(R2,X,Y),State)," \
                "\n\tR1 \= R2); " \
                "\n\t( member(at(N,X,Y),State)," \
                "\n\t (X<0 ; X>" + str(size-1) + "; Y<0; Y>" + str(size-1) +") ).\n"



queryLessProgramString = actionsToProblogProgram(actionCaseList, failCondition)

def stateToString(state):
    dict = {}
    #Change sizeOfGrid for representations of other grid sizes.
    sizeOfGrid = size
    temp = re.split(',|\(|\)', state)

    i = 1
    while(i < len(temp)):
        dict[temp[i]] = (temp[i+1], temp[i+2])
        i+=5

    matrix = [["o" for k in range(sizeOfGrid)] for l in range(sizeOfGrid)]
    outOfBounds = False
    for key in dict:
        value = dict[key]
        if(int(value[1]) < 0 or int(value[1]) >= size or int(value[0]) < 0 or int(value[0]) >= size):
            outOfBounds = True
            break

        if(matrix[size - 1 - int( value[1])][int(value[0])] == "o"):
            #The origin of our grid lies in the bottom left, but origin of the matrix lies in the top left,
            #so the vertical coordinate needs to be converted, hence: size - 1 - value[1].
            matrix[size - 1 - int(value[1])][int(value[0])] = key
        else:
            matrix[size - 1 - int(value[1])][int(value[0])] = "X"

    if(outOfBounds):
        print("Out of bounds!")
    else:
        for k in range(sizeOfGrid):
            print()
            for l in range(sizeOfGrid):
                print(matrix[k][l], end = '')
        print()

#Convert a list of strings to a string of the list. Example: ["a", "b", "c"] --> "[a, b, c]"
def planToPlanString(plan):
    planString = "["
    for step in plan:
        planString += step + ", "
    planString = planString.rstrip(", ") + "]"
    return planString

windowSize = 1
actionsForAgentOneToChooseFrom = ["right(1)", "up(1)", "down(1)", "left(1)"]
actionsForAgentTwoToChooseFrom = ["right(2)", "up(2)", "down(2)", "left(2)"]

#The problog body of the predicate that agent one tries to satisfy. Agent one desires to collide, while avoiding
#ending up outside of the grid's boundaries.
satisfiesBodyAgentOne = "\tmember(at(1,X,Y),State),\n\tmember(at(2,X,Y),State),\n\t (X>=0, X<" + str(size) + ", Y>=0, Y<" + str(size) +").\n"
#The problog body of the predicate that agent two tries to satisfy. Agent two avoids collision, while also avoiding
#ending up outside of the grid's boundaries.
satisfiesBodyAgentTwo = "\tmember(at(1,X1,Y1),State),\n\tmember(at(2,X2,Y2),State),\n\t (X1 \= X2 ; Y1 \= Y2),\n\t (X2>=0, X2<" + str(size) + ", Y2>=0, Y2<" + str(size) +").\n"


#Determines and returns the first action for a given agent to take.
#Agent one maximizes the probability of colliding, given a current state.
#Agent two minimizes the probability of colliding, given a current state.
def createAgentPlan(currentState, agentNumber):

    satisfiesBody = None
    otherAgentActions = None
    temp = None
    # Generate all possible plans(as tuples) of length windowSize.
    if(agentNumber == 1):
        #Shuffle so that when two actions have same probability of collision, the same is not always chosen.
        shuffle(actionsForAgentOneToChooseFrom)
        temp = product(actionsForAgentOneToChooseFrom, repeat = windowSize)

        satisfiesBody = satisfiesBodyAgentOne

        otherAgentActions = actionsForAgentTwoToChooseFrom

    elif(agentNumber == 2):
        #Shuffle so that when two actions have same probability of collision, the same is not always chosen.
        shuffle(actionsForAgentTwoToChooseFrom)
        temp = product(actionsForAgentTwoToChooseFrom, repeat = windowSize)

        satisfiesBody = satisfiesBodyAgentTwo

        otherAgentActions = actionsForAgentOneToChooseFrom


    # A dictionary in which the keys are the plans, and the values are the probabilities of collision.
    planProbabilityDictionary = {}

    # For each plan, we calculate the associated probability of colliding, and add this to the dictionary.
    i = 0
    listOfPlans = []

    for element in temp:
        plan = list(element)
        #A dictionary's keys cannot be lists (plans are lists), so we store the plans in an array, and associate each plan's index with
        #the plan's corresponding probability in the planProbabilityDictionary.
        listOfPlans.append(plan)

        listOfProbabilities = []
        # take the other agent's possible reactions into account
        for action in otherAgentActions:
            #insert the other agent's move into the plan
            newPlan = plan.copy()
            newPlan.insert(1,action)
            result = endStateSatisfiesQuery(queryLessProgramString, currentState, planToPlanString(newPlan), satisfiesBody)
            key, value = result.popitem()
            listOfProbabilities.append(value)
        #Assuming that the other agent will maximize its chance of success,
        # we assign the probability associated with the worst case to this agent's plan
        worstCase = min(listOfProbabilities)
        planProbabilityDictionary[i] = worstCase
        i += 1


    # Determine the plan which maximizes or minimizes the probability of colliding, depending on the given agent number.
    chosenPlanIndex = max(planProbabilityDictionary.items(), key=operator.itemgetter(1))[0]


    #Return the first action of the chosen plan, i.e. the action that maximizes/minimizes the probability of colliding.
    return [listOfPlans[chosenPlanIndex][0]]

currentState = "[at(1,4,4),at(2,5,3)]"
matrix = stateToString(currentState)
tempSatisfiesBody = "\tmember(at(1,X,Y),State),\n\tmember(at(2,X,Y),State)."
mas = MAS(actionCaseList, failCondition, currentState, [], tempSatisfiesBody, stateToString)
for i in range(10):
    #Agent one makes a move.
    mas.plan = createAgentPlan(currentState, 1)
    print(mas.plan)
    currentState = mas.run()[0]
    mas.beginState = currentState

    #Agent two makes a move.
    mas.plan = createAgentPlan(currentState, 2)
    print(mas.plan)
    currentState = mas.run()[0]
    mas.beginState = currentState