# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 09:15:20 2018

@author: Rene Planteu
"""

import Tkinter as tk
#from Tkinter import *
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
#from matplotlib.figure import figaspect
#import matplotlib.colors as colors
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class FC_GUI_Fun:
    data={}
    data_str={}
    currfile=""
    tempfile=""
    pathshort=""
    currdone=""
    tempdone=""
    
    def __init__(self):
        """Muss beim Aufrufen des Objects ausgeführt werden"""
        pass
    
    def donothing(self):
        """Tut nichts ;)"""
        filewin = tk.Toplevel(root)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()
    
    
    def importURL_Curr(self):
        """Wählt die Current Rohdatei aus und stellt sie dar"""
        self.currurl = tkFileDialog.askopenfilename(initialdir = "r'C:/Projektlabor_2/FC_Python",title = "Select file",filetypes = (("current files","*.dat"),("all files","*.*")))
        self.currurli_w_ext= os.path.basename(self.currurl)
        self.currfile, self.currext =os.path.splitext(self.currurli_w_ext)
        self.displaycurrent.delete(1.0, tk.END)
        if self.currfile=="":
            self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Currentfile ausgewählt"
            self.displaystate.insert(tk.END, self.nothingcurr+'\n')
        else:    
            self.displaycurrent.insert(tk.END, self.currfile)
            self.currread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current geladen"     
            self.displaystate.insert(tk.END, self.currread+'\n')
        
        
    def importURL_Temp(self):
        """Wählt die Temperatur Rohdatei aus und stellt sie dar"""
        self.tempurl = tkFileDialog.askopenfilename(initialdir = "r'C:/Projektlabor_2/FC_Python",title = "Select file",filetypes = (("current files","*.dat"),("all files","*.*")))
        self.tempurli_w_ext= os.path.basename(self.tempurl)
        self.tempfile, self.tempext =os.path.splitext(self.tempurli_w_ext)
        self.displaytemp.delete(1.0, tk.END)
        if self.tempfile == "":
            self.nothingtemp=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Temperaturfile ausgewählt" 
            self.displaystate.insert(tk.END, self.nothingtemp+'\n')
        else:
            self.displaytemp.insert(tk.END, self.tempfile)        
            self.tempread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperatur geladen"   
            self.displaystate.insert(tk.END, self.tempread+'\n')    
        
            
    def savepath(self):
        """Wählt den Speicherpath aus und stellt ihn dar"""
        self.path= tkFileDialog.askdirectory(title = "Select folder")    
        self.path_w_ext= os.path.basename(self.path)
        self.pathshort, self.pathext =os.path.splitext(self.path_w_ext)
        self.displaypath.delete(1.0, tk.END)
        if self.pathshort=="":
            self.nothingpath= ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Path ausgewaehlt"
            self.displaystate.insert(tk.END, self.nothingpath+'\n') 
        else:
            self.displaypath.insert(tk.END, self.pathshort)
            self.pathread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Path ausgewaehlt"   
            self.displaystate.insert(tk.END, self.pathread+'\n')     
        
        
    def read_Curr(self):
        """Liest die Currentrohdaten ein und speichert sie als Ergebnisfile ab"""
        
        if self.currfile =="":
            self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Currentfile ausgewählt"
            self.displaystate.insert(tk.END, self.nothingcurr+'\n')
        if self.pathshort =="":
            self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Path ausgewählt"
            self.displaystate.insert(tk.END, self.nothingpath+'\n')
            return
        else:
            f = open(self.currurl)
            self.SaveCurr = self.currfile                     
            self.AusCurr = (self.path+'/'+ts.strftime("%Y%m%d_%H%M%S_")+'Ergebnis_'+self.SaveCurr+'.txt')                 # Dateiname curr                               
            volt = []
            #current = []
            lines = []
            rows = 0
            for line in f:
                lines.append(line)
                if 'current' in line:
                    rows += 1
                
            f.close()
        
            timeA = float(lines[1]) 
            skip = int(entryCurrJump.get()) #17
            
            self.data_str = {}
            self.data_str['current'] = []
            self.data_str['voltage'] = []
            self.data_str['time'] = []
            self.data_str['sumcurr']=[]        
            f = open(self.AusCurr,'w')
            #init step
            start = int(entryCurrStart.get())-1    
            end = int(entryCurrEnd.get())
            L = lines[start:end]
            cols = len(L[0].replace('\n','').replace('\t',';').replace(' ','').split(';'))
            cols = cols*len(L)    
            
            currents = np.zeros((rows,cols))
            
            nr = -1
            self.data['current']=[]
            self.data['voltage']=[]
            self.data['time']=[]
            self.data['sumcurr']=[]
            for i in range(0,len(lines),skip):
                nr += 1
                
                #time sec since start
                start = i + 1
                time = lines[start]
                time = float(time)
                time = format((time -timeA),'.1f')          # 1.f = eine Nachkomma
                self.data_str['time'].append(str(time))
                self.data['time'].append(time)            
                
                #voltage
                start = i + int(entryVoltStart.get())-1#4   #1. Zeile mit Spannungswerten
                volt = lines[start]
                volt = float(volt[:8])
                volt = abs(volt)
                volt = format(volt,'.4f')                   # 4.f = 4 Nachkommastellen
                self.data_str['voltage'].append(str(volt)) 
                self.data['voltage'].append(volt)            
                
                #current
                start = i + int(entryCurrStart.get())-1                       # 1. Zeile mit Stromwerten
                end = i + int(entryCurrEnd.get())                            # Letze Zeile mit Sromwerten
                L = lines[start:end]
                rows = len(L)
                curr = []
                self.curr_str = ''
                for row in range(0,rows):
                    dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
                    curr += dummy.split(';')
                    self.curr_str = self.curr_str + dummy + ';'
                
                currents[nr,:] = curr        
                self.data_str['current'].append(self.curr_str[:-1])
                self.data['current'].append(currents[nr,:])
                
                #Sum of Current in line
                self.data_str['sumcurr'].append(str(np.sum(currents[nr,:])))
                self.data['sumcurr'].append( np.sum(currents[nr,:]))
                
                stringline = self.data_str['time'][nr] + ';' + self.data_str['voltage'][nr] +';'+ self.data_str['current'][nr] + self.data_str['sumcurr'][nr]+';' +'\n'
                f.write(stringline)
            self.data['sumcurr'] = np.array(self.data['sumcurr'])
            self.currdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current eingelesen"   
            self.displaystate.insert(tk.END, self.currdone+'\n')       
            
            f.close()
    
    def read_Temp(self):
        """Liest die Temperaturrohdaten ein und speichert sie als Ergebnisfile ab"""
        if self.tempfile =="":
            self.nothingtemp=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Temperaturfile ausgewählt"
            self.displaystate.insert(tk.END, self.nothingtemp+'\n')
        if self.pathshort =="":
            self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Path ausgewählt"
            self.displaystate.insert(tk.END, self.nothingpath+'\n')
            return
        else:
            
            
            g = open(self.tempurl)                      
            self.SaveTemp=self.tempfile    
            self.AusTemp = (self.path+'/'+ts.strftime("%Y%m%d_%H%M%S_")+'Ergebnis_'+self.SaveTemp+'.txt')
            linesB = []
            rows = 0
            for line in g:
                linesB.append(line)
                if 'temperature' in line:
                    rows += 1
            g.close()
           
            timeC = float(linesB[1]) 
            skipB = int(entryTempJump.get()) #10
            
            self.data_str['temp'] = []
            self.data_str['timetemp'] = []
           
            g = open(self.AusTemp,'w')
            
            #init step
            start = int(entryTempStart.get())-1 
            end = int(entryTempEnd.get()) 
            L = linesB[start:end]
            cols = len(L[0].split('\t'))
            cols = cols*len(L) 
            
            temperature=np.zeros((rows,cols))
            
            nr=-1
            self.data['temp']=[]
            self.data['timetemp']=[]
            for i in  range(0,len(linesB),skipB):
                nr += 1
            
                #time in sec since start
                start = i + 1
                timeB = linesB[start]
                timeB = float(timeB)
                timeB = format((timeB -timeC),'.1f') 
                self.data_str['timetemp'].append(str(timeB))
                self.data['timetemp'].append(timeB)
                
                #temperature
                start = i + int(entryTempStart.get())-1                       # 1. Zeile mit Stromwerten
                end = i + int(entryTempEnd.get())                            # Letze Zeile mit Sromwerten
                L = linesB[start:end]
                rows = len(L)
                temp = []
                self.temp_str = ''
                for row in range(0,rows):
                    dummy = L[row].replace('\n','').replace('\t',';').replace(' ','')
                    temp += dummy.split(';')
                    self.temp_str=self.temp_str + dummy +';'
                    
                temperature[nr,:] = temp
                self.data_str['temp'].append(self.temp_str[:-1])
                self.data['temp'].append(temperature[nr,:])
                
                stringline = self.data_str['timetemp'][nr]+';' +self.data_str['temp'][nr]+';'+'\n'
                g.write(stringline)
            
            
            self.tempdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature eingelesen"
            self.displaystate.insert(tk.END, self.tempdone+'\n')    
            
            
            g.close()
    
    
    
    def plot_curr(self):
        """Plotet anhand der eingebenen Zeilennummer"""
        ######## plot a 3D Current ########
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Bitte zuerst Current einlesen"
            self.displaystate.insert(tk.END, self.nothingdone+'\n')
            return
        else:
            fig = plt.figure(figsize=plt.figaspect(0.5))
            canvas = FigureCanvasTkAgg(fig, master=page3)
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page3)
            canvas.get_tk_widget().grid(row=1,column=1)
            toolbar.grid(row=50,column=1) 
              
            
            
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
            current_floats=sp.float64(self.data_str['current'][getrow].split(";")).reshape(10,10)
            maxcurr= np.max(current_floats)
            #print sp.mean(current_floats)
            top=current_floats.ravel()
            top_scaled=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
            mycolors = cm.jet(top_scaled)
            ax.bar3d(X, Y, bottom, width, depth, top,color=mycolors, alpha=float(entryTrans.get()))
            ax.set_title('Partial Currents @ '+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data['voltage'][getrow]+' V')
            
            ax.set_zlim(0,maxcurr)
            ax.set_zlabel('Current in A', linespacing=10.4)
            ax.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))
            
            #plt.show()
            fig = plt.figure()
    
           
            
            #plt.clf()
            #plt.show()
            plt.gcf().canvas.draw()
            
                  
            currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current dargestellt"
            self.displaystate.insert(tk.END, currplot+'\n')  
            
    def plot_curr_sum(self):
            """Gibt Zeilen anhand des eingebenen Stroms an"""
             ######## plot a 3D Current ########
            #for i in self.data['sumcurr']:
            if self.currfile =="":
                self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Currentfile ausgewählt"
                self.displaystate.insert(tk.END, self.nothingcurr+'\n')
            if self.pathshort =="":
                self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"kein Path ausgewählt"
                self.displaystate.insert(tk.END, self.nothingpath+'\n')
            if self.currdone =="":
                self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Bitte zuerst Current einlesen"
                self.displaystate.insert(tk.END, self.nothingdone+'\n')
                return
            else:
                getsum=int(entryCurrsum.get())
                Currenttrue = [np.logical_and((getsum-0.5 <self.data['sumcurr']),(getsum+0.5 >self.data['sumcurr']))]
                #tet=self.data['sumcurr'][Currenttrue]        
                tet2=np.where(Currenttrue)[1]        
                tet3=tet2[20:-10]
                plotsum = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Lines with selected Current:"+str(tet3)
                self.displaystate.insert(tk.END, plotsum+'\n')
                
                pass
        
    def plot_temp(self):
        ######## plot 3D Temperature ########
        
        if self.tempdone =="":
            self.nothingtdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Bitte zuerst Temperatur einlesen"
            self.displaystate.insert(tk.END, self.nothingtdone+'\n')
            return
        else:
            fig2 = plt.figure(figsize=plt.figaspect(0.5))
            canvas = FigureCanvasTkAgg(fig2, master=page3)
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page3)
            canvas.get_tk_widget().grid(row=1,column=2)
            toolbar.grid(row=50,column=2) 
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
            temp_floats=sp.float64(self.data_str['temp'][p].split(";")).reshape(5,5)
            mintemp= np.min(temp_floats)
            mintempplot = mintemp
            mintemptxt = str(round(mintemp,1))
            maxtemp=np.max(temp_floats)
            maxtempplot = maxtemp 
            maxi = maxtempplot-mintempplot+0.1
            top2=temp_floats.ravel()-mintemp
            top_scaled2=(top2-sp.amin(top2))/(sp.amax(top2)-sp.amin(top2))
            mycolors = cm.jet(top_scaled2)
            ax2.bar3d(X2, Y2, bottom, width, depth, top2,color=mycolors, alpha=float(entryTrans.get()))
            ax2.set_title('Temperature'+' @ '+self.data_str['sumcurr'][p]+' A'+'//   @ '+self.data['voltage'][p]+' V')
            
            ax2.set_zlim(0,maxi)
            ax2.set_zlabel('Temperature +'+mintemptxt+'°C')
            ax2.view_init(elev=25., azim=60)
            
            plt.gcf().canvas.draw()
            #plt.show()
            
            tempplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature dargestellt"
            self.displaystate.insert(tk.END, tempplot+'\n')
    
    def clear_msg(self):
        self.displaystate.delete('1.0', tk.END)


""" ------------------------------ GUI start-----------------------------------------------"""

""" Angaben für das Hauptfenster """

root = tk.Tk()
root.title("FC Python")
root.geometry("1000x850")
#root.wm_iconbitmap(r'C:\Software\10_FC_Python\FC_Phyton\03_GUI\FCPy_win7.ico')
labelsize1=40
labelsize2=5
labelsize3=40
labelsize4=80
labelsize6=100
labelsize9=60
textalign = "w"
textalign2="e"
stick=tk.W
stick2=tk.E
FC_GUI_Fun = FC_GUI_Fun()

nb = ttk.Notebook(root)
nb.grid(row=1, column=0, columnspan=300, rowspan=300,sticky=stick2)

#page1 = ttk.Frame(nb)
#nb.add(page1, text='Main')

page2 = ttk.Frame(nb)
nb.add(page2, text='Einstellungen')

page3 = ttk.Frame(nb)
nb.add(page3, text='Plot')

"""####-------Labels------####"""

