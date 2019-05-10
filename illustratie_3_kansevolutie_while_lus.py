from problog_controller import *
import matplotlib.pyplot as plt

moveToTable1 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B"], 0.4, 1)
moveToTable2 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], [], [], ["A", "B"], 0.6, 2)
moveFromBlockOn1 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["on(A,C)", "clear(B)"], ["on(A,B)", "clear(C)"], ["A", "B", "C"], 0.75, 1)
moveFromBlockOn2 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B", "C"], 0.15, 2)
moveFromBlockOn3 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], [], [], ["A", "B", "C"], 0.10, 3)
moveFromTableOn1 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], ["on(A,C)"], ["clear(C)", "table(A)"], ["A", "C"], 0.75, 1)
moveFromTableOn2 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], [], [], ["A", "C"], 0.25, 2)
actionsList = [moveToTable1,moveToTable2,moveFromBlockOn1,moveFromBlockOn2,moveFromBlockOn3,moveFromTableOn1,moveFromTableOn2]

querylessProgramString = actionsToProblogProgram(actionsList)
print(querylessProgramString)
beginState = ["table(a)", "table(e)", "table(g)", "table(f)", "on(b,a)","on(c,b)","on(d,c)", "clear(d)", "clear(e)", "clear(f)", "clear(g)"]
list = []
for i in range(1,14):
    plan = ["while(falseInState(clear(c)), [moveToTable(d,c)]," + str(i) + ")", "while(falseInState(clear(b)), [moveToTable(c,b)]," +
            str(i) + ")", "while(falseInState(clear(a)), [moveToTable(b,a)]," + str(i) + ")"]
    result = endStateContainsQuery(querylessProgramString, beginState, plan,["clear(a)"])
    for key in result:
        list.append(result[key])
plt.plot(range(1,len(list)+1), list, '-g')
plt.axis([0, len(list), 0, 1.05])
plt.title("Kansevolutie")
plt.xlabel("Limiet op aantal iteraties")
plt.ylabel("Kans op clear(a)")
plt.show()
