import smtplib
import os
try:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("your email","your password")
except:
    os.system("sudo reboot")
