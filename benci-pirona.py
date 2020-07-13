import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import timeit 
from random import randrange
import random 
from collections import deque

with open('./Data/dpc-covid19-ita-province.json') as f:
         d = json.load(f) 


# removing false records
today = d[len(d)-1].get("data")

begin = len(d)-1
while d[begin].get("data") == today:
    begin -= 1
newd = d[begin:]

# Each node corresponds to a city and two cities a and b are connected by an
# edge if the following holds: if x,y is the position of a, then b is in
# position z,w with z in [x-d,x+d] and w in [y-d, y+d], with d=0.8. The graph
# is symmetric. Use the latitude and longitude information available in the
# files to get the position of the cities. This task can be done in several
# ways. Use the one you think is more efficient.


def set_nodes(data=newd):
    """
    Given the data set (list of dictionaries), it builds the "province" Graph
    where nodes are provinces and their attributes are relative latitude and 
    longitude
    """
    G = nx.Graph()
    for i in range(len(data)):
        if data[i].get("lat") != 0: 
            G.add_node(data[i]["sigla_provincia"], lat=data[i]["lat"],
                       long=data[i]["long"])
    return G


P = set_nodes(data=newd)
# %timeit (set_nodes(P))
# 90.7 µs ± 2.93 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

def nearbyatt(v, w, att, d = .8):
    """
    Given two nodes, a distance d and an attribute att, it returns True if
    nodes attribute differs less than d
    """
    return abs(v[att] - w[att]) < d

def ordered_attr(G = P, att = "lat"):
    """
    Given a graph and a node attribute, it returns a list of nodes in
    ascending order by the attribute 
    """
    dic = nx.get_node_attributes(G, att)   # Ottengo dic con chiavi prov, values lat
    sort = sorted(dic, key=dic.get)        # Province ordinate in base a latitudine
    return sort
# %timeit ordered_attr(P, "lat")
# 61.8 µs ± 3.13 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


sortlat = ordered_attr(P, "lat")

def set_edges(G=P, ordered=sortlat, dist=.8):
    """
    Given a Graph, a list of (ordered) nodes and a distance dist, it adds
    edges to the Graph if two nodes latitude and longitude differ less than 
    dist
    """
    n_1 = len(ordered) - 1
    i, j = 0, 1
    while i < n_1:
        if nearbyatt(G.nodes[ordered[i]], G.nodes[ordered[j]], d=dist, att='lat'):
            if nearbyatt(G.nodes[ordered[i]], G.nodes[ordered[j]], d=dist, att='long'):
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


set_edges(P)
P.number_of_edges()
# %timeit (set_edges(P))
# 4.66 ms ± 270 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
nx.draw(P, with_labels=True, node_size=40, font_size=10, ax=ax)
# plt.savefig('P Graph')

def set_edges2(G=P, dist=.8):
    """
    Given a Graph, a list of (ordered) nodes and a distance dist, it adds
    edges to the Graph if two nodes latitude and longitude differ less than 
    dist. An edge between v and w is added if w is near to v by latitude and by
    longitude
    """  
    sortlat = ordered_attr(G, "lat")
    sortlong = ordered_attr(G, "long")
    for n in G.nodes:
        neigh_lat = find_neigh(G, nodelist = sortlat, node = n, dist = dist, att = 'lat')
        neigh_long = find_neigh(G, nodelist = sortlong, node = n, dist = dist, att = 'long')
        intersec = intersection(neigh_lat, neigh_long)
        for neigh in intersec:
            G.add_edge(n, neigh)
    return 

def find_neigh(G, nodelist, node, dist, att):
    """
    Given a Graph, one node of it and a nodal attribute, it returns a list
    of nodes near to the node by attribute
    """
    i = nodelist.index(node)
    j, k =  i-1, i+1
    n = len(nodelist) - 1 
    nbs = []
    while j >= 0 and nearbyatt(G.nodes[nodelist[i]], G.nodes[nodelist[j]], d = dist, att = att ):
        nbs.append(nodelist[j])
        j -= 1
    while k <= n and nearbyatt(G.nodes[nodelist[i]], G.nodes[nodelist[k]], d = dist, att = att):
        nbs.append(nodelist[k])
        k += 1
    return nbs
    
