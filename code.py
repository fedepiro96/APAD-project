import json
import networkx as nx
import numpy as np

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


G = nx.Graph()
for i in range(len(newd)):
    if newd[i].get("lat") != 0: 
       G.add_node(newd[i]["sigla_provincia"], lat = newd[i]["lat"], 
                  long = newd[i]["long"])

G.nodes["FI"]
G.nodes["FI"]["lat"]

def nearlat(v, w, d = .8):
    return abs(v["lat"] - w["lat"]) < d

def nearlong(v, w, d = .8):
    return abs(v["long"] - w["long"]) < d



nearlat(G.nodes["FI"], G.nodes["AR"])
dic = nx.get_node_attributes(G, "lat") #Ottengo dic con chiavi prov, values lat
sortlat = sorted(dic, key= dic.get) #Province ordinate in base a latitudine



def set_edges(G, ordered = sortlat):
    n = len(ordered) -1
    i, j = 0,1
    while i < n:
        if nearlat(G.nodes[ordered[i]], G.nodes[ordered[j]]):
            if nearlong(G.nodes[ordered[i]], G.nodes[ordered[j]]):
                G.add_edge(ordered[i], ordered[j])
            if j < n:
                j += 1
            else:
                i += 1
        else:
            i += 1
            j = i+1
    return
    
set_edges(G)    
G.number_of_edges()

    

