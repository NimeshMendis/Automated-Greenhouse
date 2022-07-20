
import smbus
import Adafruit_DHT
import time
import pyrebase
DHT_SENSOR = 11
#Adafruit_DHT.DHT11
DHT_PIN = 4
sleepTime = 1

firebaseConfig = {
  "apiKey": "AIzaSyA1cZhgLy_rE6I23zvKhg4Gy3LpfJJJ6tk",
  "authDomain": "greenhouseautomation-8af0f.firebaseapp.com",
  "databaseURL": "https://greenhouseautomation-8af0f-default-rtdb.firebaseio.com",
  "storageBucket": "greenhouseautomation-8af0f.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

bus = smbus.SMBus(1)
address = 0x48
def read (control):
    write = bus.write_byte(address, control) #_data , 0
    read = bus.read_byte(address)
    return read
while True:
    poti = read(0x40)
    moisture= read(0x41)
    light = read(0x42)
    ain2 = read(0x43)
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    print ("Moisture level:", moisture, "Light level:", light, "Temp:", temperature,"C", "Humidity:", humidity,"%")
    
    
    db.child("IOTGreenhouse").update({"humidity": humidity})
    db.child("IOTGreenhouse").update({"luminosity": light})
    db.child("IOTGreenhouse").update({"moisture": moisture})
    db.child("IOTGreenhouse").update({"temperature": temperature})
    time.sleep(sleepTime)