Curr_sel = tk.Label(page2, text=" Selected Current Data:",width=labelsize1,anchor=textalign)
Curr_sel.grid(column=0, row=0)
Temp_sel = tk.Label(page2, text=" Selected Temp Data:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=1)
Temp_sel = tk.Label(page2, text=" Selected Storage Path:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=3)
labelCurrStart=tk.Label(page2, text=" 1st line of current data in *.dat: (8)", width=labelsize1,anchor=textalign )
labelCurrStart.grid(column=0, row=6)
labelEnd=tk.Label(page2, text=" Last line of current data in *.dat: (17)", width=labelsize1,anchor=textalign)
labelEnd.grid(column=0, row=7)
labelVoltStart=tk.Label(page2, text=" 1st line of voltage data in *.dat: (5)", width=labelsize1,anchor=textalign)
labelVoltStart.grid(column=0, row=8)
labelrowplot=tk.Label(page2, text=" Which line do you want to plot? (0-xxxxxxx)", width=labelsize1,anchor=textalign)
labelrowplot.grid(column=0, row=9)
labelEvalCurr=tk.Label(page2, text="Elevation of plot view: (25)", width=labelsize1,anchor=textalign )
labelEvalCurr.grid(column=0, row=10)
labelAngleCurr=tk.Label(page2, text="Angle of plot view: (60)", width=labelsize1,anchor=textalign )
labelAngleCurr.grid(column=0, row=11)
labelTrans=tk.Label(page2, text="Transparency of Plot 1...0.5...0", width=labelsize1,anchor=textalign )
labelTrans.grid(column=0, row=12)
labelTempStart=tk.Label(page2, text="1st line of temp data in *.dat: (4)", width=labelsize1,anchor=textalign )
labelTempStart.grid(column=2, row=6)
labelTempEnd=tk.Label(page2, text="Last line of temp data in *.dat: (5)", width=labelsize1,anchor=textalign )
labelTempEnd.grid(column=2, row=7)
labelJumpCurr=tk.Label(page2, text="Number of lines between current data: (18)", width=labelsize1,anchor=textalign )
labelJumpCurr.grid(column=2, row=8)
labelJumpTemp=tk.Label(page2, text="Number of lines between temperature data: (10)", width=labelsize1,anchor=textalign )
labelJumpTemp.grid(column=2, row=9)
labelEvalTemp=tk.Label(page2, text="Elevation of plot view(Temp): (25)", width=labelsize1,anchor=textalign )
labelEvalTemp.grid(column=2, row=10)
labelAngleTemp=tk.Label(page2, text="Angle of plot view(Temp): (60)", width=labelsize1,anchor=textalign )
labelAngleTemp.grid(column=2, row=11)
labelCurrSum=tk.Label(page2, text="Measured Current ", width=labelsize1,anchor=textalign )
labelCurrSum.grid(column=2, row=12)
labelMessage=tk.Label(page2, text="Meassage ", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=16)

"""####----- Buttons -----#####"""
bwidth1=10
bwidth2=18
button_currD = tk.Button(page2, text="Load Current", command=FC_GUI_Fun.importURL_Curr)
button_currD.grid(sticky=stick2, column=2, row=0)
button_currD.config(width = bwidth1)
button_tempD = tk.Button(page2, text="Load Temp", command=FC_GUI_Fun.importURL_Temp)
button_tempD.grid(sticky=stick2,column=2, row=1)
button_tempD.config(width = bwidth1)
button_path = tk.Button(page2, text="Storage path", command=FC_GUI_Fun.savepath)
button_path.grid(sticky=stick2,column=2, row=3,)
button_path.config(width = bwidth1)
button_curr = tk.Button(page2, text="Read Current", command=FC_GUI_Fun.read_Curr)
button_curr.grid(sticky=stick, column=0, row=13)
button_curr.config(width = bwidth2)
button_temp = tk.Button(page2, text="Read Temp", command=FC_GUI_Fun.read_Temp)
button_temp.grid(sticky=stick2,column=0, row=13)
button_temp.config(width = bwidth2)
button_plcurr = tk.Button(page2, text="Plot Current", command=FC_GUI_Fun.plot_curr)
button_plcurr.grid(sticky=stick, column=2, row=13)
button_plcurr.config(width = bwidth2)
button_pltemp = tk.Button(page2, text="Plot Temperature", command=FC_GUI_Fun.plot_temp)
button_pltemp.grid(sticky=stick2, column=2, row=13)
button_pltemp.config(width = bwidth2)
button_plcurr = tk.Button(page2, text="Show Current_Lines", command=FC_GUI_Fun.plot_curr_sum)
button_plcurr.grid(sticky=stick, column=1, row=13)
button_plcurr.config(width = bwidth2)
button_plcurr = tk.Button(page2, text="Clear Message", command=FC_GUI_Fun.clear_msg)
button_plcurr.grid(sticky=stick2, column=1, row=13)
button_plcurr.config(width = bwidth2)

"""###-----text------#####"""
FC_GUI_Fun.displaycurrent=tk.Text(master=page2, height = 1, width = labelsize9 )
FC_GUI_Fun.displaycurrent.grid(sticky=stick, column=1, row=0,columnspan=2)
FC_GUI_Fun.displaytemp=tk.Text(master=page2, height = 1, width = labelsize9)
FC_GUI_Fun.displaytemp.grid(sticky=stick, column=1, row=1, columnspan=2)
FC_GUI_Fun.displaypath=tk.Text(master=page2, height = 1, width =labelsize9)
FC_GUI_Fun.displaypath.grid(sticky=stick,column=1, row=3, columnspan=2)
FC_GUI_Fun.displaystate=tk.Text(master=page2, height = 20, width =labelsize6)
FC_GUI_Fun.displaystate.grid(column=0, row=17, columnspan=3)




"""#####------Entrys------#######"""

"""Standardeinträge"""
var1 = tk.StringVar(root, value="8")
var2 = tk.StringVar(root, value="17")
var3 = tk.StringVar(root, value="5")
var4 = tk.StringVar(root, value="5")
var5 = tk.StringVar(root, value="9")
var6 = tk.StringVar(root, value="18")
var7 = tk.StringVar(root, value="10")
var8 = tk.StringVar(root, value="1")
var9 = tk.StringVar(root, value="25")
var10 = tk.StringVar(root, value="60")
var11 = tk.StringVar(root, value="25")
var12 = tk.StringVar(root, value="60")
var13 = tk.StringVar(root, value="1")

"""Position der Entryies"""
entryCurrStart=tk.Entry(page2,width=labelsize2, textvariable=var1)
entryCurrStart.grid(sticky=stick, column=1, row=6)
entryCurrEnd=tk.Entry(page2,width=labelsize2, textvariable=var2)
entryCurrEnd.grid(sticky=stick,column=1, row=7)
entryVoltStart=tk.Entry(page2,width=labelsize2, textvariable=var3)
entryVoltStart.grid(sticky=stick,column=1, row=8)
entryrowplot=tk.Entry(page2,width=labelsize2,textvariable=var8)
entryrowplot.grid(sticky=stick,column=1, row=9)
entryTempStart=tk.Entry(page2,width=labelsize2, textvariable=var4)
entryTempStart.grid(sticky=stick2, column=1, row=6)
entryTempEnd=tk.Entry(page2,width=labelsize2, textvariable=var5)
entryTempEnd.grid(sticky=stick2,column=1, row=7)
entryCurrJump=tk.Entry(page2,width=labelsize2, textvariable=var6)
entryCurrJump.grid(sticky=stick2,column=1, row=8)
entryTempJump=tk.Entry(page2,width=labelsize2, textvariable=var7)
entryTempJump.grid(sticky=stick2,column=1, row=9)
entryCurrEval=tk.Entry(page2,width=labelsize2, textvariable=var9)
entryCurrEval.grid(sticky=stick,column=1, row=10)
entryCurrAngle=tk.Entry(page2,width=labelsize2, textvariable=var10)
entryCurrAngle.grid(sticky=stick,column=1, row=11)
entryTempEval=tk.Entry(page2,width=labelsize2, textvariable=var11)
entryTempEval.grid(sticky=stick2,column=1, row=10)
entryTempAngle=tk.Entry(page2,width=labelsize2, textvariable=var12)
entryTempAngle.grid(sticky=stick2,column=1, row=11)
entryCurrsum=tk.Entry(page2,width=labelsize2,)
entryCurrsum.grid(sticky=stick2,column=1, row=12)
entryTrans=tk.Entry(page2,width=labelsize2,textvariable=var13)
entryTrans.grid(sticky=stick,column=1, row=12)

"""### Menuebar ###"""
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Load Curr", command=FC_GUI_Fun.importURL_Curr)
filemenu.add_command(label="Load Temp", command=FC_GUI_Fun.importURL_Temp)
filemenu.add_command(label="Path", command=FC_GUI_Fun.savepath)
filemenu.add_command(label="Read Curr", command=FC_GUI_Fun.read_Curr)
filemenu.add_command(label="Read Temp", command=FC_GUI_Fun.read_Temp)

menubar.add_cascade(label="File", menu=filemenu)
editmenu = tk.Menu(menubar, tearoff=0)

editmenu.add_command(label="PlotCurr", command=FC_GUI_Fun.plot_curr)
editmenu.add_command(label="PlotTemp", command=FC_GUI_Fun.plot_temp)
editmenu.add_command(label="Plot Line", command=FC_GUI_Fun.plot_curr_sum)


menubar.add_cascade(label="Plot", menu=editmenu)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=FC_GUI_Fun.donothing)
helpmenu.add_command(label="About...", command=FC_GUI_Fun.donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)




root.mainloop()