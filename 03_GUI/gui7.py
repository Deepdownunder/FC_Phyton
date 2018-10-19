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
from mpl_toolkits.mplot3d.axes3d import Axes3D as dreid
from mpl_toolkits.mplot3d.axes3d import get_test_data as datdreid
import scipy as sp
from matplotlib import cm
#from matplotlib.figure import figaspect
#import matplotlib.colors as colors
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
np.set_printoptions(threshold='nan')
from matplotlib.figure import Figure






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
            self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Currentfile was selected"
            self.displaystate.insert(tk.END, self.nothingcurr+'\n', 'RED')
        else:    
            self.displaycurrent.insert(tk.END, self.currfile)
            self.currread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Currentfile selected"     
            self.displaystate.insert(tk.END, self.currread+'\n')
        
        
    def importURL_Temp(self):
        """Wählt die Temperatur Rohdatei aus und stellt sie dar"""
        self.tempurl = tkFileDialog.askopenfilename(initialdir = "r'C:/Projektlabor_2/FC_Python",title = "Select file",filetypes = (("current files","*.dat"),("all files","*.*")))
        self.tempurli_w_ext= os.path.basename(self.tempurl)
        self.tempfile, self.tempext =os.path.splitext(self.tempurli_w_ext)
        self.displaytemp.delete(1.0, tk.END)
        if self.tempfile == "":
            self.nothingtemp=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Temperaturefile was selected" 
            self.displaystate.insert(tk.END, self.nothingtemp+'\n', 'RED')
        else:
            self.displaytemp.insert(tk.END, self.tempfile)        
            self.tempread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperaturefile selected "   
            self.displaystate.insert(tk.END, self.tempread+'\n')    
        
            
    def savepath(self):
        """Wählt den Speicherpath aus und stellt ihn dar"""
        self.path= tkFileDialog.askdirectory(title = "Select folder")    
        self.path_w_ext= os.path.basename(self.path)
        self.pathshort, self.pathext =os.path.splitext(self.path_w_ext)
        self.displaypath.delete(1.0, tk.END)
        if self.pathshort=="":
            self.nothingpath= ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Path was selected"
            self.displaystate.insert(tk.END, self.nothingpath+'\n', 'RED') 
        else:
            self.displaypath.insert(tk.END, self.pathshort)
            self.pathread = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Path selected"   
            self.displaystate.insert(tk.END, self.pathread+'\n')     
    

    def div0(current,voltage ):
        return 0 if current == 0 else voltage / current

   
        
    def read_Curr(self):
        """Liest die Currentrohdaten ein und speichert sie als Ergebnisfile ab"""
        print "im Auslesen"
        if self.currfile =="":
            self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Currentfile was selected"
            self.displaystate.insert(tk.END, self.nothingcurr+'\n', 'RED')
        if self.pathshort =="":
            self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Path was selected"
            self.displaystate.insert(tk.END, self.nothingpath+'\n', 'RED')
            return
        else:
            self.f = open(self.currurl)
            self.lines4=self.f.readlines()
            if "voltage" in self.lines4[3]:
                self.f.close()
                self.read_Curr_new()
                                
            else:
                self.f.close()
                self.read_Curr_old()
                
                return
    
    def read_Curr_new(self):
        
            self.f = open(self.currurl)
            self.SaveCurr = self.currfile                     
            self.AusCurr = (self.path+'/'+ts.strftime("%Y%m%d_%H%M%S_")+'Ergebnis_'+self.SaveCurr+'.txt')
            
            # Dateiname curr                               
            volt = []
            #current = []
            lines = []
            rows = 0
            for line in self.f:
                lines.append(line)
                if 'current' in line:
                    rows += 1
                
            self.f.close()
        
            timeA = float(lines[1]) 
            skip = int(entryCurrJump.get()) #17
            
            self.data_str = {}
            self.data_str['current'] = []
            self.data_str['voltage'] = []
            self.data_str['time'] = []
            self.data_str['sumcurr']=[]
            self.data_str['power']=[]
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
            self.data['power']=[]
            self.data['ohm']=[]
            for i in range(0,len(lines),skip):
                nr += 1
                
                #time sec since start
                start = i + 1
                time = lines[start]
                time = float(time)
                time = format((time -timeA),'.1f')          # 1.f = eine Nachkomma
                self.data['time'].append(float(time)) 
                self.data_str['time'].append(str(time))
                           
                
                #voltage
                start = i + int(entryVoltStart.get())-1#4   #1. Zeile mit Spannungswerten
                volt = lines[start]
                volt = float(volt[:8])
                volt = abs(volt)
                volt = format(volt,'.4f')
                volt_str=volt                  # 4.f = 4 Nachkommastellen
                self.data['voltage'].append(float(volt))  
                self.data_str['voltage'].append(str(volt_str)) 
                           
                
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
                self.data_str['sumcurr'].append(str(round(np.sum(currents[nr,:]),4)))
                self.data['sumcurr'].append( np.sum(currents[nr,:]))
                
                
                #Calculating Power
                self.data['power'].append(currents[nr,:]*float(volt))
                power_str_raw=np.array2string(currents[nr,:]*float(volt),precision=4, separator=';')
                power_str=power_str_raw.replace('\n','').replace('[','').replace(']','').replace('\t','')
                self.data_str['power'].append(power_str)
                                
                
                #Calculating Restiance
                self.data['ohm'].append(np.divide((currents[nr,:]),(float(volt))))
                                
                
                stringline = self.data_str['time'][nr] + ';' + self.data_str['voltage'][nr] +';'+ self.data_str['current'][nr] +';'+ self.data_str['sumcurr'][nr]+'\n'
                f.write(stringline)
            self.data['sumcurr'] = np.array(self.data['sumcurr'])
            self.currdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current was loaded with: Method 1"   
            self.displaystate.insert(tk.END, self.currdone+'\n')       
            
            f.close()
            
    def read_Curr_old(self):
        
            self.f = open(self.currurl)
            self.SaveCurr = self.currfile                     
            self.AusCurr = (self.path+'/'+ts.strftime("%Y%m%d_%H%M%S_")+'Ergebnis_'+self.SaveCurr+'.txt')
            
            # Dateiname curr                               
            volt = []
            #current = []
            lines = self.f.readlines()
            rows= int(np.shape(lines)[0]/13)
                
                
                
            self.f.close()
        
            timeA = float(lines[1]) 
            skip = int(entryCurrJump2.get()) #17
            
            self.data_str = {}
            self.data_str['current'] = []
            self.data_str['voltage'] = []
            self.data_str['time'] = []
            self.data_str['sumcurr']=[]
            self.data_str['power']=[]
            f = open(self.AusCurr,'w')
            #init step
            start = int(entryCurrStart2.get())-1    
            end = int(entryCurrEnd2.get())
            L = lines[start:end]
            cols = len(L[0].replace('\n','').replace('\t',';').replace(' ','').split(';'))
            cols = cols*len(L)    
            
            currents = np.zeros((rows,cols))
            
            nr = -1
            self.data['current']=[]
            self.data['voltage']=[]
            self.data['time']=[]
            self.data['sumcurr']=[]
            self.data['power']=[]
            self.data['ohm']=[]
            for i in range(0,len(lines),skip):
                nr += 1
                
                #time sec since start
                start = i + 1
                time = lines[start]
                time = float(time)
                time = format((time -timeA),'.1f')          # 1.f = eine Nachkomma
                self.data['time'].append(float(time))            
                self.data_str['time'].append(str(time))
                
                #voltage
                start = i + int(entryVoltStart2.get())-1#4   #1. Zeile mit Spannungswerten
                volt = lines[start].split('\t')
                volt = volt[0]
                volt = float(volt[:8])
                volt = abs(volt)
                volt = format(volt,'.4f')
                volt_str=volt                       # 4.f = 4 Nachkommastellen
                self.data['voltage'].append(float(volt))  
                self.data_str['voltage'].append(str(volt_str)) 
                          
                
                #current
                start = i + int(entryCurrStart2.get())-1                       # 1. Zeile mit Stromwerten
                end = i + int(entryCurrEnd2.get())                            # Letze Zeile mit Sromwerten
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
                self.data_str['sumcurr'].append(str(round(np.sum(currents[nr,:]),4)))
                self.data['sumcurr'].append( np.sum(currents[nr,:]))
                
                #Calculating Power
                self.data['power'].append(currents[nr,:]*float(volt))
                power_str_raw=np.array2string(currents[nr,:]*float(volt),precision=4, separator=';')
                power_str=power_str_raw.replace('\n','').replace('[','').replace(']','').replace('\t','')
                self.data_str['power'].append(power_str)
                
                #Calculating Restiance
                self.data['ohm'].append(np.divide((currents[nr,:]),(float(volt))))
                
                
                stringline = self.data_str['time'][nr] + ';' + self.data_str['voltage'][nr] +';'+ self.data_str['current'][nr] +';'+ self.data_str['sumcurr'][nr]+'\n'
                f.write(stringline)
            self.data['sumcurr'] = np.array(self.data['sumcurr'])
            self.currdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current loaded with: Method 2"   
            self.displaystate.insert(tk.END, self.currdone+'\n')       
            
            f.close()
    
    
    def read_Temp(self):
        """Liest die Temperaturrohdaten ein und speichert sie als Ergebnisfile ab"""
        if self.tempfile =="":
            self.nothingtemp=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Temperaturefile was selected"
            self.displaystate.insert(tk.END, self.nothingtemp+'\n', 'RED')
        if self.pathshort =="":
            self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Path was selected"
            self.displaystate.insert(tk.END, self.nothingpath+'\n', 'RED')
        else:
            self.g = open(self.tempurl) 
            self.lines5=self.g.readlines()
            if "temperature" in self.lines5[3]:
                self.g.close()
                self.read_Temp_new()
                
            else:
                self.g.close()
                self.read_Temp_old()
                
                return
                
    def read_Temp_new(self):
            
            
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
            self.data_str['tempmw']=[]
            
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
            self.data['tempmw']=[]
            for i in  range(0,len(linesB),skipB):
                nr += 1
            
                #time in sec since start
                start = i + 1
                timeB = linesB[start]
                timeB = float(timeB)
                timeB = format((timeB -timeC),'.1f') 
                self.data_str['timetemp'].append(str(timeB))
                self.data['timetemp'].append(float(timeB))
                
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
                
                #Sum of Current in line
                self.data_str['tempmw'].append(str(round(np.sum(temperature[nr,:])/25,4)))
                self.data['tempmw'].append(float(np.sum(temperature[nr,:])/25))
                
                stringline = self.data_str['timetemp'][nr]+';' +self.data_str['temp'][nr]+';'+self.data_str['tempmw'][nr]+'\n'
                g.write(stringline)
            
            #self.data['tempmw'] = np.array(self.data['tempmw'])
            self.tempdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature loaded with: Method 1"
            self.displaystate.insert(tk.END, self.tempdone+'\n')    
            
            
            g.close()
    
    def read_Temp_old(self):
            
            
            self.g = open(self.tempurl)                      
            self.SaveTemp=self.tempfile    
            self.AusTemp = (self.path+'/'+ts.strftime("%Y%m%d_%H%M%S_")+'Ergebnis_'+self.SaveTemp+'.txt')
            
            linesB = self.g.readlines()
            rows= int(np.shape(linesB)[0]/int(entryTempJump2.get()))          
            
            
            self.g.close()
           
            timeC = float(linesB[1]) 
            skipB = int(entryTempJump2.get()) #10
            
            self.data_str['temp'] = []
            self.data_str['timetemp'] = []
            self.data_str['tempmw']=[]
            
            self.g = open(self.AusTemp,'w')
            
            #init step
            start = int(entryTempStart2.get())-1 
            end = int(entryTempEnd2.get()) 
            L = linesB[start:end]
            cols = len(L[0].split('\t'))
            cols = cols*len(L) 
            
            temperature=np.zeros((rows,cols))
            
            nr=-1
            self.data['temp']=[]
            self.data['timetemp']=[]
            self.data['tempmw']=[]
            
            for i in  range(0,len(linesB),skipB):
                nr += 1
            
                #time in sec since start
                start = i + 1
                timeB = linesB[start]
                timeB = float(timeB)
                timeB = format((timeB -timeC),'.1f') 
                self.data_str['timetemp'].append(str(timeB))
                self.data['timetemp'].append(float(timeB))
                
                #temperature
                start = i + int(entryTempStart2.get())-1                       # 1. Zeile mit Stromwerten
                end = i + int(entryTempEnd2.get())                            # Letze Zeile mit Sromwerten
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
                
                #Sum of Current in line
                self.data_str['tempmw'].append(str(round(np.sum(temperature[nr,:])/25,4)))
                self.data['tempmw'].append(float(np.sum(temperature[nr,:])/25))
                
                stringline = self.data_str['timetemp'][nr]+';' +self.data_str['temp'][nr]+';'+self.data_str['tempmw'][nr]+'\n'
                self.g.write(stringline)
            
            #self.data['tempmw'] = np.array(self.data['tempmw'])
            
            self.tempdone = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature loaded with: Method 2"
            self.displaystate.insert(tk.END, self.tempdone+'\n')    
            
            
            self.g.close()      
            
    def plot_curr_sum(self):
            """Gibt Zeilen anhand des eingebenen Stroms an"""
             ######## plot a 3D Current ########
            #for i in self.data['sumcurr']:
            if self.currfile =="":
                self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No currentfile was selected"
                self.displaystate.insert(tk.END, self.nothingcurr+'\n', 'RED')
            if self.pathshort =="":
                self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Path was selected"
                self.displaystate.insert(tk.END, self.nothingpath+'\n', 'RED')
            if self.currdone =="":
                self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
                self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
                return
            else:
                getsum=float(entryCurrsum.get())
                Currenttrue = [np.logical_and((getsum-float(entryCurrsumplus.get()) <self.data['sumcurr']),(getsum+float(entryCurrsumplus.get()) >self.data['sumcurr']))]
                #tet=self.data['sumcurr'][Currenttrue]        
                tet2=np.where(Currenttrue)[1]        
                #tet3=tet2[20:-10]
                plotsum = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Lines with selected Current:"+str(tet2)
                self.displaystate.insert(tk.END, plotsum+'\n')
                
                pass
    
    def plot_temp_sum(self):
            """Gibt Zeilen anhand des eingebenen Stroms an"""
             ######## plot a 3D Current ########
            #for i in self.data['sumcurr']:
            if self.currfile =="":
                self.nothingcurr=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No currentfile was selected"
                self.displaystate.insert(tk.END, self.nothingcurr+'\n', 'RED')
            if self.pathshort =="":
                self.nothingpath=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"No Path was selected"
                self.displaystate.insert(tk.END, self.nothingpath+'\n', 'RED')
            if self.currdone =="":
                self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
                self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
                return
            else:
                gettemp=float(entryTempsum.get())
                Temptrue = [np.logical_and((gettemp-float(entryTempsumplus.get()) <self.data['tempmw']),(gettemp+float(entryTempsumplus.get()) >self.data['tempmw']))]
                #tet=self.data['sumcurr'][Currenttrue]        
                tet4=np.where(Temptrue)[1]        
                #tet3=tet2[20:-10]
                plottemp = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Lines with selected Temperature:"+str(tet4)
                self.displaystate.insert(tk.END, plottemp+'\n')
                
                pass
    
    
    def plot_curr(self):
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        else:
            f = Figure(figsize=(10,2), dpi=100)
            a = f.add_subplot(111)
            a.plot(self.data['time'],self.data['sumcurr'])
            a.set_title('Current vs Time')
            a.set_xlabel('Time in sec')
            a.set_ylabel('Current in A')
            a.set_xlim(np.amin(self.data['time']),np.amax(self.data['time']))
            a.set_ylim(np.amin(self.data['sumcurr']),np.amax(self.data['sumcurr']))
            canvas = FigureCanvasTkAgg(f, master=page1)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page1)
            canvas.get_tk_widget().grid(row=0,column=1)
            toolbar.grid(row=1,column=1) 
            
            
            plt.figure()
    
           
            
            plt.gcf().canvas.draw()
         
            currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current vs time ploted"
            self.displaystate.insert(tk.END, currplot+'\n') 
            
    def plot_volt(self):
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        else:
            f = Figure(figsize=(10,2), dpi=100)
            a = f.add_subplot(111)
            
            a.plot(self.data['time'],self.data['voltage'],'--y')
            a.set_title('Voltage vs Time')
            a.set_xlabel('Time in sec')
            a.set_ylabel('Voltage in V')
            a.set_xlim(np.amin(self.data['time']),np.amax(self.data['time']))
            a.set_ylim(np.amin(self.data['voltage']),np.amax(self.data['voltage']))
            canvas = FigureCanvasTkAgg(f, master=page1)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page1)
            canvas.get_tk_widget().grid(row=2,column=1)
            toolbar.grid(row=3,column=1) 
            
            
            plt.figure()           
            plt.gcf().canvas.draw()
          
            currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Voltage vs time ploted"
            self.displaystate.insert(tk.END, currplot+'\n') 
            
    def plot_temp(self):
        if self.tempdone =="":
            self.nothingtdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read Temperature first"
            self.displaystate.insert(tk.END, self.nothingtdone+'\n', 'RED')
        else:
            f = Figure(figsize=(10,2), dpi=100)
            a = f.add_subplot(111)
            
            a.plot(self.data['timetemp'],self.data['tempmw'],'-r')
            a.set_title('Temperatur vs Time')
            a.set_xlabel('Time in sec')
            a.set_ylabel('Temperature')
            a.set_xlim(np.amin(self.data['time']),np.amax(self.data['time']))
            a.set_ylim(np.amin(self.data['tempmw']),np.amax(self.data['tempmw']))
            canvas = FigureCanvasTkAgg(f, master=page1)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page1)
            canvas.get_tk_widget().grid(row=4,column=1)
            toolbar.grid(row=5,column=1) 
            
            
            plt.figure()           
            plt.gcf().canvas.draw()
          
            currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature vs time ploted"
            self.displaystate.insert(tk.END, currplot+'\n') 
    
    def plot_volt_curr(self):
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        else:
            fig = Figure(figsize=(50.0,50.0), dpi=200, frameon='true')
            fig, ax1, = plt.subplots()
            
            ax1.plot((self.data['time']),(self.data['sumcurr']), 'b-')
            ax1.set_xlabel('Time in sec')
            ax1.set_ylabel('Current in A')
            ax1.set_ylim(np.amin(self.data['sumcurr']),np.amax(self.data['sumcurr']))
            
            
            ax2 = ax1.twinx()
            
            ax2.plot((self.data['time']),(self.data['voltage']), 'y-')
            ax2.set_ylabel('Voltage in U')
            ax2.set_ylim(np.amin(self.data['voltage']),np.amax(self.data['voltage']))
            
            
        
            
            canvas = FigureCanvasTkAgg(fig, master=page5)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand='true')
            toolbar = NavigationToolbar2Tk(canvas, page5)
            canvas.get_tk_widget().grid(row=0,column=1)
            toolbar.grid(row=1,column=1, columnspan=3) 
            
            
            plt.figure()
            plt.gcf().canvas.draw()
    
            currvoltplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current & Voltage vs time ploted"
            self.displaystate.insert(tk.END, currvoltplot+'\n') 

    def plot_curr_temp(self):
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        if self.tempdone =="":
            self.nothingtdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read Temperature first"
            self.displaystate.insert(tk.END, self.nothingtdone+'\n', 'RED')
            return 
        else:
            fig = Figure(figsize=(50.0,50.0), dpi=200, frameon='true')
            fig, ax1, = plt.subplots()
            
            ax1.plot((self.data['time']),(self.data['sumcurr']), 'b-')
            ax1.set_xlabel('Time in sec')
            ax1.set_ylabel('Current in A')
            ax1.set_ylim(np.amin(self.data['sumcurr']),np.amax(self.data['sumcurr']))
            
            
            ax2 = ax1.twinx()
            
            ax2.plot((self.data['time']),(self.data['tempmw']), 'r-')
            ax2.set_ylabel('Temperature')
            ax2.set_ylim(np.amin(self.data['tempmw']),np.amax(self.data['tempmw']))
            
            
        
            
            canvas = FigureCanvasTkAgg(fig, master=page5)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand='true')
            toolbar = NavigationToolbar2Tk(canvas, page5)
            canvas.get_tk_widget().grid(row=2,column=1)
            toolbar.grid(row=3,column=1, columnspan=3) 
            
            
            plt.figure()
            plt.gcf().canvas.draw()
    
            currvoltplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current & Temperatur vs time ploted"
            self.displaystate.insert(tk.END, currvoltplot+'\n') 



    def plot_ui(self):
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        else:
            fromui=int(entryfromui.get())
            toui=int(entrytoui.get())
            
            f = Figure(figsize=(10,2), dpi=100)
            a = f.add_subplot(111)
            
            a.plot(self.data['sumcurr'][fromui:toui],self.data['voltage'][fromui:toui],'-y')
            a.set_title('Current vs Voltage')
            a.set_ylabel('Voltage in V')
            a.set_xlabel('Current in A')
            a.set_ylim(np.amin(self.data['voltage'][fromui:toui]),np.amax(self.data['voltage'][fromui:toui]))
            a.set_xlim(np.amin(self.data['sumcurr'][fromui:toui]),np.amax(self.data['sumcurr'][fromui:toui]))
            canvas = FigureCanvasTkAgg(f, master=page4)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page4)
            canvas.get_tk_widget().grid(row=0,column=1)
            toolbar.grid(row=1,column=1) 
            
            
            
            plt.figure()           
            plt.gcf().canvas.draw()
          
            currplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Voltage vs Current ploted"
            self.displaystate.insert(tk.END, currplot+'\n') 
            

            
    def plot_curr_3D(self):
        """Plotet anhand der eingebenen Zeilennummer"""
        ######## plot a 3D Current ########
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
        if self.tempdone =="":
            self.nothingtdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read Temperature first"
            self.displaystate.insert(tk.END, self.nothingtdone+'\n', 'RED')
            return   
        else:
            fig = plt.figure(figsize=plt.figaspect(0.5))
            canvas = FigureCanvasTkAgg(fig, master=page3)
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page3)
            canvas.get_tk_widget().grid(row=0,column=1)
            toolbar.grid(row=1,column=1) 
              
            
            
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
            ax.set_title('Partial Currents @ '+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data_str['voltage'][getrow]+' V')
            
            ax.set_zlim(0,maxcurr)
            ax.set_zlabel('Current in A',labelpad=15)
            ax.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))
            
            #plt.show()
            fig = plt.figure()
    
           
            
            #plt.clf()
            #plt.show()
            plt.gcf().canvas.draw()
            
                  
            currplot3D = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Current 3D ploted"
            self.displaystate.insert(tk.END, currplot3D+'\n')  
            
   
        
    def plot_temp_3D(self):
        ######## plot 3D Temperature ########
        
        if self.tempdone =="":
            self.nothingtdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read Temperature first"
            self.displaystate.insert(tk.END, self.nothingtdone+'\n', 'RED')
            return
        else:
            fig2 = plt.figure(figsize=plt.figaspect(0.5))
            canvas = FigureCanvasTkAgg(fig2, master=page3)
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page3)
            canvas.get_tk_widget().grid(row=0,column=2)
            toolbar.grid(row=1,column=2) 
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
            ax2.set_title('Temperatures'+' @ '+self.data_str['sumcurr'][p]+' A'+' //   @ '+self.data_str['voltage'][p]+' V\n'+'Mean temp:'+self.data_str['tempmw'][p]+'$^\circ$'+'C')
            
            
            ax2.set_zlim(0,maxi)
            ax2.set_zlabel(u'Temperature +'+mintemptxt+'$^\circ$'+'C',labelpad=15)
            
            ax2.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))               
            
            
            plt.gcf().canvas.draw()
            #plt.show()
            
            tempplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Temperature ploted"
            self.displaystate.insert(tk.END, tempplot+'\n')
            
    def plot_power_3D(self):
        """Plotet anhand der eingebenen Zeilennummer"""
        ######## plot a 3D Current ########
        if self.currdone =="":
            self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first!"
            self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
            return
        else:
            fig = plt.figure(figsize=plt.figaspect(0.5))
            canvas = FigureCanvasTkAgg(fig, master=page3)
            canvas.get_tk_widget().pack(side='top', fill='both')
            canvas._tkcanvas.pack(side='top', fill='both', expand=2)
            toolbar = NavigationToolbar2Tk(canvas, page3)
            canvas.get_tk_widget().grid(row=2,column=1)
            toolbar.grid(row=3,column=1) 
              
            
            
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
            power_floats=self.data['power'][getrow].reshape(10,10)
            maxpower= np.max(power_floats)
            #print sp.mean(current_floats)
            top=power_floats.ravel()
            top_scaled=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
            mycolors = cm.jet(top_scaled)
            ax.bar3d(X, Y, bottom, width, depth, top,color=mycolors, alpha=float(entryTrans.get()))
            ax.set_title('Partial Power @'+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data_str['voltage'][getrow]+' V' )
            #'+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data['voltage'][getrow]+' V')
            
            ax.set_zlim(0,maxpower)
            ax.set_zlabel('Power in W',labelpad=15)
            ax.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))
            
            #plt.show()
            fig = plt.figure()
    
           
            
            #plt.clf()
            #plt.show()
            plt.gcf().canvas.draw()
            
                  
            powerplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Power plotted"
            self.displaystate.insert(tk.END, powerplot+'\n')
            
            return
        
            
    def plot_ohm_3D(self):
        
        """Plotet anhand der eingebenen Zeilennummer"""
            ######## plot a 3D Resistance ########
        if self.currdone =="":
                self.nothingdone=ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Please read current first!"
                self.displaystate.insert(tk.END, self.nothingdone+'\n', 'RED')
                return
        else:
                fig = plt.figure(figsize=plt.figaspect(0.5))
                canvas = FigureCanvasTkAgg(fig, master=page3)
                canvas.get_tk_widget().pack(side='top', fill='both')
                canvas._tkcanvas.pack(side='top', fill='both', expand=2)
                toolbar = NavigationToolbar2Tk(canvas, page3)
                canvas.get_tk_widget().grid(row=2,column=2)
                toolbar.grid(row=3,column=2) 
                  
                
                
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
                ohm_floats=self.data['ohm'][getrow].reshape(10,10)
                maxohm= np.max(ohm_floats)
                #print sp.mean(current_floats)
                top=ohm_floats.ravel()
                top_scaled=(top-sp.amin(top))/(sp.amax(top)-sp.amin(top))
                mycolors = cm.jet(top_scaled)
                ax.bar3d(X, Y, bottom, width, depth, top,color=mycolors, alpha=float(entryTrans.get()))
                ax.set_title('Partial Resistance @'+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data_str['voltage'][getrow]+' V' )
                #'+self.data_str['sumcurr'][getrow]+' A'+'//   @ '+self.data['voltage'][getrow]+' V')
                
                ax.set_zlim(0,maxohm)
                ax.set_zlabel('Resitance in Ohm',labelpad=15)
                ax.view_init(elev=int(entryCurrEval.get()), azim=int(entryCurrAngle.get()))
                
                #plt.show()
                fig = plt.figure()
        
               
                
                #plt.clf()
                #plt.show()
                plt.gcf().canvas.draw()
                
                      
                resistanceplot = ts.strftime("%Y.%m.%d. %H:%M:%S :")+"Resistance plotted"
                self.displaystate.insert(tk.END, resistanceplot+'\n')    
     
    def onExit(self):
        
        root.destroy()    

        return   
        
    def clear_msg(self):
        self.displaystate.delete('1.0', tk.END)


