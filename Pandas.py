import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime
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

d1['data'] = pd.to_datetime(d1['data']).dt.date #alcune ore differiscono da df regione


#Creating a list of unique 'province', 'regioni', lat' and 'long' 
row = 0
day0 = d1["data"][0]
column_prov = []
column_reg = []
column_lat = []
column_long = []
column_dates = []
while d1["data"][row] == day0:
    column_prov.append(d1["sigla_provincia"][row])
    column_reg.append(d1["denominazione_regione"][row])
    column_lat.append(d1["lat"][row])
    column_long.append(d1["long"][row])
    column_dates.append(d1['data'][row])
    row += 1

MI = d1.set_index(['denominazione_regione', 'sigla_provincia', 'data'])
MI.sort_index(inplace = True)
column_dates = pd.DatetimeIndex(column_dates)
myMI = pd.DataFrame({'regioni':column_reg, 'province': column_prov,  'date': column_dates,
                     'lat':column_lat, 'long':column_long})
#Creating a list of unique dates
dates = []
for i in range(0, len(d1.index),len(column_prov)):
    dates.append(d1["data"][i])
    myMI[d1["data"][i]] = np.nan

myMI.set_index(['regioni', 'province', 'date'], inplace = True) 
myMI = myMI.sort_index()

myMI.iloc[20:30]
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

from pandas.plotting import autocorrelation_plot
autocorrelation_plot(dailyincr.sum(axis = 1))
#dashed 99%, continous 95%

from statsmodels.graphics.tsaplots import plot_acf
#ACF plot for totals
plot_acf(dailyincr.sum(axis = 1), lags=20, unbiased = True, title = 'Italy Autocorrelation')



##############################################################################

with open('G:/Algoritmi e programmazione/Progetto/Dati/dpc-covid19-ita-regioni.json') as f:
         d = json.load(f) 


datanoe = '2020-06-17T17:00:00'
row = len(d)-1
while d[row]['data'] != datanoe:
    row -= 1
d = d[:row+1]
d2 = pd.DataFrame(d)

d2['data'] = pd.to_datetime(d2['data']).dt.date
b = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01', '2020-05-01', '2020-06-01'])
l = range(1,4)
d2['new'] = pd.cut(d2['data'], bins=b, labels=l, include_lowest=True)
d2.pivot_table('terapia_intensiva', index='denominazione_regione', columns='data')
periodo = pd.cut(d2['data'], ['2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01'])
mese = list(pd.DatetimeIndex(d2['data']).month)
monthsdic = {2: '2;Febbraio', 3: '3;Marzo', 4: '4;Aprile', 5:'5;Maggio', 6:'6;Giugno'}
mese = [ monthsdic[n] for n in mese ]
d2['mese'] = mese
zone = ['1;Nord-Ovest', '2;Nord-Est', '3;Centro', '4;Sud', '5;Isole']

areageodic = {'Abruzzo': zone[2], 'Basilicata': zone[3], 'Calabria': zone[3], 
              'Campania':zone[3], 'Emilia-Romagna':zone[1], 
              'Friuli Venezia Giulia':zone[1], 'Lazio': zone[2], 
              'Liguria':zone[0], 'Lombardia':zone[0], 
              'Marche': zone[2], 'Molise':zone[3], 'P.A. Bolzano':zone[1], 
              'P.A. Trento':zone[1], 'Piemonte': zone[0], 'Puglia':zone[3],
              'Sardegna':zone[4], 'Sicilia':zone[4], 'Toscana': zone[2],
              'Umbria': zone[2], 'Valle d\'Aosta':zone[0], 
              'Veneto':zone[1]}
area_geografica = [ areageodic[n] for n in d2.denominazione_regione ]
d2['area_geografica'] = area_geografica
d2.pivot_table('terapia_intensiva', index='area_geografica', columns='mese')

tamponi_qcut = pd.qcut(d2['tamponi'], 3, labels = ['Pochi', 'Normali', 'Tanti'])
d2.pivot_table('totale_casi', index = 'area_geografica', columns = 'tamponi_qcut')
d2.set_index(['data', 'denominazione_regione'], inplace =True)
d2.sort_index(inplace = True)
d2.loc['2020-06-16']['tamponi']

cols_1 = ['codice_provincia', 'data', 'denominazione_provincia', 'denominazione_regione', 'lat', 'long', 'sigla_provincia']
mergione = pd.merge(d1[cols_1], d2, on = ['denominazione_regione', 'data'], suffixes = ["_prov", "_reg"])
mergione.set_index(['denominazione_regione','sigla_provincia', 'data'], inplace = True) #faccio index
mergione.sort_index(inplace=True)
mergione.index
mergione.shape
d1.shape
d2.shape
mergione.columns

mergione.iloc(1)
mergione.data


d2

#Creating a list of unique 'province', 'regioni', lat' and 'long' 

columns = ['data', 'denominazione_regione', 'deceduti', 'dimessi_guariti', 
           'isolamento_domiciliare', 'nuovi_positivi', 'ricoverati_con_sintomi',
           'tamponi', 'terapia_intensiva', 'totale_casi', 'totale_ospedalizzati',
           'totale_positivi', 'variazione_totale_positivi']
df = pd.DataFrame(index = range(len(d)), columns = columns)
for i in range(len(d)):
    riga = {}
    for n in range(len(columns)):
        riga[columns[n]] = d[i][columns[n]]
    df.loc[i] = riga 
    
   
df.data = pd.DatetimeIndex(df.data)
dates = list(set(df.data))
dates.sort()
regions = list(set(df.denominazione_regione))
regions.sort()
df.set_index(['data', 'denominazione_regione'], inplace = True) 
df = df.sort_index()

df.loc[dates[40]]['tamponi']
df.loc[(dates[40], 'Toscana')]
df.loc[dates[40:45]]['tamponi']
df.loc['2020-06-05 17:00:00']['tamponi']

#Division by zero problem
letalità = list(np.repeat(np.nan, len(df.index)))
for i in range(len(df.index)):
    if df.iloc[i]['totale_casi'] != 0:
        letalità[i] = df.iloc[i]['deceduti'] / df.iloc[i]['totale_casi']
df['letalità'] = letalità


letal = {}
for d in dates:
    letal[d] = []
for i in df.index:
    letal[i[0]].append(df.loc[i]['letalità'])
letal = pd.DataFrame(letal).transpose()
letal.columns = regions

import matplotlib as mpl
%matplotlib inline
letal.plot(legend = False, colormap='gist_rainbow')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))


nuovi_deceduti = list(np.repeat(np.nan, len(regions)))
for i in range(len(regions), len(df.index)):
    nuovi_deceduti.append(df.iloc[i]['deceduti'] - df.iloc[i-21]['deceduti'])
df['nuovi_deceduti'] = nuovi_deceduti

boxplot = df.boxplot(column = 'nuovi_positivi', by = 'denominazione_regione', rot = 90)
a = df.loc[dates[40]]
a.plot(x = 'dimessi_guariti', y = 'ricoverati_con_sintomi', style = '.', logy = True,
       xlim = (0,15000), ylim = (10, 15000))
df.loc[dates[40]]['ricoverati_con_sintomi']
