from pulp import*
import math
from collections import defaultdict
import csv

num_patient = 14
num_nurse= 5
num_vertex= 15
num_info = 6
num_tw = 2
M = 1000
speed = 40
#data = [[0 for x in range(num_vertex)] for y in range(num_info)]


with open('test1.csv', newline='') as data:
    reader = csv.reader(data)
    data = list(reader)

distance = [[0.0, 3.09, 6.291, 2.476, 15.725, 4.89, 4.802, 4.144, 7.153, 6.808, 6.611, 9.017, 3.197, 2.033, 1.795],
             [3.09, 0.0, 9.019, 5.478, 12.873, 5.207, 7.691, 7.158, 10.081, 9.447, 9.622, 5.928, 5.754, 3.227, 3.36],
             [6.291, 9.019, 0.0, 5.256, 20.051, 6.368, 1.652, 2.633, 1.622, 0.655, 2.074, 14.679, 3.268, 7.94, 7.604],
             [2.476, 5.478, 5.256, 0.0, 18.201, 6.566, 3.603, 2.644, 5.594, 5.885, 4.841, 11.363, 3.228, 3.052, 2.717],
             [15.725, 12.873, 20.051, 18.201, 0.0, 13.732, 19.326, 19.19, 21.54, 20.184, 21.424, 7.975, 17.187, 16.04, 16.214],
             [4.89, 5.207, 6.368, 6.566, 13.732, 0.0, 5.94, 6.146, 7.923, 6.457, 7.972, 9.352, 4.005, 6.763, 6.607],
             [4.802, 7.691, 1.652, 3.603, 19.326, 5.94, 0.0, 1.001, 2.391, 2.286, 2.097, 13.498, 2.146, 6.338, 5.998],
             [4.144, 7.158, 2.633, 2.644, 19.19, 6.146, 1.001, 0.0, 3.053, 3.277, 2.469, 13.047, 2.145, 5.498, 5.155],
             [7.153, 10.081, 1.622, 5.594, 21.54, 7.923, 2.391, 3.053, 0.0, 1.887, 0.952, 15.884, 4.474, 8.541, 8.198],
             [6.808, 9.447, 0.655, 5.885, 20.184, 6.457, 2.286, 3.277, 1.887, 0.0, 2.545, 15.023, 3.701, 8.514, 8.181],
             [6.611, 9.622, 2.074, 4.841, 21.424, 7.972, 2.097, 2.469, 0.952, 2.545, 0.0, 15.494, 4.241, 7.85, 7.508],
             [9.017, 5.928, 14.679, 11.363, 7.975, 9.352, 13.498, 13.047, 15.884, 15.023, 15.494, 0.0, 11.439, 8.694, 8.94],
             [3.197, 5.754, 3.268, 3.228, 17.187, 4.005, 2.146, 2.145, 4.474, 3.701, 4.241, 11.439, 0.0, 5.089, 4.782],
             [2.033, 3.227, 7.94, 3.052, 16.04, 6.763, 6.338, 5.498, 8.541, 8.514, 7.85, 8.694, 5.089, 0.0, 0.343],
             [1.795, 3.36, 7.604, 2.717, 16.214, 6.607, 5.998, 5.155, 8.198, 8.181, 7.508, 8.94, 4.782, 0.343, 0.0]]



nodeData0 = {}

for i in range(len(data)):
    temp = []
    for h in range(len(data[i])):
        temp.append(float(data[i][h]))

    nodeData0[str(i)] = temp

(ID, lowerbound1, upperbound1, lowerbound2, upperbound2,duration,skill, gender, language) = splitDict(nodeData0)

####################################################################SETS
N = [i for i in range(num_vertex)]            #all nodes
P = [i for i in range(1, num_vertex)]
C = [k for k in range(num_nurse)]
W1={}
W1 = defaultdict(list)
for d in (lowerbound1, lowerbound2): # you can list as many input dicts as you want here
    for key, value in d.items():
        W1[key].append(value)
