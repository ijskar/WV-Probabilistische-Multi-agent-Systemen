from problog.program import PrologString
from problog import get_evaluatable
from problog.formula import LogicFormula
import matplotlib.pyplot as plt
from problog.sdd_formula import SDD

## de bedoeling
## gebruiker maakt een lijst van Action objecten
## roept create-world-declaration op met die lijst als argument en krijgt een file of een string terug
## we hebben ook nog een query functie

class ActionCase:

    def __init__(self,name,pre,add,delete,args,chance,casenr,assign=[]):
        self.preconditions = pre
        self.addlist = add
        self.assignmentList = assign
        self.deletelist = delete
        self.argumentlist = args
        self.name = name
        self.chance = chance
        self.casenr = casenr




def actionToString(action):
    #head van het predicaat
    actionString = action.name
    actionString = actionString + "("
    for arg in action.argumentlist:
        actionString += arg +', '
    actionString += "BT, ET, Step) :- \n"

    #chance that this case of the action is true
    actionString += "\t" + action.name + str(action.casenr)+ "(Step), \n"

    #tail van het predicaat
    #precondities
    for pre in action.preconditions:
        actionString += "\tmember(" + pre +", BT), \n"

    if (len(action.addlist) == 0) and (len(action.deletelist) == 0):
        actionString += "\tET = BT, \n"
    #assignments
    if (len(action.assignmentList)!=0):
        for a in action.assignmentList:
            actionString += "\t" + a + ",\n"
    #add
    if len(action.addlist) != 0:
        actionString += "\tTemp0 = ["
        for add in action.addlist:
            actionString += add +", "
        actionString = actionString.rstrip(", ") + " |BT], \n"

    #delete
    if len(action.deletelist) != 0:
        for i in range(0,len(action.deletelist)):
            if i == len(action.deletelist)-1:
                actionString += '\tdelete(Temp' + str(i) +', ' + action.deletelist[i] + ", ET). \n"
            else:
                actionString += '\tdelete(Temp' + str(i) +', ' + action.deletelist[i] + ", Temp"+ str(i+1) +"), \n"
    else:
        actionString = actionString.rstrip(', \n') + '.'
    return actionString

##
# ActionList is a list containing all the action objects
# failCondition is a string that contains the body of the predicate defining the
# conditions for which the execution fails. (In Problog code, the different conditions are separated by a ; and
# each line should be preceded with the tab character (\t), the body should end with a '.', the header of this
# predicate is failCondition(State))
# failcondition is an empty string when there is no fail condition.

def actionsToProblogProgram(actionList,failCondition=""):
    programString = ":- use_module(library(lists)). \n"
    dictionaryOfActionNames = {}

    #build problog program starting with the actions
    for action in actionList:
        programString += actionToString(action) +"\n"
        if action.name in dictionaryOfActionNames:
            dictionaryOfActionNames[action.name].append(action)
        else:
            dictionaryOfActionNames[action.name] = [action]

    #add conditional facts to program
    for key in dictionaryOfActionNames:
        actionslist = dictionaryOfActionNames[key]
        string = ""
        for action in actionslist:
            string +=str(action.chance) + "::"+key+str(action.casenr)+"(Step) ; "
        string = string.rstrip("; ")
        programString += string + ".\n"

    #failCondition predicate
    if failCondition != "":
        programString += "\nfailCondition(State):- \n" + failCondition

    #exec
    execString = "\nexec(BT, [], BT, _).\n"

    if failCondition != "":
        execString += "exec(BT, _, BT, _):- \n\t failCondition(BT).\n"

    for actionName in dictionaryOfActionNames:
        actions = dictionaryOfActionNames[actionName]
        anAction = actions[0]
        assert isinstance(anAction, ActionCase) ##just to be sure that the value is a list of Action objects

        #We construct an exec rule handling the case that the preconditions of this action are met
        #Header
        execString += "exec(BT, ["

        nameAndArgs = anAction.name +"("
        for arg in anAction.argumentlist:
            nameAndArgs += arg + ", "
        nameAndArgs = nameAndArgs.rstrip(", ")

        execString += nameAndArgs + ")|R], ET, StepN) :-\n"
        #Body
        if failCondition != "":
            execString += "\t \+ failCondition(BT), \n"
        execString += "\t" + nameAndArgs + ", BT, TempT, StepN), \n"
        execString += "\tStepNPlusOne is StepN + 1,\n"
        execString += "\texec(TempT, R, ET, StepNPlusOne).\n\n"

        #We construct an exec rule handling the case that the preconditions of this action are not met
        #In that case this action is not executed and we proceed with executing the rest of the plan
        #Header
        execString += "exec(BT, ["+ nameAndArgs + ")|R], ET, StepN) :-\n"
        #Body
        if failCondition != "":
            execString += "\t \+ failCondition(BT), \n"
        execString += "\t \+" + nameAndArgs + ", BT, TempT, StepN), \n"
        execString += "\tStepNPlusOne is StepN + 1,\n"
        execString += "\texec(BT, R, ET, StepNPlusOne).\n\n"

    programString += execString + "\n"
    with open('templateTail.pl', 'r') as template:
        programString += template.read()
    return programString

