# Freezer_Alarm_Raspberry_pi
If you are familiar with the Raspberry Pi you can use these files to run our Freezer Alarm in your Raspberry Pi. 
Once you have your Raspberry Pi up an running you need to make sure VNC and 1-Wire are enabled (Raspberry Pi Configuration--> Interfaces)
You need also to add the following line to your crontab (for that just open crontab using $ sudo crontab -e)
@reboot sh /home/pi/launcher.sh > /home/pi/cronlog 2>$1
You can not copy into /home/pi/ the three files temperaturev3.py, Temperature-raspiv3.py and launcher.sh
You need to make launcher.sh execuable using $ chmod 755 launcher.sh
