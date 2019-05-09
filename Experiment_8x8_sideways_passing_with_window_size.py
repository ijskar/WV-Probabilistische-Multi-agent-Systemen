import re

from MAS import *

size = 8

list = []
list.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NX is X+1"]))
list.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NX is X+1", "NY is Y+1"]))
list.append(ActionCase("right", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NX is X+1", "NY is Y-1"]))
list.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,Y)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NX is X-1"]))
list.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NX is X-1", "NY is Y+1"]))
list.append(ActionCase("left", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NX is X-1", "NY is Y-1"]))
list.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,X,NY)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NY is Y+1"]))
list.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NY is Y+1", "NX is X+1"]))
list.append(ActionCase("up", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NY is Y+1", "NX is X-1"]))
list.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,X,NY)"], ["at(N,X,Y)"], ["N"], 0.5, 1, ["NY is Y-1"]))
list.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 2, ["NY is Y-1", "NX is X+1"]))
list.append(ActionCase("down", ["at(N,X,Y)"], ["at(N,NX,NY)"], ["at(N,X,Y)"], ["N"], 0.25, 3, ["NY is Y-1", "NX is X-1"]))

failCondition = "\t( member(at(R1,X,Y),State)," \
                "\n\tmember(at(R2,X,Y),State)," \
                "\n\tR1 \= R2); " \
                "\n\t( member(at(N,X,Y),State)," \
                "\n\t (X<0 ; X>" + str(size-1) + "; Y<0; Y>" + str(size-1) +") ).\n"

#mas = MAS(list, failCondition, "[at(1,0,2),at(2,4,2)]", ["right(1)","left(2)","right(1)","left(2)"])
satisfiesBody = "\tmember(at(1,X,Y),State),\n\tmember(at(2,X,Y),State)."


def visualizeState(state):
    dict = {}
    #Change sizeOfGrid for representations of other grid sizes.
    sizeOfGrid = 8
    temp = re.split(',|\(|\)', state)

    i = 1
    while(i < len(temp)):
        dict[temp[i]] = (temp[i+1], temp[i+2])
        i+=5

    matrix = [[0 for k in range(sizeOfGrid)] for l in range(sizeOfGrid)]
    for key in dict:
        value = dict[key]
        if(matrix[int(value[1])][int(value[0])] == 0):
            matrix[int(value[1])][int(value[0])] = int(key)
        else:
            matrix[int(value[1])][int(value[0])] = 9

    for k in range(sizeOfGrid):
        print()
        for l in range(sizeOfGrid):
            print(matrix[k][l], end = '')
    print()
    # plt.figure(figsize=(6, 6))
    # plt.axis('off')
    # cmap = colors.ListedColormap(['White', 'red', 'yellow'])
    # plt.pcolor(matrix[::-1], cmap=cmap, edgecolors='k', linewidths=2)
    # plt.show()

mas = MAS(list, failCondition, "[at(1,0,3),at(2,7,4)]", ["right(1)", "left(2)", "right(1)", "left(2)", "right(1)", "left(2)"], satisfiesBody, visualizeState, 4)

resultOfMas = mas.run()
print("Endstate after executing plan: " + str(resultOfMas[0]))
print("List of times needed to calculate probabilities: " + str(resultOfMas[2]))

plt.figure(figsize=(6,6))
plt.plot(resultOfMas[2])
plt.title("Evolutie uitvoeringstijd met windowsize 4")
plt.ylabel("Uitvoeringstijd in seconden")
plt.xlabel("Aantal stappen gezet in het plan")
plt.show()