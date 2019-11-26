# Freezer_Alarm_Raspberry_pi
Disk image for the Raspberry pi freezer alarm
To make a copu of this disk image into a micro SD card that can be used as the boot system in a raspberry pi you use as a freezer larm. 
Download the disk image to your desktop
Connect a new 32 GB micro SD card to your computer (in this example a Mac)
Open the temrinal and check the name of the sd card by typing:
diskutil list
Find in the list of devices the one corresponding to your 32 GB card. In this example it the name of the SD card device is disk4. Make sure you identifiy the right device corresponding to the micro SD card as you will delete the content of the selected device in the following steps. In the commands you will type in your teerminal replace the disk4 of my example below for the device name of your micro SD card
In the terminal type:
diskutil unmountDisk /dev/disk4
press enter and then type in the next line
sudo newfs_msdos -F 16 /dev/disk4
press enter. You will be asked to enter a password, that is the password of your username in your computer. after it finished type in next line fo the terminal
sudo dd if=~/Desktop/raspberrypiMacPC4GB.dmg of=/dev/disk4 bs=1m
This will take 15-30 minutes. after it is finished you have a copy of the Raspberry pi freezer alarm booting system that you can directly insert in your Raspnberry pi
