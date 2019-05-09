from problog_controller import *

moveToTable1 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B"], 0.9, 1)
moveToTable2 = ActionCase("moveToTable", ["clear(A)", "on(A,B)"], [], [], ["A", "B"], 0.1, 2)
moveFromBlockOn1 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["on(A,C)", "clear(B)"], ["on(A,B)", "clear(C)"], ["A", "B", "C"], 0.75, 1)
moveFromBlockOn2 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], ["table(A)", "clear(B)"], ["on(A,B)"], ["A", "B", "C"], 0.15, 2)
moveFromBlockOn3 = ActionCase("moveFromBlockOn", ["clear(A)", "clear(C)", "on(A,B)"], [], [], ["A", "B", "C"], 0.10, 3)
moveFromTableOn1 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], ["on(A,C)"], ["clear(C)", "table(A)"], ["A", "C"], 0.75, 1)
moveFromTableOn2 = ActionCase("moveFromTableOn", ["clear(A)", "clear(C)", "table(A)"], [], [], ["A", "C"], 0.25, 2)
actionsList = [moveToTable1,moveToTable2,moveFromBlockOn1,moveFromBlockOn2,moveFromBlockOn3,moveFromTableOn1,moveFromTableOn2]

querylessProgramString = actionsToProblogProgram(actionsList)
beginState = "[table(a), table(e), table(g), table(f), on(b,a),on(c,b),on(d,c), clear(d), clear(e), clear(f), clear(g)]"
plan = "[moveToTable(d,c), moveFromBlockOn(c, b, e), moveFromTableOn(f, g), if(trueInState(on(f,g)), moveFromBlockOn(b, a, f), moveToTable(b,a))]"
endStateContainsQuery(querylessProgramString, beginState, plan,"on(b,f)")
endStateContainsQuery(querylessProgramString, beginState, plan,"[on(b,f), on(f,g)]")
endStateContainsQuery(querylessProgramString, beginState, plan,"clear(a)")