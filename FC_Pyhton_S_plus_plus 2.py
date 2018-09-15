# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 00:55:23 2018

@author: Rene Planteu
"""
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import time as timefun
import os
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
import scipy as sp
from matplotlib import cm
from matplotlib.figure import figaspect
import matplotlib.colors as colors

script_dir = os.path.dirname(__file__)
rel_pathCurr = "Messdaten/20180315_Test_curr.dat"          # Hier das auszulesende curr 
                                                # file eingeben 
SaveCurr = rel_pathCurr[10:-4]
CurrDat = os.path.join(script_dir, rel_pathCurr)


rel_pathTemp = "Messdaten/20180104_Temp_mitAkku.dat"          # Hier das auszulesende temp 
                                                # file eingeben 

SaveTemp = rel_pathTemp[10:-4]


TempDat = os.path.join(script_dir, rel_pathTemp)

### Auslesen von Zeit, Spannung und Strom ####

f = open(CurrDat)                    
AusCurr = ('Ergebnis_'+SaveCurr+'.txt')                 # Dateiname curr                               
volt = []
current = []
lines = []
for line in f:
    lines.append(line)
f.close()

g = open(TempDat)                     # Hier das auszulesende  temp
                                                # file eingeben 
AusTemp = ('Ergebnis_'+SaveTemp+'.txt')                 # Dateiname temp                                   
voltB = []
currentB = []
linesB = []
for line in g:
    linesB.append(line)
g.close()

timeA = float(lines[1])                         # Beginnzeit in sec. curr
timeC = float(linesB[1])                        # Beginnzeit in sec. temp

"""
Stamp = (timefun.strftime("%Y_%m_%d_%H_%M_"))   # Datumsstempel für die 
                                                # Ausgabedatei curr
StampB = (timefun.strftime("%Y_%m_%d_%H_%M_"))  # Datumsstempel für die 
                                                # Ausgabedatei temp                                            
"""                                                
skip = 18                                       # Anzahl der Zeilen bis 
                                                # naechster Datensatz curr      
skipB = 10                                      # Anzahl der Zeilen bis 
                                                # naechster Datensatz temp
data = {}
dataB = {}
data['current'] = []
data['voltage'] = []
dataB['temp'] = []
data['time'] = []
dataB['time'] = []


##### Auslesen und Abspeichern Current #####

f = open(AusCurr,'w')        

for i in range(0,len(lines),skip):
    #current
    start = i + 7                               # 1. Zeile mit Stromwerten
    end = start + 10                            # Letze Zeile mit Sromwerten
    L = lines[start:end]
    rows = len(L)
    cols = len(L[0].split('\t'))
    curr = ''
    for row in range(0,rows):
        dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
        curr += dummy +';'
    data['current'].append(curr[:-1])

    #voltage
    start = i + 4                               #1. Zeile mit Spannungswerten
    volt = lines[start]
    volt = float(volt)
    volt = abs(volt)
    volt = format(volt,'.4f')                   # 4.f = eine Nachkomma
    data['voltage'].append(volt) 

    #time 
    start = i + 1
    time = lines[start]
    time = float(time)
    time = format((time -timeA),'.1f')          # 1.f = eine Nachkomma
    data['time'].append(time)
    
    stringline = str(time) + ';' + str(volt) +';'+ curr +'\n'
    f.write(stringline)

print ('Current ausgelesen')

f.close()

##### Auslesen und Abspeichern Temperature #####

g = open(AusTemp,'w')

for i in range(0,len(linesB),skipB):
    #temp
    start = i + 4
    end = start + 5
    L = linesB[start:end]
    rows = len(L)
    cols = len(L[0].split('\t'))
    temp = ''
    for row in range(0,rows):
        dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
        temp += dummy +';'
    dataB['temp'].append(temp[:-1])


    #time 
    start = i + 1
    timeB = linesB[start]
    timeB = float(timeB)
    timeB = format((timeB -timeC),'.1f') 
    dataB['time'].append(timeB)
    
    stringline = str(timeB) +';'+ temp +'\n'
    g.write(stringline)

print ('Temp ausgelesen')

g.close()


######## plot a 3D Current ########

#p=13000

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')

X = sp.linspace(0,10,10)
Y = sp.linspace(0,10,10)

X, Y = sp.meshgrid(X, Y)
X, Y = X.ravel(), Y.ravel()

#R = sp.sqrt(X**2 + Y**2)
#Z = sp.sin(R)

width = depth = 1
bottom=X*0.

#plt.ion()

place=0
current_floats=sp.float64(data['current'][place].split(";")).reshape(10,10)
print sp.mean(current_floats)
currsum= str(round(sp.sum(current_floats),1))
top=current_floats.ravel()
top_scaled=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
mycolors = cm.jet(top_scaled)
ax.bar3d(X, Y, bottom, width, depth, top,color=mycolors)
ax.set_title('Partial Currents @ '+currsum+'A')

ax.set_zlim(0,100)
ax.set_zlabel('Current in A')
ax.view_init(elev=25., azim=60)


plt.show()

#fig.canvas.draw()

#plt.pause(0.5)

#plt.clf()

######## plot 3D Temperature ########

#p=13000

fig2 = plt.figure(figsize=plt.figaspect(0.5))
ax2 = fig2.add_subplot(1, 2, 1, projection='3d')

X2 = sp.linspace(0,5,5)
Y2 = sp.linspace(0,5,5)

X2, Y2 = sp.meshgrid(X2, Y2)
X2, Y2 = X2.ravel(), Y2.ravel()

#R = sp.sqrt(X**2 + Y**2)
#Z = sp.sin(R)

width = depth = 1
bottom=X*0.

#plt.ion()

p=1
temp_floats=sp.float64(dataB['temp'][p].split(";")).reshape(5,5)
mintemp= np.min(temp_floats)
mintemptxt = str(round(mintemp,1))
top=temp_floats.ravel()-mintemp+0.5
top_scaled2=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
mycolors = cm.jet(top_scaled2)
surf2=ax2.bar3d(X2, Y2, bottom, width, depth, top,color=mycolors)
ax2.set_title('Temperature @ '+currsum+' A')

ax2.set_zlim(0,1.5)
ax2.set_zlabel('Temperature +'+mintemptxt+'°C')
ax2.view_init(elev=25., azim=60)

plt.show()

print ('Danke das Sie FC_Python benutzt haben (c)RPl&CHa')