import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels
import graphics
with open('G:/Algoritmi e programmazione/Progetto/Dati/dpc-covid19-ita-province.json') as f:
         d = json.load(f) 

Series = pd.Series(d)

#Creating raw DataFrame
d1 = pd.DataFrame(d)

datanoe = '2020-06-17T17:00:00'

row = len(d1.index)-1
while d1['data'][row] != datanoe:
    row -= 1
d1 = d1[:row+1]

#Removing fake data
toremove = []
for row in d1.index:
    if d1['lat'][row] == 0:
        toremove.append(row) #saving fake rows
d1 = d1.drop(toremove) #dropping fake rows
d1 = d1.reset_index(drop = True) #updating indexes

#Creating a list of unique 'province', 'regioni', lat' and 'long' 
row = 0
day0 = d1["data"][0]
column_prov = []
column_reg = []
column_lat = []
column_long = []
while d1["data"][row] == day0:
    column_prov.append(d1["sigla_provincia"][row])
    column_reg.append(d1["denominazione_regione"][row])
    column_lat.append(d1["lat"][row])
    column_long.append(d1["long"][row])
    row += 1

myMI = pd.DataFrame({'regioni':column_reg, 'province': column_prov, 
                     'lat':column_lat, 'long':column_long})
#Creating a list of unique dates
dates = []
for i in range(0, len(d1.index),len(column_prov)):
    dates.append(d1["data"][i])
    myMI[d1["data"][i]] = np.nan

myMI.set_index(['regioni', 'province'], inplace = True) 
myMI = myMI.sort_index()

myMI.iloc[20:30][dates[10:12]]
myMI.loc[('Toscana', 'FI')][dates[80:85]]

#Creating a TimeSeries
dates_TS = pd.DatetimeIndex(dates)
myTS = pd.DataFrame(index = dates_TS, columns = column_prov)
dailyincr = pd.DataFrame(index = dates_TS[1:], columns = column_prov) #Increment matrix

myTS.loc[myTS.index[:5]]
  
for r in d1.index:
    myTS[d1['sigla_provincia'][r]][d1['data'][r]] = d1['totale_casi'][r]
    myMI[d1['data'][r]][(d1['denominazione_regione'][r], d1['sigla_provincia'][r])] = d1['totale_casi'][r]

for i in range(1,len(myTS)):
    dailyincr.values[i-1] = myTS.values[i] - myTS.values[i-1]


myTS.values
myMI.loc['Calabria'].index
dailyincr.values

#Totale casi per regione il 2020-03-15T17:00:00
myMI.groupby('regioni')[dates[20]].sum()

#Creating three areas based on Napoli and Bologna latitudes
area = pd.cut(myMI['lat'], 
              [ min(myMI['lat']), myMI.loc[('Campania', 'NA')]['lat'], 
              myMI.loc[('Emilia-Romagna', 'BO')]['lat'], max(myMI['lat'])],
               include_lowest = True, 
               labels = ['Sud', 'Centro', 'Nord'])

area.loc['Emilia-Romagna']
#Totale cases by  geographic area at 2020-03-15T17:00:00
myMI.groupby(area)[dates[20]].sum()

import matplotlib as mpl
%matplotlib inline

myTS[list(myMI.loc['Toscana'].index)].plot()
myTS[list(myMI.loc['Lombardia'].index)].plot()
myTS[list(myMI.loc['Sardegna'].index)].plot()

dailyincr[list(myMI.loc['Toscana'].index)].plot()
dailyincr[list(myMI.loc['Lombardia'].index)].plot()
dailyincr[list(myMI.loc['Sardegna'].index)].plot()

#Daily increase for Italy
dailyincr.sum(axis = 1).plot()
autocorrelation_plot(dailyincr.sum(axis = 1))


from statsmodels.graphics.tsaplots import plot_acf
#ACF plot for totals
plot_acf(dailyincr.sum(axis = 1), lags=20, unbiased = True, title = 'Italy Autocorrelation')