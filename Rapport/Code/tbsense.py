from bluepy.btle import *
import struct
from time import sleep

class Thunderboard:

   def __init__(self, dev):
      self.dev  = dev
      self.char = dict()
      self.name = ''
      self.session = ''
     
      # Get device name and characteristics
      scanData = dev.getScanData()

      for (adtype, desc, value) in scanData:
         if (desc == 'Complete Local Name'):
            self.name = value

      ble_service = Peripheral()
      ble_service.connect(dev.addr, dev.addrType)
      characteristics = ble_service.getCharacteristics()
     
      for k in characteristics:
         if k.uuid == '2a6e':
            self.char['temperature'] = k

         elif k.uuid == '2a6f':
            self.char['humidity'] = k
            
         elif k.uuid == 'c8546913-bfd9-45eb-8dde-9f8754f4a32e':
            self.char['ambientLight'] = k

         elif k.uuid == 'c8546913-bf02-45eb-8dde-9f8754f4a32e':
            self.char['sound'] = k
            print(k.read())
           
         elif k.uuid == 'fcb89c40-c603-59f3-7dc3-5ece444a401b':
            self.char['led'] = k      

   #Helper functions to convert GATT characteristic values to numbers
   
   def readTemperature(self):
      value = self.char['temperature'].read()
      value = struct.unpack('<H', value)
      value = value[0] / 100
      return value

   def readHumidity(self):
      value = self.char['humidity'].read()
      value = struct.unpack('<H', value)
      value = value[0] / 100
      return value

   def readAmbientLight(self):
      value = self.char['ambientLight'].read()
      value = struct.unpack('<L', value)
      value = value[0] / 100
      return value

   def readSound(self):
      value = self.char['sound'].read()
      value = struct.unpack('<h', value)
      value = value[0] / 100
      return value
   
   #RGB LEDs have 4 bytes to write. First byte determines which LEDs to turn on, next three bytes are colors for red, green and blue, respectively   

   def LedOn(self):      
      self.char['led'].write('\x0F\x00\x00\x70', withResponse=True) 
      

   def LedOff(self):  
      self.char['led'].write('\x00\x00\x00\x00', withResponse=True)

