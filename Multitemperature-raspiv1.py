
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
global setTL
setT=IntVar()
setTL=IntVar()
window.title("-80 Freezer Raspberry pi Alarm")
 
window.geometry('500x500')
 
#lbl = Label(window, text="This GUI will help you to set up your freezer alarm system",font=('Arial Bold',15))
#lbl.grid()

lbl = Label(window, text="Enter sender's email address")
lbl.grid(row=0,column=0)

textBoxSender=Text(window, height=1, highlightbackground="red",  width=35)
textBoxSender.grid(row=1,column=0)

lbl = Label(window, text="Enter sender's email address password")
lbl.grid(row=0,column=1)

textBoxSenderpassword=Text(window, height=1, highlightbackground="red",  width=35)
textBoxSenderpassword.grid(row=1,column=1)

lbl = Label(window, text="Enter the list of recipients' email addresses")
lbl.grid(row=2,column=0)


textBoxRecipient=Text(window, height=2, highlightbackground="red",  width=35)
textBoxRecipient.grid(row=3,column=0)

lbl = Label(window, text="Enter freezer names (one word)")
lbl.grid(row=2,column=1)

textBoxfreezer=Text(window, height=2, highlightbackground="red",  width=35)
textBoxfreezer.grid(row=3,column=1)

lbl = Label(window, text="Enter probe ID: 35-.....")
lbl.grid(row=5)

textBoxprobe=Text(window, height=2, highlightbackground="red",  width=35)
textBoxprobe.grid(row=6)


tk.Label(window,text="Set alarm temperature (HIGHEST)").grid(row=8,column=0)
# lbl=Entry(window,textvariable=setT,width=5)
# lbl.grid()
setT.set(-60)
textBoxsetT=Text(window, height=2, highlightbackground="red",  width=5)
textBoxsetT.grid(row=9,column=0)

tk.Label(window,text="Set alarm temperature (LOWEST)").grid(row=8,column=1)
# lbl=Entry(window,textvariable=setTL,width=5)
# lbl.grid()
setTL.set(-85)
textBoxsetTL=Text(window, height=2, highlightbackground="red",  width=5)
textBoxsetTL.grid(row=9,column=1)

#lbl = Label(window, text="Push this button to upload information")
#lbl.grid()
buttonupload=Button(window, height=1, width=35,text="Upload information",font=('Arial Bold',12),relief=RAISED,
                    command=lambda: upload_input())
buttonupload.grid(row=11,column=0)

#lbl = Label(window, text="Push this button to start")
#lbl.grid()


buttonstart=Button(window, height=1, width=35, text="START", font=('Arial Bold',12),relief=RAISED,
                    command=lambda: start_program())
buttonstart.grid(row=11,column=1)

#lbl = Label(window, text="The current temperature is:")
#lbl.grid()

def upload_input():
     global segundos
#      global setTF
#      global setTLF

     senderemail=textBoxSender.get("1.0","end-1c")
     senderemailF=list(senderemail.split (" "))        
     recipientemaillist=textBoxRecipient.get("1.0","end-1c")
     recipientemailF=list(recipientemaillist.split ("\n"))
     senderpassword=textBoxSenderpassword.get("1.0","end-1c")
     senderemailpasswordF=list(senderpassword.split (" ")) 
     freezername=textBoxfreezer.get("1.0","end-1c")
     freezernameF=list(freezername.split ("\n"))
     setT=textBoxsetT.get("1.0","end-1c")
     setTF=list(setT.split ("\n"))
     setTL=textBoxsetTL.get("1.0","end-1c")
     setTFL=list(setTL.split ("\n"))
     setTL=textBoxsetTL.get("1.0","end-1c")
     setTFL=list(setTL.split ("\n"))
     probes=textBoxprobe.get("1.0","end-1c")
     probesF=list(probes.split ("\n"))

#      setTT=setT.get()
     
#      setTTL=setTL.get()
     try:
         with open('/home/pi/timelist.txt', 'w') as timeL:
             json.dump(timelist,timeL)
         with open('/home/pi/temperaturelist.txt', 'w') as tempL:
             json.dump(temperaturelist,tempL)  
         with open('/home/pi/alarmset.txt', 'w') as Alarmset:
             json.dump(setTF,Alarmset)
         with open('/home/pi/alarmsetL.txt', 'w') as AlarmsetL:
             json.dump(setTFL,AlarmsetL)                
         with open('/home/pi/senders.txt', 'w') as sender:
             json.dump(senderemailF,sender)
         with open('/home/pi/recipients.txt', 'w') as recipients:
             json.dump(recipientemailF,recipients)
         with open('/home/pi/senderpassword.txt', 'w') as Spassword:
             json.dump(senderemailpasswordF,Spassword)
         with open('/home/pi/freezername.txt', 'w') as Freezername:
             json.dump(freezernameF,Freezername) 
         with open('/home/pi/probenames.txt', 'w') as Probenames:
             json.dump(probesF,Probenames)

                
     except Exception:
         print("oh, no!")