""" ------------------------------ GUI start-----------------------------------------------"""

""" Angaben für das Hauptfenster """

root = tk.Tk()
root.title("FC Python")
root.geometry("1000x900")
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

page2 = ttk.Frame(nb)
nb.add(page2, text='Settings')

page1 = ttk.Frame(nb)
nb.add(page1, text='Plot 2D')

page3 = ttk.Frame(nb)
nb.add(page3, text='Plot 3D')

page5 = ttk.Frame(nb)
nb.add(page5, text='Plot U&I')

page4 = ttk.Frame(nb)
nb.add(page4, text='Plot UI')

"""####-------Labels------####"""

Curr_sel = tk.Label(page2, text=" Selected Current Data:",width=labelsize1,anchor=textalign)
Curr_sel.grid(column=0, row=0)
Temp_sel = tk.Label(page2, text=" Selected Temp Data:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=1)
Temp_sel = tk.Label(page2, text=" Selected Storage Path:",width=labelsize1,anchor=textalign)
Temp_sel.grid(column=0, row=3)
labelMessage=tk.Label(page2, text="------Raw data settings (Method 1)/(Methode2)--------", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=13)
labelCurrStart=tk.Label(page2, text=" 1st line of current data in *.dat: (8)/(4)", width=labelsize1,anchor=textalign )
labelCurrStart.grid(column=0, row=15)
labelEnd=tk.Label(page2, text=" Last line of current data in *.dat: (17)/(13)", width=labelsize1,anchor=textalign)
labelEnd.grid(column=0, row=16)
labelVoltStart=tk.Label(page2, text=" 1st line of voltage data in *.dat: (5)/(3)", width=labelsize1,anchor=textalign)
labelVoltStart.grid(column=0, row=17)
labelTempStart=tk.Label(page2, text="1st line of temp data in *.dat: (5)/(4)", width=labelsize1,anchor=textalign )
labelTempStart.grid(column=2, row=15)
labelTempEnd=tk.Label(page2, text="Last line of temp data in *.dat: (9)/(8)", width=labelsize1,anchor=textalign )
labelTempEnd.grid(column=2, row=16)
labelJumpCurr=tk.Label(page2, text="Num of lines between curr data: (18)/(13)", width=labelsize1,anchor=textalign )
labelJumpCurr.grid(column=2, row=17)
labelJumpTemp=tk.Label(page2, text="Num of lines between temp data: (10)/(8)", width=labelsize1,anchor=textalign )
labelJumpTemp.grid(column=2, row=18)
labelMessage=tk.Label(page2, text="---------------Read Load & Write:---------------", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=19)
labelMessage=tk.Label(page2, text="---------------Plotting:---------------", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=21)
labelEvalCurr=tk.Label(page2, text="Elevation of 3D plot view: (25)", width=labelsize1,anchor=textalign )
labelEvalCurr.grid(column=2, row=22)
labelAngleCurr=tk.Label(page2, text="Angle of 3D plot view : (60)", width=labelsize1,anchor=textalign )
labelAngleCurr.grid(column=2, row=23)
labelTrans=tk.Label(page2, text="Transparency of Plot 1...0.5...0", width=labelsize1,anchor=textalign )
labelTrans.grid(column=0, row=22)
labelMessage=tk.Label(page2, text="---------------Options for Lineplot:---------------", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=26)
labelrowplot=tk.Label(page2, text=" Which line do you want to plot? (0-xxxxxxx)", width=labelsize1,anchor=textalign)
labelrowplot.grid(column=0, row=27)
labelfromui=tk.Label(page2, text=" UI: From which line (0-xxxxxxx)", width=labelsize1,anchor=textalign)
labelfromui.grid(column=0, row=28)
labeltoui=tk.Label(page2, text=" UI: To which line (0-xxxxxxx)", width=labelsize1,anchor=textalign)
labeltoui.grid(column=0, row=29)
labelCurrSum=tk.Label(page2, text="Measured Current                                            +/- ", width=labelsize1,anchor=textalign )
labelCurrSum.grid(column=2, row=27)
labelTempSum=tk.Label(page2, text="Measured Temp                                            +/- ", width=labelsize1,anchor=textalign )
labelTempSum.grid(column=2, row=28)
labelMessage=tk.Label(page2, text="---------------Status:---------------", width=labelsize1,anchor=textalign )
labelMessage.grid(column=1, row=29)




"""####----- Buttons -----#####"""
bwidth1=10
bwidth2=18
bwidth3=24
bheight1=3
button_currD = tk.Button(page2, text="Select Current", command=FC_GUI_Fun.importURL_Curr)
button_currD.grid(sticky=stick2, column=2, row=0)
button_currD.config(width = bwidth1)
button_tempD = tk.Button(page2, text="Select Temp", command=FC_GUI_Fun.importURL_Temp)
button_tempD.grid(sticky=stick2,column=2, row=1)
button_tempD.config(width = bwidth1)
button_path = tk.Button(page2, text="Storage path", command=FC_GUI_Fun.savepath)
button_path.grid(sticky=stick2,column=2, row=3,)
button_path.config(width = bwidth1)
"""---Load and Read---"""
button_curr = tk.Button(page2, text="Read Current", command=FC_GUI_Fun.read_Curr)
button_curr.grid(sticky=stick2, column=0, row=20)
button_curr.config(width = bwidth3, height=bheight1, bg='#b5d12b', font='helv20')
button_temp = tk.Button(page2, text="Read Temp", command=FC_GUI_Fun.read_Temp)
button_temp.grid(sticky=stick,column=2, row=20)
button_temp.config(width = bwidth3, height=bheight1, bg='#1cb8db', font='helv20')
"""---Plots---"""

button_plcurr = tk.Button(page2, text="Plot Current ", command=FC_GUI_Fun.plot_curr)
button_plcurr.grid(sticky=stick, column=0, row=24)
button_plcurr.config(width = bwidth2)


button_pltemp = tk.Button(page2, text="Plot Voltage ", command=FC_GUI_Fun.plot_volt)
button_pltemp.grid(sticky=stick2, column=0, row=25)
button_pltemp.config(width = bwidth2)

button_pltpwr = tk.Button(page2, text="Plot Temp ", command=FC_GUI_Fun.plot_temp)
button_pltpwr.grid(sticky=stick2, column=0, row=24)
button_pltpwr.config(width = bwidth2)

"""
button_pltohm = tk.Button(page2, text="Plot Ohm ", command=FC_GUI_Fun.plot_ohm)
button_pltohm.grid(sticky=stick2, column=0, row=25)
button_pltohm.config(width = bwidth2)

button_pltohm = tk.Button(page2, text="Plot Power ", command=FC_GUI_Fun.plot_power)
button_pltohm.grid(sticky=stick2, column=0, row=25)
button_pltohm.config(width = bwidth2)

"""
button_plcurr = tk.Button(page2, text="Plot U&I", command=FC_GUI_Fun.plot_volt_curr)
button_plcurr.grid(sticky=stick, column=1, row=24)
button_plcurr.config(width = bwidth2)

button_plcurr = tk.Button(page2, text="Plot U vs I ", command=FC_GUI_Fun.plot_ui)
button_plcurr.grid(sticky=stick2, column=1, row=24)
button_plcurr.config(width = bwidth2)

button_plcurr = tk.Button(page2, text="Plot I vs T", command=FC_GUI_Fun.plot_curr_temp)
button_plcurr.grid(sticky=stick, column=1, row=25)
button_plcurr.config(width = bwidth2)

"""----3D Plots----"""
button_plcurr = tk.Button(page2, text="Plot Current 3D", command=FC_GUI_Fun.plot_curr_3D)
button_plcurr.grid(sticky=stick, column=2, row=24)
button_plcurr.config(width = bwidth2)
button_pltemp = tk.Button(page2, text="Plot Temperature 3D", command=FC_GUI_Fun.plot_temp_3D)
button_pltemp.grid(sticky=stick2, column=2, row=24)
button_pltemp.config(width = bwidth2)
button_pltpwr = tk.Button(page2, text="Plot Power 3D", command=FC_GUI_Fun.plot_power_3D)
button_pltpwr.grid(sticky=stick, column=2, row=25)
button_pltpwr.config(width = bwidth2)
button_pltohm = tk.Button(page2, text="Plot Ohm 3D", command=FC_GUI_Fun.plot_ohm_3D)
button_pltohm.grid(sticky=stick2, column=2, row=25)
button_pltohm.config(width = bwidth2)

button_plcurr = tk.Button(page2, text="Show Lines for Ampere", command=FC_GUI_Fun.plot_curr_sum)
button_plcurr.grid(sticky=stick, column=1, row=27)
button_plcurr.config(width = bwidth3)
button_pltemp = tk.Button(page2, text="Show Lines for Temp", command=FC_GUI_Fun.plot_temp_sum)
button_pltemp.grid(sticky=stick, column=1, row=28)
button_pltemp.config(width = bwidth3)

button_plcurr = tk.Button(page2, text="Clear Status Message", command=FC_GUI_Fun.clear_msg)
button_plcurr.grid(sticky=stick2, column=1, row=40)
button_plcurr.config(width = bwidth2)
button_pltemp = tk.Button(page2, text="Exit",fg="#ba160c", command=FC_GUI_Fun.onExit)
button_pltemp.grid(sticky=stick2, column=2, row=40)
button_pltemp.config(width = bwidth3, height=bheight1, bg='#7c7474', font='helv20')

"""###-----text------#####"""
FC_GUI_Fun.displaycurrent=tk.Text(master=page2, height = 1, width = labelsize9 )
FC_GUI_Fun.displaycurrent.grid(sticky=stick, column=1, row=0,columnspan=2)
FC_GUI_Fun.displaytemp=tk.Text(master=page2, height = 1, width = labelsize9)
FC_GUI_Fun.displaytemp.grid(sticky=stick, column=1, row=1, columnspan=2)
FC_GUI_Fun.displaypath=tk.Text(master=page2, height = 1, width =labelsize9)
FC_GUI_Fun.displaypath.grid(sticky=stick,column=1, row=3, columnspan=2)
FC_GUI_Fun.displaystate=tk.Text(master=page2, height = 20, width =labelsize6)
FC_GUI_Fun.displaystate.grid(column=0, row=30, columnspan=3)
FC_GUI_Fun.displaystate.tag_config('RED', foreground='red')




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
var14 = tk.StringVar(root, value="4")
var15 = tk.StringVar(root, value="13")
var16 = tk.StringVar(root, value="3")
var17 = tk.StringVar(root, value="4")
var18 = tk.StringVar(root, value="8")
var19 = tk.StringVar(root, value="13")
var20 = tk.StringVar(root, value="8")
var21 = tk.StringVar(root, value="0.2")
var22 = tk.StringVar(root, value="0.2")
var23 = tk.StringVar(root, value="0")
var24 = tk.StringVar(root, value="1000")


"""Position der Entryies"""
entryCurrStart=tk.Entry(page2,width=labelsize2, textvariable=var1)
entryCurrStart.grid(sticky=stick2, column=0, row=15)
entryCurrStart2=tk.Entry(page2,width=labelsize2, textvariable=var14)
entryCurrStart2.grid(sticky=stick, column=1, row=15)
entryCurrEnd=tk.Entry(page2,width=labelsize2, textvariable=var2)
entryCurrEnd.grid(sticky=stick2,column=0, row=16)
entryCurrEnd2=tk.Entry(page2,width=labelsize2, textvariable=var15)
entryCurrEnd2.grid(sticky=stick,column=1, row=16)
entryVoltStart=tk.Entry(page2,width=labelsize2, textvariable=var3)
entryVoltStart.grid(sticky=stick2,column=0, row=17)
entryVoltStart2=tk.Entry(page2,width=labelsize2, textvariable=var16)
entryVoltStart2.grid(sticky=stick,column=1, row=17)

entryTempStart=tk.Entry(page2,width=labelsize2, textvariable=var4)
entryTempStart.grid(sticky=stick2, column=1, row=15)
entryTempStart2=tk.Entry(page2,width=labelsize2, textvariable=var17)
entryTempStart2.grid(sticky=stick2, column=2, row=15)
entryTempEnd=tk.Entry(page2,width=labelsize2, textvariable=var5)
entryTempEnd.grid(sticky=stick2,column=1, row=16)
entryTempEnd2=tk.Entry(page2,width=labelsize2, textvariable=var18)
entryTempEnd2.grid(sticky=stick2,column=2, row=16)
entryCurrJump=tk.Entry(page2,width=labelsize2, textvariable=var6)
entryCurrJump.grid(sticky=stick2,column=1, row=17)
entryCurrJump2=tk.Entry(page2,width=labelsize2, textvariable=var19)
entryCurrJump2.grid(sticky=stick2,column=2, row=17)
entryTempJump=tk.Entry(page2,width=labelsize2, textvariable=var7)
entryTempJump.grid(sticky=stick2,column=1, row=18)
entryTempJump2=tk.Entry(page2,width=labelsize2, textvariable=var20)
entryTempJump2.grid(sticky=stick2,column=2, row=18)
entryCurrEval=tk.Entry(page2,width=labelsize2, textvariable=var9)
entryCurrEval.grid(sticky=stick2,column=1, row=22)
entryCurrAngle=tk.Entry(page2,width=labelsize2, textvariable=var10)
entryCurrAngle.grid(sticky=stick2,column=1, row=23)
entryTrans=tk.Entry(page2,width=labelsize2,textvariable=var13)
entryTrans.grid(sticky=stick2,column=0, row=22)
"""----Linepolot---_"""
entryrowplot=tk.Entry(page2,width=labelsize2,textvariable=var8)
entryrowplot.grid(sticky=stick2,column=0, row=27)
entryfromui=tk.Entry(page2,width=labelsize2,textvariable=var23)
entryfromui.grid(sticky=stick2,column=0, row=28)
entrytoui=tk.Entry(page2,width=labelsize2,textvariable=var24)
entrytoui.grid(sticky=stick2,column=0, row=29)


entryCurrsum=tk.Entry(page2,width=labelsize2,)
entryCurrsum.grid(sticky=stick2,column=1, row=27)
entryCurrsumplus=tk.Entry(page2,width=labelsize2,textvariable=var21)
entryCurrsumplus.grid(sticky=stick2,column=2, row=27)
entryTempsum=tk.Entry(page2,width=labelsize2,)
entryTempsum.grid(sticky=stick2,column=1, row=28)
entryTempsumplus=tk.Entry(page2,width=labelsize2,textvariable=var22)
entryTempsumplus.grid(sticky=stick2,column=2, row=28)

"""### Menuebar ###"""
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Select Curr", command=FC_GUI_Fun.importURL_Curr)
filemenu.add_command(label="Select Temp", command=FC_GUI_Fun.importURL_Temp)
filemenu.add_command(label="Select Path", command=FC_GUI_Fun.savepath)
filemenu.add_separator()
filemenu.add_command(label="Read Curr", command=FC_GUI_Fun.read_Curr)
filemenu.add_command(label="Read Temp", command=FC_GUI_Fun.read_Temp)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Plot Curr 3D", command=FC_GUI_Fun.plot_curr_3D)
editmenu.add_command(label="Plot Temp 3D", command=FC_GUI_Fun.plot_temp_3D)
editmenu.add_command(label="Plot Power 3D", command=FC_GUI_Fun.plot_power_3D)
editmenu.add_command(label="Plot Resistance 3D", command=FC_GUI_Fun.plot_ohm_3D)
editmenu.add_separator()
editmenu.add_command(label="Show Line with A", command=FC_GUI_Fun.plot_curr_sum)
editmenu.add_command(label="Show Line with Temp", command=FC_GUI_Fun.plot_temp_sum)
menubar.add_cascade(label="Plot", menu=editmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=FC_GUI_Fun.donothing)
helpmenu.add_command(label="About...", command=FC_GUI_Fun.donothing)
helpmenu.add_separator()
helpmenu.add_command(label="Exit", command=FC_GUI_Fun.onExit)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)




root.mainloop()