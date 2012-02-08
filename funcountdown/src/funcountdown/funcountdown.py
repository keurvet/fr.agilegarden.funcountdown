#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4 févr. 2012

@author: Pierrick Thibault Agile Garden
@license: GPL
'''
import time
import sys
from datetime import timedelta, datetime
import threading
import Tkinter as tk
import tkFont
from Tkinter import PhotoImage
import webbrowser

class CountDown(object):
      
    def __init__(self, startSeconds, notifier):
        self.notifier = notifier
        self.count = startSeconds
        self.digits = []
         
    def update(self):
        if self.count > 0 :
            self.count -= 1
                
    def getCountStr(self):
        hours = self.count  / 3600
        minutes = (self.count - hours * 3600) / 60
        seconds = self.count - hours * 3600 - minutes * 60
        return str(hours) + ":" + ('0' if minutes < 10 else '') + str(minutes)  + ":" + ('0' if seconds < 10 else '') + str(seconds)
  
    def getCountHour(self):
        dt = datetime(2000, 1, 1, 0, 0, 0) + timedelta(seconds=self.count)
        return dt.hour
 
    def getCountMinute(self):
        dt = datetime(2000, 1, 1, 0, 0, 0) + timedelta(seconds=self.count)
        return dt.minute
 
    def getCountSecond(self):
        dt = datetime(2000, 1, 1, 0, 0, 0) + timedelta(seconds=self.count)
        return dt.second
    
    def enter(self, digit):
        self.digits.insert(0,digit)
        self.count = self.calculateFromDigits()
        if len(self.digits) >= 6 :
            self.digits = []
            
    def deleteLastEntered(self):
        if len(self.digits) > 0 : 
            self.digits.remove(self.digits[0])
            self.count = self.calculateFromDigits()
        
    def calculateFromDigits(self):
        result = 0
        multiplicators = [1, 10, 60, 600, 3600, 36000]
        for i in range(0,len(self.digits)):
            result += multiplicators[i] * self.digits[i]
        return result
 
class SecondNotifier(object):
    def __init__(self, stepSeconds):
        self.stepSeconds = stepSeconds 
        self.listObservers = []
        self.lastTime = time.time()
        self.notifying = False
  
    def register(self, observer):
        if observer not in self.listObservers :
            self.listObservers.append(observer)
    
    def unRegister(self, observer):
        self.listObservers.remove(observer)
            
    def start(self):
        if not self.notifying:
            self.thread1 = threading.Thread(target=self.notifyLoop)
            self.thread1.start()
 
    def notifyLoop(self):
        self.notifying = True
        self.notifyAll()
        self.lastTime = time.time()
        while self.notifying :
            time.sleep(self.stepSeconds/3.)
            if time.time() > self.lastTime + self.stepSeconds :
                self.notifyAll()
                self.lastTime = time.time()
                        
    def stop(self):
        self.notifying = False

                        
    def notifyAll(self):
        for obs in self.listObservers:
            obs.update()
            

'''
**************************************
               VIEW
**************************************
'''
class FunView(tk.Frame):
    '''
    classdocs
    '''
    def __init__(self, master):
        '''
        Constructor
        '''     
        self.fontColor = "white"
        self.backgroungColor="#1A171C"
        self.alertColor="#E75294"

        self.master = master
        self.master.title("Fun Count Down - Set with numeric keys, <Return> to start/stop, <Escape> to reinitialize")
        self.master["background"]=self.backgroungColor
        self.master.geometry("800x600")

        
        self.initialTime = 0
        self.notifier = SecondNotifier(1)
        self.countDown = CountDown(0, self.notifier)
        self.notifier.register(self)
        self.notifier.register(self.countDown)
        self.fontPolice="DejaVu Sans"
        self.fontWeight="bold"
            
        tk.Frame.__init__(self, self.master)
        self["background"]=self.backgroungColor
        self.pack(fill="both", expand=1)
               
        self.logo = PhotoImage(file = sys.path[0]+'/agile-garden.gif')
        self.labellogo=tk.Label(self, image=self.logo, background=self.backgroungColor)
        self.labellogo.pack(fill="both", expand=1)

        
        self.time=tk.StringVar()
        self.secondsLabel=tk.Label(self, background=self.backgroungColor, fg=self.fontColor, textvariable=self.time)
        self.secondsLabel.pack(fill="both", expand=1)
        self.sefFontSize(150)
                
        self.time.set(self.countDown.getCountStr())
        
        self.link=tk.Label(self, background=self.backgroungColor, fg="#707172", text="http://www.agilegarden.fr")
        self.link.pack(fill="y", expand=1)
        
        self.link.bind("<Button-1>", self.openAgilGardenSite)
        self.link.bind("<Enter>", self.overAgilGardenSite)
        self.link.bind("<Leave>", self.unoverAgilGardenSite)
        self.master.bind( '<Configure>', self.onWindowEvent )
        self.master.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.master.bind_all('<Key>', self.key)
        self.master.bind_all('<Return>', self.startStop)
        self.master.bind_all('<space>', self.startStop)
        self.master.bind_all('<Escape>', self.clear)
        self.master.bind_all('<BackSpace>', self.backspace)
        
      
    ''' EVENTS '''
    
    '''THIS IS THE METHOD THAT IS CALLED ASYNCHRONOUSLY BY THE NOTIFIER'''
    def update(self):
        self.time.set(self.countDown.getCountStr())  
        self.update_idletasks()
        if self.countDown.count == 0 : 
            self.alert()

    def onWindowEvent(self, event):
        if event.type == '22':
            self.sefFontSize(self.master.winfo_width() / 8)
 
    def onQuit(self):
        self.notifier.stop()
        self.master.destroy()
 
    def key(self, event):
        key = event.char
        if not self.notifier.notifying :
            try:
                digit = int(key)
                self.countDown.enter(digit)
                self.initTime()
            except ValueError:
                pass
                
    def backspace(self, event):
        if not self.notifier.notifying :
            self.countDown.deleteLastEntered()
            self.initTime()
                 
    def startStop(self, event):
        if self.notifier.notifying :
            self.stop()
        else :
            self.start()
    
    def clear(self, event):
        if self.notifier.notifying :
            self.stop()
            
        self.secondsLabel["fg"]= self.fontColor
        self.countDown.count = self.initialTime
        self.initTime()
    
    def openAgilGardenSite(self, event):
        webbrowser.open("http://www.agilegarden.fr")
    
    def overAgilGardenSite(self, event):
        self.link["fg"]="#1BBBEA"
    
    def unoverAgilGardenSite(self, event):
        self.link["fg"]="#707172"
        
    ''' /EVENTS '''

    def start(self):
        self.notifier.start()

    def resume(self):
        self.notifier.start()

 
    def stop(self):
        self.notifier.stop()

    def initTime(self):
        self.initialTime = self.countDown.count
        self.time.set(self.countDown.getCountStr())

    def alert(self):
        self.secondsLabel["fg"]= self.alertColor
        self.time.set("") 
        time.sleep(0.5)
        self.time.set(self.countDown.getCountStr()) 
        
    def sefFontSize(self, size):
        self.secondsLabel["font"]=tkFont.Font(family=self.fontPolice,size=size,weight=self.fontWeight)

        
if __name__ == '__main__':
    root = tk.Tk()
    view = FunView(root)
    view.mainloop()
