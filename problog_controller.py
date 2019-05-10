from problog.program import PrologString
from problog import get_evaluatable
from problog.formula import LogicFormula
import matplotlib.pyplot as plt
from problog.sdd_formula import SDD

class ActionCase:
    """
    A class used to represent a specific case of an action, with a probability of that case taking place when executing the action.

    Attributes
    ----------
    name : str
        The name of the action this action case object is a case of. The name is used to identify the action this action case is a case of,
        as well as identifying other action cases of the same action.
    preconditions: list
        A list of strings that represent the preconditions of this action case as ProbLog facts.
    addlist: list
        A list of strings that represent the additions to a state when this action case gets executed on that state as ProbLog facts.
    deletelist: list
        A list of strings that represent the deletions from a state when this action case gets executed on that state as ProbLog facts.
    argumentlist: list
        A list of arguments that should be provided, alongside the name of the action, to represent the action this action case is a case of in a plan.

        For example: moveToTable1 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B"], 0.9, 1) is an
        action case of the action of moving a block to a table in the blocks world. The point of this action is to move a block A, which is standing
        on a block B, to the table. The preconditions, additions and deletions are defined in function of A and B. The name of this action (case) is "moveToTable", and its
        argumentlist-attribute is ["A", "B"]. This means that if one would want to move a block x, which is standing on a block y, to the table,
        one would represent the moveToTable action in a plan as a "moveToTable(x,y)" string. If, on the other hand, block y is standing on block x,
        and one wants to move y to the table, the representation in a plan would be "moveToTable(y,x)".
    probability: float
        The probability of this case happening when the action this action case is a case of gets performed.
    casenr: int
        An integer identifying this action case for the action it belongs to. Each action case belonging to the same
        action should have a unique casenr. Action cases belonging to different action (having different names) can have
        the same casenr.
    assignmentlist: list
        (optional but advanced) A list of strings that represent ProbLog assignments.

        For example: We definine an action case of an action named "right" as follows:
        right = ActionCase("right", ["at(N,X,Y)"], ["at(N,X+1,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1)
        The point of this action is to move a robot N, which is located at position (X, Y) in a grid, to the right. In other words,
        if robot(N) is located at (X, Y) (represented as "at(N, X, Y)"), we want the robot to be located at (X+1, Y) after executing this action case.
        One might try putting "at(N, X+1, Y)" in the addlist of this actioncase, but this wouldn't work.
        Just like in ProbLog, as well as ProLog, X+1 will not get grounded to the value of X incremented by one.
        Instead, one would have to add "at(N, NX, Y) to the addlist, and "NX is X+1" to the assignmentlist.
        The correct declaration of the action is then:
        right = ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NX is X+1"])
    """

    def __init__(self,name,pre,add,delete,args,prob,casenr,assign=[]):
        """
        The constructor of an ActionCase. For more detailed information and examples for the parameters, see the class documentation for ActionCase.
        :param name: The name of the action this action case object is a case of.
        :param pre: A list of strings that represent the preconditions of this action case as ProbLog facts.
        :param add: A list of strings that represent the additions to a state when this action case gets executed on that state as ProbLog facts.
        :param delete: A list of strings that represent the deletions from a state when this action case gets executed on that state as ProbLog facts.
        :param args: A list of arguments that should be provided, alongside the name of the action, to represent the action this action case is a case of in a plan.
        :param prob: The probability of this case happening when the action this action case is a case of gets performed.
        :param casenr: An integer identifying this action case for the action it belongs to.
        :param assign: (optional but advanced) A list of strings that represent ProbLog assignments.
        """
        self.name = name
        self.preconditions = pre
        self.addlist = add
        self.deletelist = delete
        self.argumentlist = args
        self.probability = prob
        self.casenr = casenr
        self.assignmentlist = assign




def actionToProblog(actionCase):
    """
    A method that translates an ActionCase object to ProbLog code defining this action case.

    It is used when generating a ProbLog program using the actionsToProblogProgram method.

    Parameters
    ----------
    :param actionCase: The ActionCase object to generate ProbLog code about.

    Returns
    -------
    :return: A string containing the generated ProbLog code.
    """

    #head van het predicaat
    actionString = actionCase.name
    actionString = actionString + "("
    for arg in actionCase.argumentlist:
        actionString += arg +', '
    actionString += "BT, ET, Step) :- \n"

    #chance that this case of the action is true
    actionString += "\t" + actionCase.name + str(actionCase.casenr) + "(Step), \n"

    #tail van het predicaat
    #precondities
    for pre in actionCase.preconditions:
        actionString += "\tmember(" + pre +", BT), \n"

    if (len(actionCase.addlist) == 0) and (len(actionCase.deletelist) == 0):
        actionString += "\tET = BT, \n"
    #assignments
    if (len(actionCase.assignmentlist)!=0):
        for a in actionCase.assignmentlist:
            actionString += "\t" + a + ",\n"
    #add
    if len(actionCase.addlist) != 0:
        actionString += "\tTemp0 = ["
        for add in actionCase.addlist:
            actionString += add +", "
        actionString = actionString.rstrip(", ") + " |BT], \n"

    #delete
    if len(actionCase.deletelist) != 0:
        for i in range(0, len(actionCase.deletelist)):
            if i == len(actionCase.deletelist)-1:
                actionString += '\tdelete(Temp' + str(i) +', ' + actionCase.deletelist[i] + ", ET). \n"
            else:
                actionString += '\tdelete(Temp' + str(i) +', ' + actionCase.deletelist[i] + ", Temp" + str(i + 1) + "), \n"
    else:
        actionString = actionString.rstrip(', \n') + '.'
    return actionString



