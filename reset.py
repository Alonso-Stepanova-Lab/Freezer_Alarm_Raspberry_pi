import smtplib
import os
try:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("alonsobellverraspberrypi@gmail.com","TAronjes")
except:
    os.system("sudo reboot")
