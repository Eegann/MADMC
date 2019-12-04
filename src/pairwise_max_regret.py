# -*- coding: utf-8 -*-

from gurobipy import *

def computePMR(x,y):
    m = Model("Pairwise Max Regret")
    w=[]
    for i in range(len(x)):
        w.append(m.addVar(vtype=GRB.CONTINUOUS))
    for i in range(len(w)):
        m.addConstr(w[i] <= 1)
        m.addConstr(w[i] >= 0)
    m.addConstr(quicksum(w[i] for i in range(len(w))) <= 1)
    
    m.setObjective(quicksum(w[i] * y[i] for i in range(len(w))) - quicksum(w[i] * x[i] for i in range(len(w))), GRB.MAXIMIZE)

    m.optimize()
    
    obj = m.getObjective()
    
    print(w[0].X,w[1].X)
    
    pritn(obj.getValue())