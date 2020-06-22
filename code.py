import json
import networkx as nx
import numpy as np
import timeit 
import random 
with open('G:/Algoritmi e programmazione/Progetto/APAD-project/dpc-covid19-ita-province.json') as f:
         d = json.load(f) 

type(d)  #list
type(d[1]) #dictionary
today = d[len(d)-1].get("data")

#Lista di dizionari, eliminare province farlocche e date antecedenti a 16 giugno
#Notare che gli elementi di d sono ordinati per data (in fondo i più recenti)
begin = len(d)-1
while d[begin].get("data") == today:
    begin -= 1
newd = d[begin:]

#Each node corresponds to a city and two cities a and b are connected by an 
#edge if the following holds: if x,y is the position of a, then b is in 
#position z,w with z in [x-d,x+d] and w in [y-d, y+d], with d=0.8. The graph 
#is symmetric. Use the latitude and longitude information available in the 
#files to get the position of the cities. This task can be done in several 
#ways. Use the one you think is more efficient.

P = nx.Graph()
def set_nodes(G = P, data = newd):
    for i in range(len(data)):
        if data[i].get("lat") != 0: 
            G.add_node(newd[i]["sigla_provincia"], lat = newd[i]["lat"], 
                       long = newd[i]["long"])
    return

set_nodes(P)
#%timeit (set_nodes(P))
#90.7 µs ± 2.93 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
P.nodes["FI"]
P.nodes["FI"]["lat"]

def nearlat(v, w, d = .8):
    return abs(v["lat"] - w["lat"]) < d

def nearlong(v, w, d = .8):
    return abs(v["long"] - w["long"]) < d



nearlat(P.nodes["FI"], P.nodes["AR"])
dic = nx.get_node_attributes(P, "lat") #Ottengo dic con chiavi prov, values lat
sortlat = sorted(dic, key= dic.get) #Province ordinate in base a latitudine
#%timeit (sorted(dic, key= dic.get))
#12.4 µs ± 132 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

def set_edges(G = P, ordered = sortlat, dist = .8):
    n_1 = len(ordered) -1
    i, j = 0,1
    while i < n_1:
        if nearlat(G.nodes[ordered[i]], G.nodes[ordered[j]], d = dist):
            if nearlong(G.nodes[ordered[i]], G.nodes[ordered[j]], d = dist):
                G.add_edge(ordered[i], ordered[j])
            if j < n_1:
                j += 1
            else:
                i += 1
                j = i+1
        else:
            i += 1
            j = i+1
    return

#%timeit (set_edges(G))
#4.53 ms ± 523 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
set_edges(P)    
P.number_of_edges()


def set_edges2(G = P, dist = .8):
    nodes = list(G.nodes)
    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            if nearlat(G.nodes[nodes[i]], G.nodes[nodes[j]], dist) and  nearlong(G.nodes[nodes[i]], G.nodes[nodes[j]], dist):
                G.add_edge(nodes[i], nodes[j])
    return

#%timeit (set_edges2(G)) 
#11.3 ms ± 1.18 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
set_edges2(P)


#Generate 2000 pairs of double (x,y) with x in [30,50) and y in [10,20).
help(random.random)
random.seed(1)
x = y = []
for i in range(2000):
    x.append(30 + 20*random.random())
for j in range(2000):
    y.append(10 + 10*random.random())


#Repeat the algorithm at step 1, building a graph R using NetworkX where each 
#pair is a node and two nodes are connected with the same rule reported above, 
#still with d=0.08. If the algorithm at step 1 takes too long, repeat step 1. 
#Note that here d=0.08 (and not 0.8 as in the previous item), as in this way 
#the resulting graph is sparser.
R = nx.Graph()
set_nodes(R)
set_edges(G = R, ordered = sortlat, dist = .20)
R.nodes["AQ"]


def distance(v, w):
    return ((v["lat"] - w["lat"])**2 + (v["long"] - w["long"])**2)**.5 

def set_distances(G = P):
    edges = list(G.edges)
    distances = {}
    for edge in edges:
        distances[edge] = {"distance": distance(G.nodes[edge[0]], G.nodes[edge[1]])}
    nx.set_edge_attributes(G, distances)
    return
        
        
       # G.edges[nodes[i], nodes[j]]["weight"] = distance(G.nodes[nodes[i]], G.nodes[nodes[j]])
            
set_distances(P)
set_distances(R)







from collections import deque
def ecc(graph, start):
    queue = deque([start])
    level = {start: 0}
    while queue:
        v = queue.popleft()
        for n in graph[v]:
            if n not in level:            
                queue.append(n)
                level[n] = level[v] + 1
    maxlev = max(level.values())
    if maxlev > 0:
        return maxlev
    else:
        return None
    
    
nx.set_node_attributes(P, None, "eccentricity")
nx.set_node_attributes(R, None, "eccentricity")
for node in list(P.nodes):
    P.nodes[node]["eccentricity"] = ecc(graph = P, start = node)
    R.nodes[node]["eccentricity"] = ecc(graph = R, start = node)
