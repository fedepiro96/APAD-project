import json
import networkx as nx
import numpy as np

with open('/home/noe/Università/in_corso/Algoritmi/APAD-project/dati/dati-json/dpc-covid19-ita-province.json') as f:
    d = json.load(f)

lats = {}
longs = {}
for record in d:                                                # per ogni osservazione
    if record['lat'] != 0 and record['long'] != 0:              # elimino i record sbagliati
        if record['sigla_provincia'] not in lats.keys():        # memorizzo solo la provincia e la sua lat e long
            lats[record['sigla_provincia']] = record['lat']     # in due dizionari lats e longs
            longs[record['sigla_provincia']] = record['long']

prov_sort = sorted(lats, key=lats.get)

def graph_builder(node_list_sort, lat, long, dist):
    """It build a graph nodes are cities contained in node_list_sort
    two cities are linked if their lats and longs are nearer than d.
    node_list_sort: list of cities sorted by latitudes
    lat: dictionary where each node (key) is associated to its latitude
    long: dictionary where each node (key) is associated to its longitude"""
    G = nx.Graph()
    i = 0
    j = 1
    while i <= (len(node_list_sort)-1):
        G.add_node(node_list_sort[i])
        if j <= (len(node_list_sort)-1) and abs(lat[node_list_sort[i]] - lat[node_list_sort[j]]) < dist:
            if abs(long[node_list_sort[i]] - long[node_list_sort[j]]) < dist:
                G.add_edge(node_list_sort[i], node_list_sort[j])
                j += 1
            else:
                j += 1
        else:
            i += 1
            j = i + 1
    return G


P = graph_builder(prov_sort, lats, longs, dist=0.8)
print(P.nodes())
print(P.edges())
print(len(P.edges()))

from random import random
from random import randrange
print(randrange(30, 49))

def generate_x():
    """Random generator for latitude"""
    while True:
        r = randrange(30, 49)
        eps = random()
        yield r+eps

def generate_y():
    """Random generator for longitude"""
    while True:
        r = randrange(10, 19)
        eps = random()
        yield r+eps

def random_graph(n):
    """It build:
    - a list of nodes with length n;
    - a dictionary where each node (key) is associated to a random latitude;
    - a dictionary where each node (key) is associated to a random longitude;
    The function exploits two generator for latitude and longitude"""
    node_list = []
    lat = {}
    long = {}
    x = generate_x()
    y = generate_y()
    for i in range(n):
        node_list.append(i)
        lat[i] = next(x)
        long[i] = next(y)
    return node_list, lat, long


rand_nodes, rand_lat, rand_long = random_graph(2000)

rand_graph1 = graph_builder(sorted(rand_lat, key=rand_lat.get), rand_lat, rand_long, dist=0.8)
print(rand_graph1.nodes())
print(rand_graph1.edges())
print(len(rand_graph1.edges()))

R = graph_builder(prov_sort, lats, longs, dist=0.08)
print(R.nodes())
print(R.edges())
print(len(R.edges()))

rand_graph2 = graph_builder(sorted(rand_lat, key=rand_lat.get), rand_lat, rand_long, dist=0.08)
print(rand_graph2.nodes())
print(rand_graph2.edges())
print(len(rand_graph2.edges()))








