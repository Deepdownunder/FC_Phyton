# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 09:15:20 2018

@author: Rene
"""

import Tkinter as tk
from Tkinter import *
import tkFileDialog
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import time as ts
import os
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
import scipy as sp
from matplotlib import cm
from matplotlib.figure import figaspect
import matplotlib.colors as colors


def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def importURL_Curr():    
    currurl = tkFileDialog.askopenfilename(initialdir = "r'C:/Projektlabor_2/FC_Python",title = "Select file",filetypes = (("current files","*.dat"),("all files","*.*")))
    
    currread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current geladen"     
    displaystate.insert(tk.END, currread+'\n')
    
    return currurl
   
def displayURL_curr():
    displayURL_curr.curr_URL = importURL_Curr()
    
    curr_data_display = displaycurrent
    curr_data_display.insert(tk.END, displayURL_curr.curr_URL)

def importURL_Temp():    
    tempurl = tkFileDialog.askopenfilename(initialdir = "r'C:/Projektlabor_2/FC_Python",title = "Select file",filetypes = (("current files","*.dat"),("all files","*.*")))
    
    tempread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperatur geladen"   
    displaystate.insert(tk.END, tempread+'\n')    
    
    return tempurl
   
def displayURL_temp():
    displayURL_temp.temp_URL = importURL_Temp()
    
    temp_data_display = displaytemp
    temp_data_display.insert(tk.END, displayURL_temp.temp_URL)

def savepath():
    savepath.path= tkFileDialog.askdirectory()    
    
    displaypath.delete(1.0, END)
    displaypath.insert(tk.END, savepath.path[20:])
    pathread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Path ausgewaehlt"   
    displaystate.insert(tk.END, pathread+'\n')     
    
    
def read_Curr():
    f = open(displayURL_curr.curr_URL)
    SaveCurr = displayURL_curr.curr_URL[38:-4]                       
    AusCurr = (savepath.path+'/'+'Ergebnis_'+SaveCurr+'.txt')                 # Dateiname curr                               
    volt = []
    current = []
    lines = []
    rows = 0
    for line in f:
        lines.append(line)
        print line
        if 'current' in line:
            rows += 1
    f.close()

    timeA = float(lines[1]) 
    skip = int(entryCurrJump.get()) #17
    
    read_Curr.data = {}
    read_Curr.data['current'] = []
    read_Curr.data['voltage'] = []
    read_Curr.data['time'] = []
    #read_Curr.data =['currentsum']    
    
    f = open(AusCurr,'w')
    #init step
    start = int(entryCurrStart.get())-1    
    end = int(entryCurrEnd.get())
    L = lines[start:end]
    cols = len(L[0].replace('\n','').replace('\t',';').replace(' ','').split(';'))
    cols = cols*len(L)    
    
    currents = np.zeros((rows,cols))
    
    nr = -1
    for i in range(0,len(lines),skip):
        nr += 1
        #current
        start = i + int(entryCurrStart.get())-1                       # 1. Zeile mit Stromwerten
        end = i + int(entryCurrEnd.get())                            # Letze Zeile mit Sromwerten
        L = lines[start:end]
        rows = len(L)
        #cols = len(L[0].split('\t'))
        curr = []
        curr_str = ''
        for row in range(0,rows):
            dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
            curr += dummy.split(';')
            curr_str = curr_str + dummy + ';'
        
        currents[nr,:] = curr        
        read_Curr.data['current'].append(curr_str[:-1])
               
        #Sum of Current in line
        sumcurr= np.sum(currents[nr,:])
        
        #voltage
        start = i + int(entryVoltStart.get())-1#4                               #1. Zeile mit Spannungswerten
        volt = lines[start]
        volt = float(volt)
        volt = abs(volt)
        volt = format(volt,'.4f')                   # 4.f = eine Nachkomma
        read_Curr.data['voltage'].append(volt) 
    
        #time sec since start
        start = i + 1
        time = lines[start]
        time = float(time)
        time = format((time -timeA),'.1f')          # 1.f = eine Nachkomma
        read_Curr.data['time'].append(time)
        
        #Current sum in row
        #start = i + int(entryCurrStart.get()) #7                               # 1. Zeile mit Stromwerten
        #end = start + int(entryCurrEnd.get())#10  
        #L = lines[start:end] 
        #rows = len(L)
        #for row in range(0,rows):
            #currs = L[row].replace('\n','').replace('\t',';').replace(' ','') 
            #print(currs)
            #currsfloat =sp.float64(currs[row].split(";"))           
            
            #print(repr(currsfloat))
        #currsum=np.sum(currsfloat, axis=1).tolist()
        #print(currsum)        
        
        stringline = str(time) + ';' + str(volt) +';'+ curr_str + str(sumcurr)+';' +'\n'
        f.write(stringline)
    
    currdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current eingelesen"   
    displaystate.insert(tk.END, currdone+'\n')       
    
    f.close()

def read_Temp():
 
    g = open(displayURL_temp.temp_URL)                      
    SaveTemp=displayURL_temp.temp_URL[38:-4]    
    AusTemp = (savepath.path+'/'+'Ergebnis_'+SaveTemp+'.txt')                                                    
    voltB = []
    currentB = []
    linesB = []
    for line in g:
        linesB.append(line)
    g.close()
   
    timeC = float(linesB[1]) 
    skipB = int(entryTempJump.get()) #10
    
    read_Temp.dataB = {}
    read_Temp.dataB['temp'] = []
    read_Temp.dataB['time'] = []
   
    g = open(AusTemp,'w')
    
    for i in range(0,len(linesB),skipB):
        #temp
        start = i + int(entryTempStart.get())-1 #4
        end = i+ int(entryTempEnd.get()) -1#5
        L = linesB[start:end]
        rows = len(L)
        cols = len(L[0].split('\t'))
        temp = ''
        for row in range(0,rows):
            dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
            temp += dummy +';'
        read_Temp.dataB['temp'].append(temp[:-1])
    
    
        #time 
        start = i + 1
        timeB = linesB[start]
        timeB = float(timeB)
        timeB = format((timeB -timeC),'.1f') 
        read_Temp.dataB['time'].append(timeB)
        
        stringline = str(timeB) +';'+ temp +'\n'
        g.write(stringline)
    
    print ('Temp ausgelesen')
    
    
    tempdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature eingelesen"
    displaystate.insert(tk.END, tempdone+'\n')    
    
    
    g.close()



def plot_curr():
    ######## plot a 3D Current ########
        
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
    getrow=int(entryrowplot.get())
    current_floats=sp.float64(read_Curr.data['current'][getrow].split(";")).reshape(10,10)
    maxcurr= np.max(current_floats)
    currsum = str(round(np.sum(current_floats)))
    #print sp.mean(current_floats)
    top=current_floats.ravel()
    top_scaled=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
    mycolors = cm.jet(top_scaled)
    ax.bar3d(X, Y, bottom, width, depth, top,color=mycolors)
    ax.set_title('Partial Currents @ '+currsum+' A')
    
    ax.set_zlim(0,maxcurr)
    ax.set_zlabel('Current in A', linespacing=10.4)
    ax.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))
    
    plt.show()
    
    currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current dargestellt"
    displaystate.insert(tk.END, currplot+'\n')    
    
def plot_temp():
    ######## plot 3D Temperature ########
    
    
    fig2 = plt.figure(figsize=plt.figaspect(0.5))
    ax2 = fig2.add_subplot(1, 2, 1, projection='3d')
    
    X2 = sp.linspace(0,5,5)
    Y2 = sp.linspace(0,5,5)
    
    X2, Y2 = sp.meshgrid(X2, Y2)
    X2, Y2 = X2.ravel(), Y2.ravel()
    
    #R = sp.sqrt(X**2 + Y**2)
    #Z = sp.sin(R)
    
    width = depth = 1
    bottom=X2*0
    
    #plt.ion()
    
    p=int(entryrowplot.get())
    temp_floats=sp.float64(read_Temp.dataB['temp'][p].split(";")).reshape(5,5)
    mintemp= np.min(temp_floats)
    mintemptxt = str(round(mintemp,1))
    top=temp_floats.ravel()-mintemp+0.5
    top_scaled2=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
    mycolors = cm.jet(top_scaled2)
    ax2.bar3d(X2, Y2, bottom, width, depth, top,color=mycolors)
    ax2.set_title('Temperature')
    
    ax2.set_zlim(0,top)
    ax2.set_zlabel('Temperature +'+mintemptxt+'°C')
    ax2.view_init(elev=25., azim=60)
    
    plt.show()
    
    tempplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature dargestellt"
    displaystate.insert(tk.END, tempplot+'\n')

root = Tk()
root.title("FC Python")
root.geometry("900x450")
root.wm_iconbitmap(r'C:\Projektlabor_2\FC_Python\GUI\FCPy_win7.ico')
labelsize1=40
labelsize2=5
labelsize3=30
labelsize4=80
textalign = "w"
textalign2="e"
stick=W
stick2=E

####-------Labels------####
Curr_sel = tk.Label(text="Selected Current Data:",width=labelsize1,anchor=textalign)
Curr_sel.grid(column=0, row=0)
Temp_sel = tk.Label(text="Selected Temp Data:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=1)
Temp_sel = tk.Label(text="Selected Storage Path:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=3)
labelCurrStart=tk.Label(text="1st row of current data in *.dat: (8)", width=labelsize1,anchor=textalign )
labelCurrStart.grid(column=0, row=6)
labelEnd=tk.Label(text="Last row of current data in *.dat: (17)", width=labelsize1,anchor=textalign)
labelEnd.grid(column=0, row=7)
labelVoltStart=tk.Label(text="1st row of voltage data in *.dat: (5)", width=labelsize1,anchor=textalign)
labelVoltStart.grid(column=0, row=8)
labelrowplot=tk.Label(text="Which row do you want to plot? (0-xxxxxxx)", width=labelsize1,anchor=textalign)
labelrowplot.grid(column=0, row=9)
labelEvalCurr=tk.Label(text="Elevation of plot view: (25)", width=labelsize1,anchor=textalign )
labelEvalCurr.grid(column=0, row=10)
labelAngleCurr=tk.Label(text="Angle of plot view: (60)", width=labelsize1,anchor=textalign )
labelAngleCurr.grid(column=0, row=11)
labelTempStart=tk.Label(text="1st row of temp data in *.dat: (4)", width=labelsize1,anchor=textalign )
labelTempStart.grid(column=2, row=6)
labelTempEnd=tk.Label(text="Last row of temp data in *.dat: (5)", width=labelsize1,anchor=textalign )
labelTempEnd.grid(column=2, row=7)
labelJumpCurr=tk.Label(text="Number of rows between current data: (18)", width=labelsize1,anchor=textalign )
labelJumpCurr.grid(column=2, row=8)
labelJumpTemp=tk.Label(text="Number of rows between temperature data: (10)", width=labelsize1,anchor=textalign )
labelJumpTemp.grid(column=2, row=9)
labelEvalTemp=tk.Label(text="Elevation of plot view(Temp): (25)", width=labelsize1,anchor=textalign )
labelEvalTemp.grid(column=2, row=10)
labelAngleTemp=tk.Label(text="Angle of plot view(Temp): (60)", width=labelsize1,anchor=textalign )
labelAngleTemp.grid(column=2, row=11)


####----- Buttons -----#####
button_currD = tk.Button(text="Load Current", command=displayURL_curr)
button_currD.grid(sticky=stick, column=2, row=0)
button_tempD = tk.Button(text="Load Temp", command=displayURL_temp)
button_tempD.grid(sticky=stick,column=2, row=1)
button_path = tk.Button(text="Storage path", command=savepath)
button_path.grid(sticky=stick,column=2, row=3,)
button_temp = tk.Button(text="Read Temp", command=read_Temp)
button_temp.grid(sticky=stick2,column=0, row=12)
button_curr = tk.Button(text="Read Current", command=read_Curr)
button_curr.grid(sticky=stick, column=0, row=12)
button_plcurr = tk.Button(text="Plot Current_row", command=plot_curr)
button_plcurr.grid(sticky=stick, column=2, row=12)
button_pltemp = tk.Button(text="Plot Temperature", command=plot_temp)
button_pltemp.grid(sticky=stick2, column=2, row=12)
button_plcurr = tk.Button(text="Plot Current_sum", command=plot_curr)
button_plcurr.grid(sticky=stick, column=2, row=13)

###-----text------#####
displaycurrent=tk.Text(master=root, height = 1, width = labelsize3 )
displaycurrent.grid(column=1, row=0)
displaytemp=tk.Text(master=root, height = 1, width = labelsize3)
displaytemp.grid(column=1, row=1)
displaypath=tk.Text(master=root, height = 1, width =labelsize3)
displaypath.grid(column=1, row=3)
displaystate=tk.Text(master=root, height = 20)
displaystate.grid(column=0, row=16, columnspan=3)




#####------Entrys------#######
var1 = StringVar(root, value="8")
var2 = StringVar(root, value="17")
var3 = StringVar(root, value="5")
var4 = StringVar(root, value="5")
var5 = StringVar(root, value="9")
var6 = StringVar(root, value="18")
var7 = StringVar(root, value="10")
var8 = StringVar(root, value="1")
var9 = StringVar(root, value="25")
var10 = StringVar(root, value="60")
var11 = StringVar(root, value="25")
var12 = StringVar(root, value="60")

entryCurrStart=tk.Entry(width=labelsize2, textvariable=var1)
entryCurrStart.grid(sticky=stick, column=1, row=6)
entryCurrEnd=tk.Entry(width=labelsize2, textvariable=var2)
entryCurrEnd.grid(sticky=stick,column=1, row=7)
entryVoltStart=tk.Entry(width=labelsize2, textvariable=var3)
entryVoltStart.grid(sticky=stick,column=1, row=8)
entryrowplot=tk.Entry(width=labelsize2,textvariable=var8)
entryrowplot.grid(sticky=stick,column=1, row=9)
entryTempStart=tk.Entry(width=labelsize2, textvariable=var4)
entryTempStart.grid(sticky=stick2, column=1, row=6)
entryTempEnd=tk.Entry(width=labelsize2, textvariable=var5)
entryTempEnd.grid(sticky=stick2,column=1, row=7)
entryCurrJump=tk.Entry(width=labelsize2, textvariable=var6)
entryCurrJump.grid(sticky=stick2,column=1, row=8)
entryTempJump=tk.Entry(width=labelsize2, textvariable=var6)
entryTempJump.grid(sticky=stick2,column=1, row=9)
entryCurrEval=tk.Entry(width=labelsize2, textvariable=var9)
entryCurrEval.grid(sticky=stick,column=1, row=10)
entryCurrAngle=tk.Entry(width=labelsize2, textvariable=var10)
entryCurrAngle.grid(sticky=stick,column=1, row=11)
entryTempEval=tk.Entry(width=labelsize2, textvariable=var11)
entryTempEval.grid(sticky=stick2,column=1, row=10)
entryTempAngle=tk.Entry(width=labelsize2, textvariable=var12)
entryTempAngle.grid(sticky=stick2,column=1, row=11)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Curr", command=displayURL_curr)
filemenu.add_command(label="Open Temp", command=displayURL_temp)

menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

editmenu.add_command(label="PlotCurr", command=plot_curr)
editmenu.add_command(label="PlotTemp", command=plot_temp)


menubar.add_cascade(label="Plot", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)




root.mainloop()