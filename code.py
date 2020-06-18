import json
import networkx as nx

with open('G:/Algoritmi e programmazione/Progetto/Dati/dpc-covid19-ita-province.json') as f:
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

n = len(newd)
copy = newd[:]
for i in range(n):
    if copy[i].get("lat") == 0:
       newd.pop(i)

len(newd)   #107, sembra corretto