#def start_timeout():
#    global segundos
#    segundos=segundos+1
#    window.after(1000,start_timeout)
#window.after(1000,start_timeout())

#var=DoubleVar()
#var.set(22.00)
#lbl=Label(window,textvariable=var)
#lbl.grid()    


#if segundos>=600 and os.path.exists('/home/pi/recipients.txt') and os.path.exists('/home/pi/senders.txt') and os.path.exists('/home/pi/senderpassword.txt'): #and os.path.exists('/Users/josem.alonso.imacii/Desktop/wifinames.txt') and os.path.exists('/Users/josem.alonso.imacii/Desktop/wifipassword.txt')
#    start_program
def start_program():
    global setTTL
    global setTT
    global device_folder
    global device_file




    time.sleep(1)
    #global setT
    #global setTL
    #global counter
    counter=0
    # temperaturelist=[0]*10000
    # timelist=['a']*10000
    device_folder=[]
    device_file=[]
    temp_cL=[]
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir='/sys/bus/w1/devices/'
    with open('/home/pi/alarmset.txt','r') as alarmset:
        setT=json.load(alarmset) 
    with open('/home/pi/alarmsetL.txt','r') as alarmsetL:
        setTL=json.load(alarmsetL)
    with open('/home/pi/temperaturelist.txt','r') as tempL:
        temperaturelist=json.load(tempL)
    with open('/home/pi/timelist.txt','r') as timeL:
        timelist=json.load(timeL)
    with open ('/home/pi/probenames.txt','r') as probesList:
        probesL=json.load(probesList)
    for x1 in range(len(probesL)):
        device_folderT=glob.glob(base_dir + probesL[x1])[0]
        device_folder.append(device_folderT)
        device_fileT=device_folder[x1] + '/w1_slave'
        device_file.append(device_fileT)

    def read_temp_raw():
        lines=[]
        global device_folder
        global device_file
        for x2 in range(len(probesL)):
            f=open(device_file[x2], 'r')
            lin=f.readlines()
            f.close()
            lines.append(lin)
        return lines
    def read_temp():
        nombre=''
        temperatura=''
        alarma=0
        counter=0
        temp_cL=[]
        lines=read_temp_raw()
        for x3 in range(len(probesL)):
            linesY=lines[x3]
            while linesY[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines=read_temp_raw()
                linesY=lines[x3]

            equals_pos=linesY[1].find('t=')
            if equals_pos !=-1:
                temp_string=linesY[1][equals_pos+2:]
                temp_c=float(temp_string)/1000.0
            temp_cL.append(temp_c)
            if temp_c>=float(setT[x3])+10 or temp_c<=float(setTL[x3])-5:
                alarma=2
            if  temp_c>=float(setT[x3]) or temp_c<=float(setTL[x3]):
                alarma=1

        if alarma==1:
            try:
                with open('/home/pi/freezername.txt','r') as Freezername:
                    freezer=json.load(Freezername)            
                with open('/home/pi/recipients.txt','r') as recipients:
                    emailR=json.load(recipients)      
                with open('/home/pi/senders.txt','r') as senders:
                    emailS=json.load(senders)     
                with open('/home/pi/senderpassword.txt','r') as senderpassword:
                    emailP=json.load(senderpassword)
                numberofemails=len(emailR)
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(emailS[0],emailP[0])
                print(alarma)
                for x5 in range (len(freezer)):
                    nombre=nombre+freezer[x5]+', '
                    temperatura=temperatura+str(temp_cL[x5])+', '
                subject = '#FreezerAlarm'
                msg = 'Subject:{}\n\nThe temperature in the -80C freezers %s are %s respectively'.format(subject) %(nombre,temperatura)
                for x in range(numberofemails-1):
                    server.sendmail(emailS[0],emailR[x],msg)
                if alarma==2:
                    server.sendmail(emailS[0],'trigger@applet.ifttt.com',msg)
                server.quit
                time.sleep(600)

            except:
                time.sleep(10)
                counter=counter+1
                if counter==5:
                    counter=0
                    os.system("sudo reboot")
        currenttime=datetime.datetime.now()
        tiempoactual=currenttime.isoformat()
        timetosend=tiempoactual.split('T')
        timetosend1=timetosend[1].split('.')
        timetosend2=timetosend1[0].split(':')
        timetosend3=timetosend2[0]+':'+timetosend2[1]

        if int(timetosend2[0])==11 and int(timetosend2[1])>=40 and int(timetosend2[1])<=45:
            nombre=''
            temperatura=''
            try:
                with open('/home/pi/freezername.txt','r') as Freezername:
                    freezer=json.load(Freezername)
                with open('/home/pi/senderpassword.txt','r') as senderpassword:
                    emailP=json.load(senderpassword)
                with open('/home/pi/senders.txt','r') as senders:
                    emailS=json.load(senders)
                with open('/home/pi/recipients.txt','r') as recipients:
                    emailR=json.load(recipients)
                for x6 in range (len(freezer)):
                    nombre=nombre+freezer[x6]+', '
                    temperatura=temperatura+str(temp_cL[x6])

                subject = '#freezer alarm'
                msg = 'Subject:{}\n\nThe temperature in the -80C freezers %s are %s respectively'.format(subject) %(nombre,temperatura)
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(emailS[0],emailP[0])
                server.sendmail(emailS[0],emailS[0],msg)
                server.sendmail(emailS[0],emailR[0],msg)
                time.sleep(60)
                server.quit
            except:
                time.sleep(300)
                try:
                    nombre=''
                    temperatura=''
                    with open('/home/pi/freezername.txt','r') as Freezername:
                        freezer=json.load(Freezername)
                    with open('/home/pi/senderpassword.txt','r') as senderpassword:
                        emailP=json.load(senderpassword)
                    with open('/home/pi/senders.txt','r') as senders:
                        emailS=json.load(senders)
                    with open('/home/pi/recipients.txt','r') as recipients:
                        emailR=json.load(recipients)
                    nombre=freezer
                    for x7 in range (len(freezer)):
                        nombre=nombre+freezer[x7]+', '
                        temperatura=temperatura+str(temp_cL[x7])+', '
                    subject = '#freezer alarm'
                    msg = 'Subject:{}\n\nThe temperature in the -80C freezers %s are %s respectively'.format(subject) %(nombre,temperatura)
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                    server.login(emailS[0],emailP[0])
                    server.sendmail(emailS[0],emailS[0],msg)
                    server.sendmail(emailS[0],emailR[0],msg)
                    time.sleep(60)
                    server.quit
                except:
                    time.sleep(300)
                    try:
                        nombre=''
                        temperatura=''
                        with open('/home/pi/freezername.txt','r') as Freezername:
                            freezer=json.load(Freezername)
                        with open('/home/pi/senderpassword.txt','r') as senderpassword:
                            emailP=json.load(senderpassword)
                        with open('/home/pi/senders.txt','r') as senders:
                            emailS=json.load(senders)
                        with open('/home/pi/recipients.txt','r') as recipients:
                            emailR=json.load(recipients)
                        for x8 in range (len(freezer)):
                            nombre=nombre+freezer[x8]+', '
                            temperatura=temperatura+str(temp_cL[x8])+', '
                        subject = '#freezer alarm'
                        msg = 'Subject:{}\n\nThe temperatures in the -80C freezers %s are %s respectively'.format(subject) %(nombre,temperatura)
                        server = smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        server.login(emailS[0],emailP[0])
                        server.sendmail(emailS[0],emailS[0],msg)
                        server.sendmail(emailS[0],emailR[0],msg)
                        time.sleep(60)
                        server.quit
                    except:
                        time.sleep(10)
                        os.system("sudo reboot")

        return temp_cL
    while True:
        #global temperaturelist
        #global timelist
        temp_cL=read_temp()
        print(temp_cL)
        del temperaturelist[0]
        del timelist[0]
        temperaturelist.append(temp_cL)
        currenttime=datetime.datetime.now()
        tiempoactual=currenttime.isoformat()
        timelist.append(tiempoactual)
        with open('/home/pi/temperaturelist.txt','w') as templist:
            json.dump(temperaturelist,templist)
        with open('/home/pi/timelist.txt','w') as tiempolist:
            json.dump(timelist,tiempolist)
        time.sleep(300)
window.mainloop()