def intersection(l1, l2):
    """
    Given two lists, it returns a list with an intersection of the elements
    of them, using a similar method to the sorting in MergeSort
    """
    l1.sort()
    l2.sort()
    i = j = 0
    inter = []
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            i += 1
        elif l1[i] > l2[j]:
            j += 1
        else:
            inter.append(l1[i])
            i += 1
            j += 1
    return inter


PP = set_nodes(data=newd)
set_edges2(PP)
len(PP.edges)
# % timeit set_edges2(PP)
# 10.7 ms ± 359 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


def set_edges3(G=P, dist=.8):
    """
    A trivial version of set_edges function, to add edges to the graph G
    """
    nodes = list(G.nodes)
    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            if nearbyatt(G.nodes[nodes[i]], G.nodes[nodes[j]], att='lat', d=dist) and nearbyatt(G.nodes[nodes[i]], G.nodes[nodes[j]], att='long', d=dist):
                G.add_edge(nodes[i], nodes[j])
    return


PPP = set_nodes(data = newd)
set_edges3(PPP)
len(PPP.edges)
# %timeit (set_edges3(PPP))
# 12 ms ± 965 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

def random_generator(lower, upper):
    """
    Random generator for latitude and longitude
    """
    while True: 
        yield lower + random.random()*(upper - lower)

def random_graph(n):
    """
    It builds a list of dictionaries similar to original data; every dictionary
    has three keys: "sigla_provincia", "lat" and "long".
    """
    node_list = []
    x = random_generator(30,50)
    y = random_generator(10,20)
    for i in range(n):
        node_list.append({"sigla_provincia": i, "lat": next(x), "long": next(y)})
    return node_list


n = 2000
random.seed(1)
random_data = random_graph(n)

R = set_nodes(data = random_data)
# %timeit set_nodes(data = random_data)
# 1.85 ms ± 78 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

sortlat2 = ordered_attr(R, "lat")
set_edges(G = R, ordered = sortlat2, dist = .08)
len(R.edges)

# %timeit ordered_attr(R, "lat")
# 1.33 ms ± 60.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# %timeit set_edges(R, sortlat2, dist = .08)
# 66.8 ms ± 3.61 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


nx.draw_random(R, node_size = 10)
# plt.savefig('R graph')

RR = set_nodes(data = random_data)
set_edges2(RR, dist = .08)
len(RR.edges)
# %timeit set_edges2(RR)
# 2.72 s ± 114 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

RRR = set_nodes(data = random_data)
set_edges3(RRR, dist = .08)
# %timeit set_edges3(RRR)
# 3.75 s ± 89.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


# The cost of the function set_Edges and set_Edges2 should belong to the same
# Order of magnitude O(nlogn) because of the sorting cost. However set_Edges
# seems to perform faster than set_Edges2 according to timeit module.
# The cost of the function set_Edges3 is instead O(n^2) because every node is
# compared to every other n-1 nodes

def distance(v, w):
    """
    It returns the Euclidean Distance from node v to node w, based on their
    values of latitude and longitude
    """
    return ((v["lat"] - w["lat"])**2 + (v["long"] - w["long"])**2)**.5 

