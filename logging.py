

import serial
import time
import csv
import os


os.chdir('/home/pi/csvdata')






def mainloop():
    name = time.strftime('%b %d %Y %H:%M:%S')
    f = open(name + '.csv', 'wt')
    writer = csv.writer(f, delimiter=',')
 
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
 
    for t in range(1000000):
        data = ser.read(1)
        if data:
            data += ser.read(ser.inWaiting())
            for line in data.split('\r\n'):
                if not line.strip(): continue # skip to next reading
                text = time.strftime('%X %x'),line.strip()                
                writer.writerow(text)
                f.flush()
                print text
 
    if t == 999999:
        print ("why")
        f.close()
        ser.close()
        mainloop()
 
mainloop()
