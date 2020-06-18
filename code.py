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

for record in d:                                                # per ogni osservazione
    if record['lat']!=0 and record['long']!=0:                  # elimino i record sbagliati
        for provincia in list(P.nodes):                         # per ogni nodo nella lista dei nodi
            if record['denominazione_provincia']!=provincia:    # se non
            P.add_node(record['denominazione_provincia'])


print(list(P.nodes))

def graph_builder(data, d=0.8):
    return None