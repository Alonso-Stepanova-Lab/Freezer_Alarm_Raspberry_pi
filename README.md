# Freezer_Alarm_Raspberry_pi
If you are familiar with the Raspberry Pi you can use these files to run our Freezer Alarm in your Raspberry Pi. 
Once you have your Raspberry Pi up and running you need to make sure VNC and 1-Wire are enabled (Raspberry Pi Configuration--> Interfaces).
You need also to add the following line to your crontab (for that just open crontab using $ sudo crontab -e)
$ @reboot sudo python /home/pi/temperaturev5.py
"in a new line type"
0 8 * * * sudo python /home/pi/reset.py
"in a new line type"
0 20 * * * sudo python /home/pi/reset.py
You can now copy into /home/pi/ the three files temperaturev5.py, Temperature-raspiv4.py and reset.py
If you want to use a single RPi to monitor the temperature of several sensors you will need to use the multitempearturev1.py instead of the temperaturev5.py file, and the Multitemperature-raspiv1.py instad of the Temperature-raspiv4.py file. You will also need to change the @reboot sudo python /home/pi/temperaturev5.py to @reboot sudo python /home/pi/multitemperaturev1.py line.
You will also need to connect each one of your temperature sensors to the same three pins in the RPI (one resistor for all the sensors) as described here (https://alonsostepanova.wordpress.ncsu.edu/diy/). You will need 64 bit addresses for each one of the sensors to set up your alarm. To find these addresses you should connect the first sensor and then check for a file starting with 28 in the  /sys/bus/w1/devices directory of your RPi. That will be that sensor's address. Then connect the second sensor and a new address will appear in the devices directory. You will need these addresses when setting up your alarm using the Multitemperature-raspiv1.py script. After you have set up the alarm by running this python script in your RPI the alarm should be ready to go.
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

