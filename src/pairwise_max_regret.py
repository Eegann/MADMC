# -*- coding: utf-8 -*-

from gurobipy import *

def computePMR(x,y):
    m = Model("Pairwise Max Regret")
    m.setParam("OutputFlag",0)
    w=[]
    for i in range(len(x)):
        w.append(m.addVar(vtype=GRB.CONTINUOUS))
    for i in range(len(w)):
        m.addConstr(w[i] >= 0)
    m.addConstr(quicksum(w[i] for i in range(len(w))) <= 1)
    
    m.setObjective(quicksum(w[i] * y[i] for i in range(len(w))) - quicksum(w[i] * x[i] for i in range(len(w))), GRB.MAXIMIZE)

    m.optimize()
    
    obj = m.getObjective()

    return obj.getValue()