W2={}
W2 = defaultdict(list)
for d in (upperbound1, upperbound2): # you can list as many input dicts as you want here
    for key, value in d.items():
        W2[key].append(value)
W1W2= [k for k in range(2)]
pn = {"0": [1,1,1], "1": [1,1,1], "2": [1,1,1], "3": [1,1,1], "4": [1,1,1]}
pp = {}
pp = defaultdict(list)
for d in (skill, gender, language): # you can list as many input dicts as you want here
    for key, value in d.items():
        pp[key].append(value)

##############################################################
travel_time = [[0 for x in range(num_vertex)] for y in range(num_vertex)]
for i in N:
    for j in N:
        travel_time[i][j] = (distance[i][j] / speed)
        travel_time[i][j] = math.floor((travel_time[i][j]*100))/100

#################################################################################################################
# decision variables are defined

Xijk = LpVariable.dicts("X",(N,N,C), 0, 1, LpBinary)
Zik = LpVariable.dicts("Z", (N,C), 0, 1, LpBinary)  # Z_ik
Sik = LpVariable.dicts("S", (N,C), 0, None, LpContinuous)  # S_ik
Viq = LpVariable.dicts("V", (N,W1W2), 0, 1, LpBinary)

##############################################
prob = LpProblem("const", LpMinimize)
##############################################
# OBJECTIVE FUNCTION
prob += lpSum(travel_time[i][j] * Xijk[i][j][k] for i in N for j in N for k in C)

######################################################################################################################
#constranints
#number2
for j in P:
    prob += lpSum(Xijk[i][j][k] for i in N for k in C if i!=j) == 1
#number3
for k in C:
    for j in P:
        prob += lpSum(Xijk[i][j][k] for i in N) - Zik[j][k] == 0

#number5 (same as ap)
for k in range(num_nurse):
    prob += lpSum(Xijk[0][j][k] for j in P) - lpSum(Xijk[j][0][k] for j in P) == 0

for k in C:
    prob += lpSum(Xijk[0][j][k] for j in P) <= 1
#number6
for k in range(num_nurse):
    for j in P:
        prob += lpSum(Xijk[i][j][k] for i in N) - lpSum(Xijk[j][i][k] for i in N) == 0
#number7
for k in C:
    prob += lpSum(Xijk[0][j][k] for j in P) <= num_nurse
#number8
#kk= W1[str(1)][1]
for k in range(num_nurse):
    for i in N:
        for q in W1W2:
            prob += Sik[i][k] + M * (1 - Zik[i][k]) + M*(1-Viq[i][q]) >= W1[str(i)][q]

#number9
for k in range(num_nurse):
    for i in N:
        for q in W1W2:
            prob += Sik[i][k] - M * (1 - Zik[i][k]) - M*(1-Viq[i][q]) <= W2[str(i)][q]
#number10
for i in P:
    prob += lpSum(Viq[i][q] for q in W1W2) == 1

#number11
for k in range(num_nurse):
    for i in N:
        for j in P:
            prob += Sik[i][k] + travel_time[i][j] + duration[str(i)] - Sik[j][k] <= M * (1 - Xijk[i][j][k])
for k in range(num_nurse):
    for i in P:
        if ((pn[str(k)][0] != (pp[str(i)][0])) or (pn[str(k)][1] != (pp[str(i)][1]))
                or (pn[str(k)][2] != (pp[str(i)][2]))):
            prob += lpSum(Zik[i][k]) == 0

#######################################################################################################################
prob.writeLP("small.wide.lp")
print("CPLEX")
prob.solve(solver = CPLEX_CMD())

#writing the results in a txt file
f = open("response.txt", "w+")
f.write("%s = %s\n" % ("Status:", LpStatus[prob.status]))
f.write("%s = %s\n" % ("OBJ Function:",(pulp.value(prob.objective))))
#print("Status:", LpStatus[prob.status])
#print(pulp.value(prob.objective))
for v in prob.variables():
    if v.varValue != 0:
        f.write("%s = %s\n" % (v.name, v.varValue))
l = 0
f.close()