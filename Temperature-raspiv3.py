
# coding: utf-8

# In[1]:


import os
import glob
import time
import smtplib
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
    from Tkinter import *
else:
    import tkinter as tk
    from tkinter import *
import json
import datetime
window = Tk()
senderemail=[]
senderpassword=[]
recipientemaillist=[]
wifiname=[]
wifipassword=[]
senderemailpassword=[]
segundos=0
temperaturelist=[0]*17280
timelist=['a']*17280 
global setT
setT=IntVar()
window.title("-80 Freezer Raspberry pi Alarm")
 
window.geometry('500x500')
 
lbl = Label(window, text="This GUI will help you to set up your freezer alarm system",font=('Arial Bold',15))
lbl.grid()

lbl = Label(window, text="Enter sender's email address")
lbl.grid()

textBoxSender=Text(window, height=1, highlightbackground="red",  width=50)
textBoxSender.grid()

lbl = Label(window, text="Enter sender's email address password")
lbl.grid()

textBoxSenderpassword=Text(window, height=1, highlightbackground="red",  width=50)
textBoxSenderpassword.grid()

lbl = Label(window, text="Enter the list of recipients' email addresses")
lbl.grid()


textBoxRecipient=Text(window, height=2, highlightbackground="red",  width=50)
textBoxRecipient.grid()

lbl = Label(window, text="Enter freezer name (one word)")
lbl.grid()

textBoxfreezer=Text(window, height=1, highlightbackground="red",  width=50)
textBoxfreezer.grid()

tk.Label(window,text="Set alarm temperature").grid()
lbl=Entry(window,textvariable=setT,width=5)
lbl.grid()
setT.set(-60)

lbl = Label(window, text="Push this button to upload information")
lbl.grid()
buttonupload=Button(window, height=1, width=50,text="Upload information",font=('Arial Bold',12),relief=RAISED,
                    command=lambda: upload_input())
buttonupload.grid()

lbl = Label(window, text="Push this button to start")
lbl.grid()


buttonstart=Button(window, height=1, width=50, text="START", font=('Arial Bold',15),relief=RAISED,
                    command=lambda: start_program())
buttonstart.grid()

lbl = Label(window, text="The current temperature is:")
lbl.grid()

def upload_input():
     global segundos

     senderemail=textBoxSender.get("1.0","end-1c")
     senderemailF=list(senderemail.split (" "))        
     recipientemaillist=textBoxRecipient.get("1.0","end-1c")
     recipientemailF=list(recipientemaillist.split ("\n"))
     senderpassword=textBoxSenderpassword.get("1.0","end-1c")
     senderemailpasswordF=list(senderpassword.split (" ")) 
     freezername=textBoxfreezer.get("1.0","end-1c")
     freezernameF=list(freezername.split (" ")) 
     global setT
     setTT=setT.get()
     try:
         with open('/home/pi/timelist.txt', 'w') as timeL:
             json.dump(timelist,timeL)
         with open('/home/pi/temperaturelist.txt', 'w') as tempL:
             json.dump(temperaturelist,tempL)  
         with open('/home/pi/alarmset.txt', 'w') as Alarmset:
             json.dump(setTT,Alarmset)
         with open('/home/pi/senders.txt', 'w') as sender:
             json.dump(senderemailF,sender)
         with open('/home/pi/recipients.txt', 'w') as recipients:
             json.dump(recipientemailF,recipients)
         with open('/home/pi/senderpassword.txt', 'w') as Spassword:
             json.dump(senderemailpasswordF,Spassword)
         with open('/home/pi/freezername.txt', 'w') as Freezername:
             json.dump(freezernameF,Freezername)  
     except Exception:
         print("oh, no!")
def start_timeout():
    global segundos
    segundos=segundos+1
    window.after(1000,start_timeout)
window.after(1000,start_timeout())

var=DoubleVar()
var.set(22.00)
lbl=Label(window,textvariable=var)
lbl.grid()    


#if segundos>=600 and os.path.exists('/home/pi/recipients.txt') and os.path.exists('/home/pi/senders.txt') and os.path.exists('/home/pi/senderpassword.txt'): #and os.path.exists('/Users/josem.alonso.imacii/Desktop/wifinames.txt') and os.path.exists('/Users/josem.alonso.imacii/Desktop/wifipassword.txt')
#    start_program
def start_program():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir='/sys/bus/w1/devices/'
    device_folder=glob.glob(base_dir + '28*')[0]
    device_file=device_folder + '/w1_slave'
    global setTT
    with open('/home/pi/alarmset.txt','r') as tempset:
        setTT=json.load(tempset)
    def read_temp_raw():
        f=open(device_file, 'r')
        lines=f.readlines()
        f.close()
        return lines
    def read_temp():
        global setT
        lines=read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines=read_temp_raw()
        equals_pos=lines[1].find('t=')
        if equals_pos !=-1:
            temp_string=lines[1][equals_pos+2:]
            temp_c=float(temp_string)/1000.0
            temp_f=temp_c*9.0/5.0+32.0
            if temp_c>=setTT: 
                with open('/home/pi/recipients.txt','r') as recipients:
                    emailR=json.load(recipients)      
                with open('/home/pi/senders.txt','r') as senders:
                    emailS=json.load(senders)     
                with open('/home/pi/senderpassword.txt','r') as senderpassword:
                    emailP=json.load(senderpassword) 
                with open('/home/pi/freezername.txt','r') as Freezername:
                    freezer=json.load(Freezername)
                numberofemails=len(emailR)
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(emailS[0],emailP[0])
                nombre=freezer[0]
                subject = '#freezer alarm' #Line that causes trouble
                msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
                for x in range(numberofemails):
                    server.sendmail(emailS[0],emailR[x],msg)
                time.sleep(600)
                server.quit
            currenttime=datetime.datetime.now()
            tiempoactual=currenttime.isoformat()
            timetosend=tiempoactual.split('T')
            timetosend1=timetosend[1].split('.')
            timetosend2=timetosend1[0].split(':')
            timetosend3=timetosend2[0]+':'+timetosend2[1]
            if timetosend3=='11:45':
                with open('/home/pi/freezername.txt','r') as Freezername:
                    freezer=json.load(Freezername)
                nombre=freezer[0]
                subject = '#freezer alarm' #Line that causes trouble
                msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
                with open('/home/pi/senderpassword.txt','r') as senderpassword:
                    emailP=json.load(senderpassword)
                with open('/home/pi/senders.txt','r') as senders:
                    emailS=json.load(senders)  
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(emailS[0],emailP[0])
                server.sendmail(emailS[0],emailS[0],msg)
                time.sleep(60)
                server.quit
            return temp_c, temp_f
    while True:
        global temperaturelist
        global timelist
        (tempc,tempf)=read_temp()
        var.set(tempc)
        print(tempc)
        window.update_idletasks()
        del temperaturelist[0]
        del timelist[0]
        temperaturelist.append(tempc)
        currenttime=datetime.datetime.now()
        tiempoactual=currenttime.isoformat()
        timelist.append(tiempoactual)
        with open('/home/pi/temperaturelist.txt','w') as templist:
            json.dump(temperaturelist,templist)
        with open('/home/pi/timelist.txt','w') as tiempolist:
            json.dump(timelist,tiempolist)
        time.sleep(5)
window.mainloop()

