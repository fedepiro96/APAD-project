# APAD-project
Project of exam 'Algorithms and Programming for data Analysis'.

# Project Assignment
## Setup

Data about Covid19 with respect to our country, Italy.
Let’s start: download the data available at https://github.com/pcm-dpc/COVID-19. In particular, clone the Git repository locally.

In a cell of Jupiter or in a script load the data as follows.

import json

with open('dpc-covid19-ita-province.json') as f:

         d = json.load(f)

## Building the graphs
Next steps are reported in the file benci-pirona.py https://github.com/fedepiro96/APAD-project/blob/master/benci-pirona.py

- Build the graph of provinces P using NetworkX.
  - Each node corresponds to a city and two cities a and b are connected by an edge if the following holds: if x,y is the position of a, then b is in position z,w with z in [x-d,x+d] and w in [y-d, y+d], with d=0.8. The graph is symmetric. Use the latitude and longitude information available in the files to get the position of the cities. This task can be done in several ways. Use the one you think is more efficient.
  - Generate 2000 pairs of double (x,y) with x in [30,50) and y in [10,20).
- Repeat the algorithm at step 1, building a graph R using NetworkX where each pair is a node and two nodes are connected with the same rule reported above, still with d=0.08. If the algorithm at step 1 takes too long, repeat step 1. Note that here d=0.08 (and not 0.8 as in the previous item), as in this way the resulting graph is sparser.
- Both P and R can be seen as weighted graphs putting on each edge the distance between the two cities.
- Modify P and R to weight their edges.
- Counting triangles: http://timroughgarden.org/s14/l/l1.pdf;
  Eccentricity centrality https://en.wikipedia.org/wiki/Distance_(graph_theory);
  - Read the related articles
  - implement the corresponding algorithm in python using NetworkX
  - apply them both to P and R
- Prepare slides (file benci-pirona.pdf)(the presentation will last 15 minutes per person) explaining the chosen algorithms, your implementations, and their applications to a toy example.

## Pandas
Next steps are reported in the notebook benci-pirona.ipynb https://github.com/fedepiro96/APAD-project/blob/master/benci-pirona.ipynb

Until now we have only used the name of the cities and their corresponding position. We now use the remaining data.

- Familiarize with the data (especially its tree structure)
- Write down a quick summary (git commits history, collaborators and maintainers, what it contains and whatever you observe).
-Data: https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-regioni.json and its companion at https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-province.json
- Load both of them in two different Python objects and inspect their contents, write down your thoughts and observations of their structure. You can both use plain Python dictionaries (for a preliminary step) and Pandas dataframes (required).
- Describe data using Pandas features and provide some plots according to your intuition (start small following the examples that we had done together); also, feel free to explore some connections you find interesting.
- Provide visualizations such as plots, box-plots and scatter matrices (have a look at https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html  for inspiration). The more combination you explore the better, in the sense to combine in the same figure multiple subplots or data series.
The two files are correlated in the sense that the second adds details to the first. Figure out the connections and build new Pandas dataframes that use hierarchy indexes. Also perform some interesting marginalizations you like to report.
For instance, we expect to see a dataframe that is indexed by an outermost level of regions and an inner level of provinces; accordingly, the rows should report data with respect to this index.
The more graphics, descriptions and Pandas manipulation you experiment the better.
All the previous points have to be collected in a Jupyter notebook, nicely prepared with a very short bio of the author(s) and a sequence of cells that interleave documentation and code; don’t forget to describe the environment you work in.
You can use the interpreter and environment that best suit your needs, justify and report them clearly in the notebook. Btw, we will redo your notebook using the official interpreter from https://www.python.org/downloads/ and Jupyter from pip).
Do easy steps and justify them to move over more complex ones. Describe how you design your work and comment your code in order to give us the opportunity to read your manuscript from top to bottom without “interruptions” due to reverse-engineering what you have done (of course we will review together in the oral session of the exam).