def set_distances(G = P):
    """
    Given a graph G, it adds as edges attribute the Euclidean Distance
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

# Drawing weighted Graph P
pos = nx.layout.spring_layout(P)

M = P.number_of_edges()
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
edge_colors = [d*1.5 for d in nx.get_edge_attributes(P, 'distance').values()]
edge_cmap = plt.cm.YlOrRd
nodes = nx.draw_networkx_nodes(P, pos, node_size=20)
nx.draw_networkx_labels(P, pos, font_size=8, font_family='sans-serif', ax=ax)
edges = nx.draw_networkx_edges(P, pos, edge_color=edge_colors, 
                               edge_cmap=edge_cmap,  
                               width=2)

sm = plt.cm.ScalarMappable(cmap=edge_cmap, norm=plt.Normalize(vmin=min(nx.get_edge_attributes(P, 'distance').values()),
                                                              vmax=max(nx.get_edge_attributes(P, 'distance').values())))

sm._A = []
plt.colorbar(sm)
plt.axis('off')
plt.show()
# plt.savefig('P Weighted Graph')

# Drawing Weighted Graph R
pos = nx.layout.random_layout(R)

M = R.number_of_edges()
fig, ax = plt.subplots(1, 1, figsize = (10, 10))
edge_colors = [d*1.5 for d in nx.get_edge_attributes(R, 'distance').values()]
edge_cmap=plt.cm.YlOrRd
nodes = nx.draw_networkx_nodes(R, pos, node_size=20)
# nx.draw_networkx_labels(R, pos, font_size=8, font_family='sans-serif', ax = ax )
edges = nx.draw_networkx_edges(R, pos, edge_color=edge_colors, 
                               edge_cmap=edge_cmap,  
                               width=2)

sm = plt.cm.ScalarMappable(cmap=edge_cmap, norm=plt.Normalize(vmin=min(nx.get_edge_attributes(R, 'distance').values()),
                                                              vmax=max(nx.get_edge_attributes(R, 'distance').values())))

sm._A = []
plt.colorbar(sm)
plt.axis('off')
plt.show()
# plt.savefig('R Weighted Graph')

#### Global Indices and Structures:
#### Counting Triangles

def sorted_degree(G):
    """
    Given a graph G, it calculates the degree for each node
    and it returns a list of nodes sorted by degree
    """
    nodes = list(G.nodes())
    deg = {}
    for n in nodes:
        deg[n] = len(G[n])
    return deg, sorted(deg, key=deg.get)

def passes(v, w, degree):
    """
    It Checks if the degree of v is less than the degree of w;
    if are equal it checks which node is smaller alphabetically
    """
    return degree[v] < degree[w] or (degree[v] == degree[w] and v < w)
# print(sort_deg, degree)

def triangles_discover(G):
    """
    Given a graph G, this function returns the list of all triangles of G
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
triangles_count_P = len(triangles_discover(P))
# print(triangles_count_P)
# 352

triangles_list_R = triangles_discover(R)
triangles_count_R = len(triangles_discover(R))
# print(triangles_count_R)
# 12


# %timeit (triangles_discover(P))
# 1.01 ms ± 51.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# %timeit (triangles_discover(R))
# 4.52 ms ± 194 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

# %timeit sum(nx.triangles(P).values())/3
# 2.29 ms ± 138 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# %timeit sum(nx.triangles(R).values())/3
# 14 ms ± 1.17 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)

#### Centralities:
#### Eccentricity

def ecc(start, graph):
    """Given a graph and a vertex v of the graph, it returns the eccentricity 
    of v
    """
    level = {}
    color = {}
    for v in graph.nodes:
        level[v] = float('inf')
        color[v] = 'white'
    queue = deque([start])
    color[start] = 'no_white' 
    level[start] = 0
    while queue:
        v = queue.popleft()
        for n in graph[v]:
            if color[n] == 'white':            
                queue.append(n)
                level[n] = level[v] + 1
                color[n] = 'no_white'
    maxlev = max(level.values())
    return maxlev

   
p = nx.subgraph(P, max(nx.connected_components(P), key=len))
r = nx.subgraph(R, max(nx.connected_components(R), key=len))

nx.set_node_attributes(p, None, "eccentricity")
nx.set_node_attributes(r, None, "eccentricity")

for node in list(p.nodes()):
    p.nodes[node]["eccentricity"] = ecc(graph=p, start=node)

for node in list(r.nodes()):
    r.nodes[node]["eccentricity"] = ecc(graph=r, start=node)    

# %timeit for node in list(p.nodes()): p.nodes[node]["eccentricity"] = ecc(graph=p, start=node)
# 63.3 ms ± 5.3 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# %timeit for node in list(r.nodes()):r.nodes[node]["eccentricity"] = ecc(graph=r, start=node)
# 236 µs ± 20.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

star_graph = nx.star_graph(4)
nx.draw(star_graph)

for node in list(star_graph.nodes()):
    star_graph.nodes[node]["eccentricity"] = ecc(graph=star_graph, start=node)
nx.get_node_attributes(star_graph, "eccentricity").values()

