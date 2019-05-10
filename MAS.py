import random as rnd

from problog_controller import *
from matplotlib import colors
from matplotlib import pyplot as plt
import time


class Agent:
    """
    A class used to represent an agent within the multi-agent system.

    Attributes
    ----------
    number: int
        The unique identifier for this agent.
    plan: list
        The plan this agent wants to execute.
    """

    def __init__(self, number, plan):
        """
        The constructor of an Agent.
        :param number: The id of the agent.
        :param plan: The plan of the agent.
        """

        self.number = number
        self.plan = plan

class MAS:
    """
    A class used to represent a multi-agent system, which provides the functionalitie of executing the plans
    of every agent.

    Attributes
    ----------
    actionCaseList: list
        A list of all actionCases that define the actions that can be taken by agents. It defines
        the world for this multi-agent system
    agentList: list
        A list of strings containing the Agent-objects, representing the agents that are present in the world.
    plan: list
        A list of strings containing the intertwined plans of all agents.
    beginState: list
        A list of strings representing ProbLog facts, which describes the initial state of the world in the
        multi-agent system.
    failCondition: str
        The body of a failcondition predicate, provided in ProbLog code. The code implements the body of a ProbLog rule failCondition(State)
        which is true when the
    queryLessProgramString:
    perStepSatisfies:
    stateToString:
    windowSize:
    """

    def __init__(self,actionCaseList, failCondition, beginState, perStepSatisfies = None, stateToString = None, windowSize = None, agentList = []):
        self.actionCaseList = actionCaseList
        self.agentList = agentList
        self.beginState = beginState
        self.failCondition = failCondition
        self.queryLessProgramString = actionsToProblogProgram(self.actionCaseList, self.failCondition)
        self.perStepSatisfies = perStepSatisfies
        self.stateToString = stateToString
        self.windowSize = windowSize

    @property
    def beginState(self):
        return self.__beginState

    @beginState.setter
    def beginState(self, beginState):
        if (type(beginState) == list):
            self.__beginState = self.listOfStringsToStringOfList(beginState)
        else:
            self.__beginState = beginState

    def addAgent(self, number, plan):
        self.agentList.append(Agent(number, plan))

    def run(self):

        self.plan = self.intertwinePlans()
        currentState = self.beginState

        listOfProbabilities = []
        listOfTimesNeeded = []
        while(len(self.plan) > 0):

            if(self.stateToString != None):
                if(type(currentState) == list):
                    self.stateToString(self.listOfStringsToStringOfList(currentState))
                else:
                    self.stateToString(currentState)

            if (self.perStepSatisfies != None):
                if(self.windowSize == None):
                    t = time.time()
                    result = endStateSatisfiesQuery(self.queryLessProgramString, currentState, self.plan,
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
                                                    self.plan[0:self.windowSize],
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
        stateDictionary = execQuery(self.queryLessProgramString, state, [actionString])
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

    def listOfStringsToStringOfList(self, plan):
        planString = "["
        for step in plan:
            planString += step + ", "
        planString = planString.rstrip(", ") + "]"
        return planString

    def intertwinePlans(self):
        """
        A method which intertwines two plans.

        The method takes two plans, and forms a new plan, in which actions from the given plans alternate, starting with the first action of the first given plan.
        If one of the two plans is shorter than the other, the surplus actions of the longer plan are placed consecutively at the end of the new plan.

        For example:
        plan1 = [a, a, a]
        plan2 = [b, b, b, b, b]
        Resulting plan = [a, b, a, b, a, b, b, b]

        :param plan1: A list of strings representing the first plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].
        :param plan2: A list of strings representing the second plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].
        :return: A list of strings representing the resulting, intertwined plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].
        """

        maxPlanLength = 0
        for agent in self.agentList:
            if (len(agent.plan) > maxPlanLength):
                maxPlanLength = len(agent.plan)

        intertwinedPlan = []
        for i in range(maxPlanLength):
            for agent in self.agentList:
                if(i < len(agent.plan)):
                    intertwinedPlan.append(agent.plan[i])
        return intertwinedPlan



