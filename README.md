# Freezer_Alarm_Raspberry_pi
If you are familiar with the Raspberry Pi you can use these files to run our Freezer Alarm in your Raspberry Pi. 
Once you have your Raspberry Pi up and running you need to make sure VNC and 1-Wire are enabled (Raspberry Pi Configuration--> Interfaces).
You need also to add the following line to your crontab (for that just open crontab using $ sudo crontab -e)
$ @reboot sudo python /home/pi/temperaturev5.py
"in a new line type"
0 8 * * * sudo python /home/pi/reset.py
"in a new line type"
0 20 * * * sudo python /home/pi/reset.py
You cannot copy into /home/pi/ the three files temperaturev5.py, Temperature-raspiv4.py and reset.py
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
$ sudo python Temeperature-raspiv4.py to set your Alarm System.