def actionsToProblogProgram(actionList,failCondition=""):
    """
    A method used to generate ProbLog code to reason about a given list of ActionCase objects.

    It generates ProbLog code defining each action case in the given list, using the actionToProblog method.
    On top of that, it generates ProbLog code used to all find all possible states resulting from executing an action, or a plan of actions on a state.
    All this ProbLog code gets appended, and returned as a string representing a ProbLog program.
    Optionally, the body of a failCondition in ProbLog code can be provided in the form of a string. When a state satisfies
    the failCondition, actions do not alter the state. In other words: when a failcondition is provided, an action only alters a state if:
        a) The state meets the action's preconditions
        b) The state does not meet the failcondition
    When providing a failcondition, one should only provide the body of the predicate. Each line should be preceded by a tab character (\t),
    each line needs to end with a comma (,) and a newline (\n), and the body has to end with a period (.).
    The header of the predicate may not be provided in the given string, as it will be added internally by this method.
    When refering to the state that gets checked for the failcondition, refer to it with State. For example:
    when the failcondition is that a foo(bar) fact is present in the state, the failCondition-argument would be:
        "\tmember(foo(bar),State)."
    Another example of a valid failCondition-argument:
        "\tmember(at(R1,X,Y),State),
         \n\tmember(at(R2,X,Y),State),
         \n\tR1 \= R2."

    Parameters
    ----------
    :param actionList: A list of all ActionCases the generated ProbLog program should support.
    :param failCondition: (optional but advanced) The body of a failcondition predicate, provided in ProbLog code. Familiarity with ProbLog
    is required in order to use this parameter.

    Returns
    -------
    :return: A string containing the generated ProbLog program that can reason about plans made up of actions from the given list of action cases.
    """

    programString = ":- use_module(library(lists)). \n"
    dictionaryOfActionNames = {}

    #build problog program starting with the actions
    for action in actionList:
        programString += actionToProblog(action) + "\n"
        if action.name in dictionaryOfActionNames:
            dictionaryOfActionNames[action.name].append(action)
        else:
            dictionaryOfActionNames[action.name] = [action]

    #add conditional facts to program
    for key in dictionaryOfActionNames:
        actionslist = dictionaryOfActionNames[key]
        string = ""
        for action in actionslist:
            string +=str(action.probability) + "::"+key+str(action.casenr)+"(Step) ; "
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



def endStateContainsQuery(querylessProgString, beginState, plan, toContainList):
    """
    A method used to query for the probability that a given fact or list of facts would be true in the end state, if one would perform a given plan on a given begin state.

    The method takes a string containing a ProbLog program, generated by the actionsToProblogProgram method. It generates a query, asking
    what the probability is that a given fact or list of facts would be true in the end state, if one would perform a given plan of probabilistic actions on a given begin state.
    It appends this generated query to the given ProbLog program, executes the ProbLog program and returns the result of the query as a dictionary in which the query is the key,
    and the resulting probability is the value.
    The given ProbLog program has to be able to reason about the actions in the given plan, which is the case if all the ActionCase objects relating to those actions were passed to
    the actionsToProblogProgram method when the ProbLog program was generated.

    Parameters
    ----------
    :param querylessProgString: A ProbLog program, generated by the actionsToProblogProgram method, which is able to reason about the actions in the given plan.
    :param beginState: A list of strings representing the begin state. This is a list of ProbLog facts, for example: ["table(a)", "table(e)", "table(g)"]
    :param plan: A list of strings representing the plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].
    :param toContainList: A list of strings representing the fact(s) that are queried for. This is a list of ProbLog facts,
    for example: ["on(b,f)"], or ["on(b,f)", "on(f,g)"].

    Returns
    -------
    :return: The result of the query as a dictionary in which the query is the key, and the resulting probability is the value.
    """

    if (type(beginState) == list):
        query = "query(endStateContains(" + listOfStringsToStringOfList(beginState) +", " + listOfStringsToStringOfList(plan) +", " + listOfStringsToStringOfList(toContainList) + ")).\n"
    else:
        query = "query(endStateContains(" + beginState + ", " + listOfStringsToStringOfList(plan) + ", " + listOfStringsToStringOfList(
            toContainList) + ")).\n"

    programString = querylessProgString + query
    formula = LogicFormula.create_from(PrologString(programString))
    sdd = SDD.create_from(formula)
    result = sdd.evaluate()
    print(result)
    return result



