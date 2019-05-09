import random as rnd

from problog_controller import *
from matplotlib import colors
from matplotlib import pyplot as plt
import time

class Agent:

    def __init__(self, number, plan):
        self.number = number
        self.plan = plan

class MAS:

    def __init__(self,actionList,failCondition, beginState, plan, perStepSatisfies = None, stateToString = None, windowSize = None):
        self.actionList = actionList
        self.agentList = []
        self.plan = plan
        self.beginState = beginState
        self.failCondition = failCondition
        self.queryLessProgramString = actionsToProblogProgram(self.actionList, self.failCondition)
        self.perStepSatisfies = perStepSatisfies
        self.stateToString = stateToString
        self.windowSize = windowSize

    def addAgent(self, number, plan):
        self.agentList(Agent(number, plan))

    def run(self):
        currentState = self.beginState

        listOfProbabilities = []
        listOfTimesNeeded = []
        while(len(self.plan) > 0):

            if(self.stateToString != None):
                self.stateToString(currentState)

            if (self.perStepSatisfies != None):
                if(self.windowSize == None):
                    t = time.time()
                    result = endStateSatisfiesQuery(self.queryLessProgramString, currentState, self.planToPlanString(self.plan),
                                           self.perStepSatisfies)
                    timeNeeded = time.time() - t
                    for key in result:
                        listOfProbabilities.append(result[key])
                        print("Chance that end state will satisfy the given condition: " + str(result[key]))
                    print("Time needed to calculate this probability: " + str(timeNeeded))
                    listOfTimesNeeded.append(timeNeeded)
                else:
                    t = time.time()
                    result = endStateSatisfiesQuery(self.queryLessProgramString, currentState,
                                                    self.planToPlanString(self.plan[0:self.windowSize]),
                                                    self.perStepSatisfies)
                    timeNeeded = time.time() - t
                    for key in result:
                        listOfProbabilities.append(result[key])
                        print("Chance the given condition will be satisfied in " + str(self.windowSize) + " steps: " + str(result[key]))
                    print("Time needed to calculate this probability: " + str(timeNeeded))
                    listOfTimesNeeded.append(timeNeeded)
            next = self.plan[0]
            currentState = self.myExec(currentState, next)
            self.plan.remove(self.plan[0])

        #Also show the end state.
        if (self.stateToString != None):
            self.stateToString(currentState)

        print("List of probabilities: " + str(listOfProbabilities))
        return (currentState, listOfProbabilities, listOfTimesNeeded)




        # while(len(self.plan) > 0):
        #     next = self.plan[0]
        #     actionName  = next.split("(")[0]
        #     actionCaseList = []
        #     for action in self.actionList:
        #         if (actionName == action.name):
        #             actionCaseList.append(action)
        #     currentState = self.exec(currentState, actionCaseList)
        #     self.plan.remove(self.plan[0])
        # return currentState

    def myExec(self, state, actionString):
        stateDictionary = execQuery(self.queryLessProgramString, state, "["+actionString+"]")
        #Parsing
        pickedCase = self.pickCase(stateDictionary)
        temp1 = str(pickedCase).split("[")[-1]
        temp2 = temp1.split("]")[0]
        return "[" + temp2 + "]"


    def pickCase(self, stateDictionary):
        randomNumber = rnd.uniform(0, 1)
        counter = 0.0
        for key in stateDictionary:
            counter += stateDictionary[key]
            if (randomNumber <= counter):
                return key
        return None

    def planToPlanString(self, plan):
        planString = "["
        for step in plan:
            planString += step + ", "
        planString = planString.rstrip(", ") + "]"
        return planString


