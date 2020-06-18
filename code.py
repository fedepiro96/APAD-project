import json
import networkx as nx
import numpy as np

with open('/home/noe/Università/in_corso/Algoritmi/APAD-project/dati/dati-json/dpc-covid19-ita-province.json') as f:
    d = json.load(f)

# print(len(d))
# print(type(d))  #list
# print(type(d[1])) #dictionary

# print(d)

P = nx.Graph()
dist = {}
for record in d:                                                # per ogni osservazione
    if record['lat']!=0 and record['long']!=0:                  # elimino i record sbagliati
        if record['denominazione_provincia'] not in list(P.nodes):
            P.add_node(record['denominazione_provincia'])
            dist[record['denominazione_provincia']] = {'long' : record['long'], 'lat': record['lat']}
print(list(P.nodes))
print(dist)

for i in dist:
    print(dist[i]['lat'])
def graph_builder(data, d=0.8):
    return None