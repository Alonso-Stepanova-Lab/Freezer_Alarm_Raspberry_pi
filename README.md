# Freezer_Alarm_Raspberry_pi
If you are familiar with the Raspberry Pi you can use these files to run our Freezer Alarm in your Raspberry Pi. 
Once you have your Raspberry Pi up and running you need to make sure VNC and 1-Wire are enabled (Raspberry Pi Configuration--> Interfaces).
You need also to add the following line to your crontab (for that just open crontab using $ sudo crontab -e)
$ @reboot sh /home/pi/launcher.sh > /home/pi/cronlog 2>$1
You cannot copy into /home/pi/ the three files temperaturev3.py, Temperature-raspiv3.py and launcher.sh
You need to make launcher.sh executable using $ chmod 755 launcher.sh
To make sure your sensor is working type
$ sudo modprobe w1-therm
$ cd /sys/bus/w1/devices
$ ls
there should be a directory starting with the number 28. Go to that directory
$ cd 28.....
type the following command
$ cat w1_slave
reboot your system and it should be ready to go
type 
$ sudo python Temeperature-raspiv3.py to set your Alarm System.

