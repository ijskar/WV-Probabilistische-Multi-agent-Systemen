import matplotlib.pyplot as plt

from problog_controller import *

moveToTable1 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B"], 0.9, 1)
moveToTable2 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], [], [], ["A", "B"], 0.1, 2)
moveFromBlockOn1 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["on(A,C)", "clear(B)"], ["on(A,B)", "clear(C)"], ["A", "B", "C"], 0.75, 1)
moveFromBlockOn2 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B", "C"], 0.15, 2)
moveFromBlockOn3 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], [], [], ["A", "B", "C"], 0.10, 3)
moveFromTableOn1 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], ["on(A,C)"], ["clear(C)", "table(A)"], ["A", "C"], 0.30, 1)
moveFromTableOn2 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], [], [], ["A", "C"], 0.70, 2)
actionsList = [moveToTable1,moveToTable2,moveFromBlockOn1,moveFromBlockOn2,moveFromBlockOn3,moveFromTableOn1,moveFromTableOn2]

queryLessProgramString = actionsToProblogProgram(actionsList)
#plotWhileQuery(queryLessProgramString, "[clear(d), clear(c), clear(b), on(d,a), table(a), table(b), table(c)]", "trueInState(table(b))", "moveFromTableOn(b,c)", "3", "on(b,c)", "Probability of on(b,c) after n iterations of: WHILE table(b) DO moveOn(b,c)")

# maxLimit = 17
# runTimeArray = [maxLimit]
# for limit in range(1, maxLimit):
#     t = time.time()
#     endStateContainsWhileVersionQuery(queryLessProgramString, "[clear(d), clear(c), clear(b), on(d,a), table(a), table(b), table(c)]",
#                    "trueInState(table(b))", "moveFromTableOn(b,c)", str(limit), "on(b,c)")
#     elapsed = time.time() - t
#     print(elapsed)
#     runTimeArray.append(elapsed)
#
# print(runTimeArray)
#

#plotWhileQuery(queryLessProgramString, "[clear(d), clear(c), clear(b), on(d,a), table(a), table(b), table(c)]",
 #                   "trueInState(table(b))", "moveFromTableOn(b,c)", "3", "on(b,c)",
  #                  "Probability of on(b,c) after n iterations of: WHILE table(b) DO moveOn(b,c)")

#endStateContainsWhileVersionQuery(queryLessProgramString,  "[clear(d), clear(c), clear(b), on(d,a), table(a), table(b), table(c)]",
 #                 "trueInState(table(b))", "moveFromTableOn(b,c)", "3", "on(b,c)")

testArray = [0.13663434982299805, 0.2094416618347168, 0.22340011596679688, 0.23935937881469727, 0.28822970390319824, 0.2852351665496826, 0.33510375022888184, 0.37100768089294434, 0.4757387638092041, 0.7569665908813477, 1.3783140182495117, 2.8074898719787598, 6.62631368637085, 16.809043169021606, 43.48565316200256, 113.27683091163635]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Uitvoeringstijd in functie van aantal iteraties van de while-lus")
ax.set_xlabel("Aantal iteraties")
ax.set_ylabel("Uitvoeringstijd in seconden")
ax.set_yscale('log')
ax.plot(range(1, 17), testArray,  '#4A7A65')
plt.show(fig)
fig.savefig('C:/Users/Sara/Documents/Academiejaar 2018-2019/WV/WV/plot.png', dpi = 400)