def runWhileProgram (programString):
	# Run ProbLog program and save retrieved dictionary of queries and associated probabilities in result.
	result = get_evaluatable().create_from(PrologString(programString)).evaluate()
	# Process results
	listOfTuples = []
	for _tuple in result.items():
            splitList = str(_tuple[0]).split(']')
            last = splitList[-1]
            splittedLast = last.split(',')
            key = int(splittedLast[1])
            listOfTuples.append((key, str(_tuple[1])))
	listOfProbabilities = []
	for _tuple in sorted(listOfTuples):
		listOfProbabilities.append(float(_tuple[1]))
	return listOfProbabilities

def plotWhileQuery(querylessProgString, beginState, condition, do, upperLimit, toContainList, title):
    query = "query(iterateOverLimit(" + beginState + ", " + "while(" + condition + ", [" + do + "], Limit), " + upperLimit + ", " + toContainList + ")). \n"
    programString = querylessProgString + query
    #print(programString)
    listOfProbabilities = runWhileProgram(programString)
    print(listOfProbabilities)
    plt.plot(range(1,len(listOfProbabilities)+1), listOfProbabilities, '-g')
    plt.axis([0, len(listOfProbabilities), 0, 1.05])
    plt.title(title)
    plt.xlabel("n")
    plt.ylabel("probability")
    plt.show()

def endStateContainsWhileVersionQuery(querylessProgString, beginState, condition, do, limit, toContainList):
    query = "query(endStateContainsWhileVersion(" + beginState + ", " + "while(" + condition + ", [" + do + "], " + limit + "), " + toContainList + ")). \n"
    programString = querylessProgString + query
    result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    print(result)
    #listOfProbabilities = runWhileProgram(programString)
    #print(listOfProbabilities)

def endStateContainsQuery(querylessProgString,beginState,plan,toContainList):
    query = "query(endStateContains("+beginState+", "+plan+", "+toContainList+")).\n"
    programString = querylessProgString + query
    formula = LogicFormula.create_from(PrologString(programString))
    sdd = SDD.create_from(formula)
    result = sdd.evaluate()
    #result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    print(result)
    return result

def execQuery(querylessProgString,beginState,plan):
    query = "query(exec(" + beginState + ", " + plan + ", EndState, 1)).\n"
    programString = querylessProgString + query
    result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    return result

#satisfiesBody is a string representing the body of the satisfies predicate, which takes 1 argument, namely a State. The
# body should contain the necessary tabs and dot.
# The predicate's head is satisfies(State).
def endStateSatisfiesQuery(querylessProgString,beginState,plan,satisfiesBody):
    programString = querylessProgString + "\n satisfies(State):- \n" + satisfiesBody+ "\n"
    programString += "query(endStateSatisfies(" + beginState + ", " + plan +")).\n"
    result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    #print(result)
    return result

def intertwinePlans(plan1, plan2):
    maxPlanLength = max(len(plan1), len(plan2))
    intertwinedPlan = "["
    for i in range(maxPlanLength):
        if(i < len(plan1)):
            intertwinedPlan += plan1[i] + ", "
        if(i < len(plan2)):
            intertwinedPlan += plan2[i] + ", "
    intertwinedPlan = intertwinedPlan.rstrip(", ") + "]"
    return intertwinedPlan


def test():
    #name,pre,add,delete,args,chance,casenr
    moveToTable1 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B"], 0.9, 1)
    moveToTable2 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], [], [], ["A", "B"], 0.1, 2)
    moveOn1 = ActionCase("moveOn", ["clear(A)", "clear(C)", "on(A,B)"], ["on(A,C)", "clear(B)"], ["on(A,B)", "clear(C)"], ["A", "B", "C"], 0.75, 1)
    listv = [moveToTable1,moveToTable2,moveOn1]

