import json
import networkx as nx
import numpy as np
import timeit 
from random import randrange
import random 
from collections import deque

with open('G:/Algoritmi e programmazione/Progetto/APAD-project/dpc-covid19-ita-province.json') as f:
         d = json.load(f) 

today = d[len(d)-1].get("data")

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


def set_nodes(data = newd):
    """given the dataset (list of dictionaries), it builds the "province" Graph
    where nodes are provinces and their attributes are relative latitude and 
    longitude
    """
    G = nx.Graph()
    for i in range(len(data)):
        if data[i].get("lat") != 0: 
            G.add_node(data[i]["sigla_provincia"], lat = data[i]["lat"], 
                       long = data[i]["long"])
    return G

P = set_nodes(data = newd)
#%timeit (set_nodes(P))
#90.7 µs ± 2.93 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


def nearlat(v, w, d = .8):
    """given two nodes and a distance d, it returns True if nodes latitude 
    differs less than d
    """
    return abs(v["lat"] - w["lat"]) < d

def nearlong(v, w, d = .8):
    """given two nodes and a distance d, it returns True if nodes longitude 
    differs less than d
    """
    return abs(v["long"] - w["long"]) < d

def ordered_attr(G = P, att = "lat"):
    """Given a graph and a node attribute, it returns a list of nodes in 
    ascending order by the attribute 
    """
    dic = nx.get_node_attributes(G, att) #Ottengo dic con chiavi prov, values lat
    sort = sorted(dic, key= dic.get) #Province ordinate in base a latitudine
    return sort
#%timeit (sorted(dic, key= dic.get))
#12.4 µs ± 132 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

sortlat = ordered_attr(P, "lat")

def set_edges(G = P, ordered = sortlat, dist = .8):
    """Given a Graph, a list of (ordered) nodes and a distance dist, it adds 
    edges to the Graph if two nodes latitude and longitude differ less than 
    dist
    """
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
    """A trivial version of set_edges fuunction, to add edges to the graph G
    """
    nodes = list(G.nodes)
    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            if nearlat(G.nodes[nodes[i]], G.nodes[nodes[j]], dist) and  nearlong(G.nodes[nodes[i]], G.nodes[nodes[j]], dist):
                G.add_edge(nodes[i], nodes[j])
    return

#%timeit (set_edges2(G)) 
#11.3 ms ± 1.18 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)




def generate_x():
    """Random generator for latitude
    """
    while True:
        r = randrange(30, 49)
        eps = random.random()
        yield r+eps

def generate_y():
    """Random generator for longitude
    """
    while True:
        r = randrange(10, 19)
        eps = random.random()
        yield r+eps



def random_graph(n):
    """It builds a list of dictionaries similar to original data; every dictionary 
    has three keys: "sigla_provincia", "lat" and "long".
    """
    node_list = []
    x = generate_x()
    y = generate_y()
    for i in range(n):
        node_list.append({"sigla_provincia": i, "lat": next(x), "long": next(y)})
    return node_list

n = 2000
random.seed(1)
random_data = random_graph(n)

random_P = set_nodes(data = random_data)
sortlat2 = ordered_attr(random_P, "lat")
set_edges(random_P, sortlat2, dist = .8)
len(random_P.edges)

random_R = set_nodes(data = random_data)
set_edges(random_R, sortlat2, dist = .08)
len(random_R.edges)

R = set_nodes()
set_edges(G = R, dist = .08)


def distance(v, w):
    """It returns the Euclidean Distance from node v to node w, based on their
    values of latitude and longitude
    """
    return ((v["lat"] - w["lat"])**2 + (v["long"] - w["long"])**2)**.5 

def set_distances(G = P):
    """Given a graph G, it adds as edges attribute the Euclidean Distance 
    for all edges in G
    """
    edges = list(G.edges)
    distances = {}
    for edge in edges:
        distances[edge] = {"distance": distance(G.nodes[edge[0]], G.nodes[edge[1]])}
    nx.set_edge_attributes(G, distances)
    return
        
set_distances(P)
set_distances(R)

####Global Indices and Structures:
####Counting Triangles

def sorted_degree(G):
    """Given a graph G, it calculates the degree for each node
    and it returns a list of nodes sorted by degree
    """
    nodes = list(G.nodes())
    deg = {}
    for n in nodes:
        deg[n] = len(G[n])
    return deg, sorted(deg, key=deg.get)

def passes(v, w, degree):
    """It Checks if the degree of v is less than the degree of w;
    if are equal it checks which node is smaller alphabetically
    """
    return degree[v] < degree[w] or (degree[v] == degree[w] and v < w)
# print(sort_deg, degree)

def triangles_discover(G):
    """Given a graph G, this function returns the list of all triangles of G
    """
    degree, sort_deg = sorted_degree(G)
    triangles = []
    for node in sort_deg:
        near = list(G.neighbors(node))
        for i in range(len(near)-1):
            if passes(node, near[i], degree):
                for j in range(i+1, len(near)):
                    if passes(node, near[j], degree) and near[j] in G.neighbors(near[i]):
                        triangles.append((node, near[i], near[j]))
    return triangles


triangles_list_P = triangles_discover(P)
print(triangles_list_P)
triangles_count_P = len(triangles_discover(P))
print(triangles_count_P)

triangles_list_R = triangles_discover(R)
print(triangles_list_R)
triangles_count_R = len(triangles_discover(R))
print(triangles_count_R)


#%timeit (triangles_discover(P))
#1.2 ms ± 97.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



####Centralities:
####Eccentricity

nx.node_connected_component(P, "FI")
P.graph['largest_cc'] = max(nx.connected_components(P), key=len)
R.graph['largest_cc'] = max(nx.connected_components(R), key=len)
   
def ecc(graph, start):
    """Given a graph and a vertex v of the graph, it returns the eccentricity 
    of v
    """
    if start in P.graph['largest_cc']:
        queue = deque([start])
        level = {start: 0}
        while queue:
            v = queue.popleft()
            for n in graph[v]:
                if n not in level:            
                    queue.append(n)
                    level[n] = level[v] + 1
        maxlev = max(level.values())
        return maxlev
    else:
        return float('inf')
   
P.graph['largest_cc'] = max(nx.connected_components(P), key=len)
p = nx.subgraph(P, P.graph['largest_cc'])
R.graph['largest_cc'] = max(nx.connected_components(R), key=len)
r = nx.subgraph(R, R.graph['largest_cc'])

nx.set_node_attributes(P, None, "eccentricity")
nx.set_node_attributes(R, None, "eccentricity")

for node in list(p.nodes()):
    p.nodes[node]["eccentricity"] = ecc(graph=P, start=node)

for node in list(r.nodes()):
    r.nodes[node]["eccentricity"] = ecc(graph=R, start=node)    
    





