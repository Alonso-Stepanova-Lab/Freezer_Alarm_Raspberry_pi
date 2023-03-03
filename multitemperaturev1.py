import os
import glob
import time
import sys
import smtplib
if sys.version_info[0] <3:
    import Tkinter as tk
    from Tkinter import *
else:
    import tkinter as tk
    from tkinter import *
import json
import datetime



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
#with open('/home/pi/temperaturelist.txt','r') as tempL:
#    temperaturelist=json.load(tempL)
#with open('/home/pi/timelist.txt','r') as timeL:
#    timelist=json.load(timeL)
try:
    with open('/home/pi/temperaturelist.txt','r') as tempL:
        temperaturelist=json.load(tempL)
    with open('/home/pi/timelist.txt','r') as timeL:
        timelist=json.load(timeL)
except:
    temperaturelist=[0]*10000
    timelist=['a']*10000
    os.remove('/home/pi/temperaturelist.txt')
    os.remove('/home/pi/timelist.txt')
    with open('/home/pi/temperaturelist.txt','w') as templist:
        json.dump(temperaturelist,templist)
    with open('/home/pi/timelist.txt','w') as tiempolist:
        json.dump(timelist,tiempolist)

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
    alarma1=0
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
            alarma1=2
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
            if alarma1==2:
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
                temperatura=temperatura+str(temp_cL[x6])+', '
            
            subject = '#freezer alarm 27'
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
                subject = '#freezer alarm 27'
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
                    subject = '#freezer alarm 27'
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
    try:
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
    except:
        time.sleep(1)
        temperaturelist=[0]*10000
        timelist=['a']*10000
        os.remove('/home/pi/temperaturelist.txt')
        os.remove('/home/pi/timelist.txt')
        with open('/home/pi/temperaturelist.txt','w') as templist:
            json.dump(temperaturelist,templist)
        with open('/home/pi/timelist.txt','w') as tiempolist:
            json.dump(timelist,tiempolist)   
    time.sleep(300)