def execQuery(querylessProgString,beginState,plan):
    """
    A method used to find all states that could be reached, and with what probability, if one would perform a given plan of probabilistic actions on a given begin state.

    The method takes a string containing a ProbLog program, generated by the actionsToProblogProgram method. It generates a query,
    asking what states could be reached could be reached, and with what probability, if one would perform a given plan of probabilistic actions on a given begin state.
    It appends this generated query to the given ProbLog program, executes the ProbLog program and returns the result of the query as a dictionary.
    This dictionary contains various entries: one for each possible end state. The keys of the dictionary are string representations of the query,
    each with a possible end state grounded as third argument. Each value is the probability that the end state found in the associated key would take place
    if one would perform the plan.
    The given ProbLog program has to be able to reason about the actions in the given plan, which is the case if all the ActionCase objects relating to those actions were passed to
    the actionsToProblogProgram method when the ProbLog program was generated.

    Parameters
    ----------
    :param querylessProgString: A ProbLog program, generated by the actionsToProblogProgram method, which is able to reason about the actions in the given plan.
    :param beginState: A list of strings representing the begin state. This is a list of ProbLog facts, for example: ["table(a)", "table(e)", "table(g)"]
    :param plan: A list of strings representing the plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].

    Returns
    -------
    :return: The result of the query as a dictionary.
    """

    if (type(beginState) == list):
        query = "query(exec(" + listOfStringsToStringOfList(beginState) + ", " + listOfStringsToStringOfList(plan) + ", EndState, 1)).\n"
    else:
        query = "query(exec(" + beginState + ", " + listOfStringsToStringOfList(
            plan) + ", EndState, 1)).\n"

    programString = querylessProgString + query
    result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    return result



def endStateSatisfiesQuery(querylessProgString,beginState,plan,satisfiesBody):
    """
    A method used to query for the probability that the end state would satisfy a given satisfies-predicate, if one would perform a given plan on a given begin state.

    The method takes a string containing a ProbLog program, generated by the actionsToProblogProgram method. It generates a query, asking
    what the probability is that the end state would satisfy a given satisfies-predicate, if one would perform a given plan of probabilistic actions on a given begin state.
    The body of the satisfies-predicate in ProbLog code has to be provided in the form of a string.
    The method appends the generated query to the given ProbLog program, executes the ProbLog program and returns the result of the query as a dictionary in which the query is the key,
    and the resulting probability is the value.
    The given ProbLog program has to be able to reason about the actions in the given plan, which is the case if all the ActionCase objects relating to those actions were passed to
    the actionsToProblogProgram method when the ProbLog program was generated.

    When providing a satisfies-predicate, one should only provide the body of the predicate.
    Each line should be preceded by a tab character (\t), each line needs to end with a comma (,) and a newline (\n), and the body has to end with a period (.).
    The header of the predicate may not be provided in the given string, as it will be added internally by this method.
    When refering to the state that gets checked for the satisfy-condition, refer to it with State. For example:
    when a state satisfies the satisfies-predicate iff a foo(bar) fact is present in the state, the satisfiesBody-argument would be:
        "\tmember(foo(bar),State)."
    Another example of a valid satisfiesBody-argument:
        "\tmember(at(R1,X,Y),State),
         \n\tmember(at(R2,X,Y),State),
         \n\tR1 \= R2."

    Parameters
    ----------
    :param querylessProgString: A ProbLog program, generated by the actionsToProblogProgram method, which is able to reason about the actions in the given plan.
    :param beginState: A list of strings representing the begin state. This is a list of ProbLog facts, for example: ["table(a)", "table(e)", "table(g)"]
    :param plan: A list of strings representing the plan. This is a list of actions, for example: ["moveToTable(d,c)", "moveFromBlockOn(c, b, e)"].
    :param satisfiesBody: The body of a satisfies-predicate, provided in ProbLog code. Familiarity with ProbLog
    is required.

    Returns
    -------
    :return: The result of the query as a dictionary in which the query is the key, and the resulting probability is the value.
    """

    programString = querylessProgString + "\n satisfies(State):- \n" + satisfiesBody+ "\n"
    if(type(beginState) == list):
        programString += "query(endStateSatisfies(" + listOfStringsToStringOfList(beginState) + ", " + listOfStringsToStringOfList(plan) +")).\n"

    else:
        programString += "query(endStateSatisfies(" + beginState + ", " + listOfStringsToStringOfList(plan) + ")).\n"

    result = get_evaluatable().create_from(PrologString(programString)).evaluate()
    #print(result)
    return result



def listOfStringsToStringOfList(plan):
    planString = "["
    for step in plan:
        planString += step + ", "
    planString = planString.rstrip(", ") + "]"
    return planString


