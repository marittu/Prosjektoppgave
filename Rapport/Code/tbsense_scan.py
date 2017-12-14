from bluepy.btle import *
import struct
from tbsense import Thunderboard
import threading
from post_db import post
from get_leds import read_db
from datetime import datetime
from time import sleep


def getThunderboards():
    scanner = Scanner(0)
    devices = scanner.scan(3)
    tbsense = dict()
    for dev in devices:
        scanData = dev.getScanData()
        for (adtype, desc, value) in scanData:
            if desc == 'Complete Local Name':
                if 'Thunder Sense #' in value:
                    deviceId = int(value.split('#')[-1])
                    tbsense[deviceId] = Thunderboard(dev)

    return tbsense

def sensorLoop(tb, devId):
   
    while True:
        data = dict()
        
        try:
            for key in tb.char.keys():

                if key == 'temperature':
                        data['temperature'] = tb.readTemperature()

                elif key == 'humidity':
                    data['humidity'] = tb.readHumidity()

                elif key == 'ambientLight':
                    data['ambientLight'] = tb.readAmbientLight()

                elif key == 'sound':
                    data['sound'] = tb.readSound()

        except:
            return

        post(devId, data) #Posts sensor data to database
    	read_db(tb, devId) #Read Led data from database
    	sleep(1)


def dataLoop( thunderboards):
    threads = []
    for devId, tb in thunderboards.items():
        t = threading.Thread(target=sensorLoop, args=(tb, devId))
        threads.append(t)
        print('Starting thread {} for {}'.format(t, devId))
        t.start()


if __name__ == '__main__':   

    while True:
        thunderboards = getThunderboards()
	
        if len(thunderboards) == 0:
	    pass
        else:
            dataLoop(thunderboards)
        

	
