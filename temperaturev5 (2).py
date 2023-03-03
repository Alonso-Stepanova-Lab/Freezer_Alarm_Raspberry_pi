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



time.sleep(30)
#global setT
#global setTL
#global counter
counter=0
#temperaturelist=[0]*10000
#timelist=['a']*10000
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir + '28*')[0]
device_file=device_folder + '/w1_slave'
with open('/home/pi/alarmset.txt','r') as alarmset:
    setT=json.load(alarmset) 
with open('/home/pi/alarmsetL.txt','r') as alarmsetL:
    setTL=json.load(alarmsetL)
    
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
        
def read_temp_raw():
    f=open(device_file, 'r')
    lines=f.readlines()
    f.close()
    return lines
def read_temp():
    global counter
    lines=read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines=read_temp_raw()
    equals_pos=lines[1].find('t=')
    if equals_pos !=-1:
        temp_string=lines[1][equals_pos+2:]
        temp_c=float(temp_string)/1000.0
        temp_f=temp_c*9.0/5.0+32.0
        if temp_c>=setT or temp_c<=setTL:
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
                nombre=freezer[0]
                subject = '#FreezerAlarm'
                msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
                for x in range(numberofemails-1):
                    server.sendmail(emailS[0],emailR[x],msg)
                if temp_c>=setT+10 or temp_c<=setTL-5:
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
            try:
                with open('/home/pi/freezername.txt','r') as Freezername:
                    freezer=json.load(Freezername)
                with open('/home/pi/senderpassword.txt','r') as senderpassword:
                    emailP=json.load(senderpassword)
                with open('/home/pi/senders.txt','r') as senders:
                    emailS=json.load(senders)
                with open('/home/pi/recipients.txt','r') as recipients:
                    emailR=json.load(recipients)
                nombre=freezer[0]
                subject = '#freezer alarm'
                msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
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
                    with open('/home/pi/freezername.txt','r') as Freezername:
                        freezer=json.load(Freezername)
                    with open('/home/pi/senderpassword.txt','r') as senderpassword:
                        emailP=json.load(senderpassword)
                    with open('/home/pi/senders.txt','r') as senders:
                        emailS=json.load(senders)
                    with open('/home/pi/recipients.txt','r') as recipients:
                        emailR=json.load(recipients)
                    nombre=freezer[0]
                    subject = '#freezer alarm'
                    msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
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
                        with open('/home/pi/freezername.txt','r') as Freezername:
                            freezer=json.load(Freezername)
                        with open('/home/pi/senderpassword.txt','r') as senderpassword:
                            emailP=json.load(senderpassword)
                        with open('/home/pi/senders.txt','r') as senders:
                            emailS=json.load(senders)
                        with open('/home/pi/recipients.txt','r') as recipients:
                            emailR=json.load(recipients)
                        nombre=freezer[0]
                        subject = '#freezer alarm'
                        msg = 'Subject:{}\n\nThe temperature in the -80C freezer %s is %f'.format(subject) %(nombre,temp_c)
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
    
        return temp_c, temp_f
while True:
    #global temperaturelist
    #global timelist
    (tempc,tempf)=read_temp()
    print(tempc)
    del temperaturelist[0]
    del timelist[0]
    temperaturelist.append(tempc)
    currenttime=datetime.datetime.now()
    tiempoactual=currenttime.isoformat()
    timelist.append(tiempoactual)
    try:
        with open('/home/pi/temperaturelist.txt','w') as templist:
            json.dump(temperaturelist,templist)
        with open('/home/pi/timelist.txt','w') as tiempolist:
            json.dump(timelist,tiempolist)
    except:
        temperaturelist=[0]*10000
        timelist=['a']*10000
        os.remove('/home/pi/temperaturelist.txt')
        os.remove('/home/pi/timelist.txt')
        with open('/home/pi/temperaturelist.txt','w') as templist:
            json.dump(temperaturelist,templist)
        with open('/home/pi/timelist.txt','w') as tiempolist:
            json.dump(timelist,tiempolist)       
        
        
        
    time.sleep(300)
