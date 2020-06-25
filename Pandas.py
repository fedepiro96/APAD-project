import json
import pandas as pd
import numpy as np


with open('G:/Algoritmi e programmazione/Progetto/Dati/dpc-covid19-ita-province.json') as f:
         d = json.load(f) 

Series = pd.Series(d)

#Creating raw DataFrame
df = pd.DataFrame(d)


#Removing fake data
toremove = []
for row in df.index:
    if df['lat'][row] == 0:
        toremove.append(row) #saving fake rows
df = df.drop(toremove) #dropping fake rows
df = df.reset_index(drop = True) #updating indexes

#Creating a list of unique 'province' and a list of tuples(regioni, province)
row = 0
day0 = df["data"][0]
column_prov = []
column_reg = []
while df["data"][row] == day0:
    column_prov.append(df["sigla_provincia"][row])
    column_reg.append(df["denominazione_regione"][row])
    row += 1

myMI = pd.DataFrame({'regioni':column_reg, 'province': column_prov})
#Creating a list of unique dates
dates = []
for i in range(0, len(df.index),len(column_prov)):
    dates.append(df["data"][i])
    myMI[df["data"][i]] = np.nan
dates_TI = pd.DatetimeIndex(dates)


myMI.set_index(['regioni', 'province'], inplace = True)
#myMI.reindex([column_reg, column_prov]) 
myMI = myMI.sort_index()

myMI.loc[('Abruzzo', 'CH')]

myTS = pd.DataFrame(index = dates_TI, columns = column_prov)
dailyincr = pd.DataFrame(index = dates_TI[1:], columns = column_prov)


  
for r in df.index:
    myTS[df['sigla_provincia'][r]][df['data'][r]] = df['totale_casi'][r]
    myMI[df['data'][r]][(df['denominazione_regione'][r], df['sigla_provincia'][r])] = df['totale_casi'][r]
myTS.values
myMI.loc['Calabria']

for i in range(1,len(myTS)):
    dailyincr.values[i-1] = myTS.values[i] - myTS.values[i-1]

