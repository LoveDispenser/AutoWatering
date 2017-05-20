# LoveDispensers Automatic watering system + temperature and humidity measurement
originally made for a spacebucket

_________________________

Hi, Im sharing my project and I will descripe what you need to do to get it working the way I did it. Im not a programmer, just a hobbyist, I had to learn a lot to do this and Im sure it can be done more professionally, but this stuff works and thats what matters.

_________________________

Brief overview:

Its very basic.
Raspberry PI powers the Arduino through usb cable. Arduino controls relay to water the plants and sends sensor data to Raspberry PI, which logs it, stores in .csv files and plots it every 5 minutes and saves .png file of the graph. 

Automatic watering works like this- it gets soil humidity sensor readings from the Chirp soil moisture sensor, if it is below the user-defined value, it closes the relay, and the pump stars working and watering the plants. 

To get the temperature and moisture readings, it uses 2 DHT22 sensors, gets the average values, rounds the number and thats your temperature and humidity.

_________________________

To do autowatering system and temperature+humidity measurement, you will need:

Raspberry PI Zero W
Arduino Uno
Water pump + power supply
Two DHT22 temp and humidity sensors
Chirp! Soil moisture sensor (important: you need the rugged version, because you will be keeping it in soil for long time)
Relay board for Arduino


_________________________

How to do it:

1. Install operating system to Raspberry Pi. I used PiBakery. You can configure your wifi settings, username and password, before install with an ease using this. Be sure to install VNC software to the PI also, so you can control the Raspberry PI Over wifi from your desktop PC.

2. Install Arduino software on Windows or Raspberry PI.

3. Copy the Arduino code from GitHub page to your Arduino software and upload it to Arduino (you will need to install the DHT library for your Arduino compiler software, found here: https://github.com/adafruit/DHT-sensor-library . 

4. Set-up webserver for your Raspberry PI so you can put and get files from it over LAN. I used this tutorial for Samba - https://pimylifeup.com/raspberry-pi-nas/ . If you get file names scrambled, its because Linux can have some symbols in files names that windows can't use. Check the comments for that tutorial for some help.

5. Get the python scripts from GitHub and place them to your raspberry PI /home/pi/csvdata

6. Open terminal and write "sudo crontab -e". This will open crontab which can be used to schedule the excecution of programs on Raspberry PI. We want to make it begin logging the sensor data and plotting graph automatically, when the Raspberry PI turns on. Type these commands at the end of the crontab file:

>@reboot sudo python /home/pi/csvdata/logging.py > /home/pi/logs/log.txt
>*/5 * * * * sudo python /home/pi/csvdata/plotting.py > /home/pi/logs/plotlog.txt

Example photo http://imgur.com/a/1vtiP

First command will run the sensor logging script, which creates a new .csv file with current date and starts writing sensor data.
Second command will excecute plotting script every 5 minutes. It will read the latest .csv file in the folder and plot its data and save .png file with the name of the csv file (also it should also save onto plot.png file everytime but it somehow doesn't work lol)
It will also log your python scripts activities to log files in the /home/pi/logs folder. I'd suggest you create that folder before running scripts.


7. Connect everything like in this picture: and everything should work now. 


_________________________

Notes:

The humidity in the graph appears as for example 140 instead of 40, this is to separate the graph itself from the temperature graph. Just remove the 1 in your mind when you're reading it.

To setup when the system starts watering the plant, open up your arduino code and change value "350" to something that works for you in this line:

>if (20 < readI2CRegistepump6bit(0x20, 0)  && readI2CRegistepump6bit(0x20, 0)  < 350) {

>(350 is what worked for me, but it will be different for you, just check the values your sensor is writing to csv file when your plant needs watering and write in that)

To change the time for the pump to be working, change value "400000" to your desired value in this line:

>delay(400000);

>(this value is milliseconds, turn on your pump to water your plants, start the timer and when you see the runoff, take the time it took to water your plant and convert it to milliseconds)

