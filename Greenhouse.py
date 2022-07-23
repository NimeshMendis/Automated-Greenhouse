import time
import pyrebase
import Adafruit_DHT
import spidev
import RPi.GPIO as GPIO
import smbus

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

def read(control):
    write = bus.write_byte(address, control)  # _data , 0
    read = bus.read_byte(address)
    return read

#tested
def temp_humid_sensor():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4

    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.")
    return temperature, humidity

def light_moisture_sensor():
    unused1 = read(0x40)
    moisture_raw = read(0x41)
    light_raw = read(0x42)
    unused2 = read(0x43)

    moisture = (moisture_raw / float(255) * 100)
    moisture = round(moisture, 2)

    light = (light_raw / float(255) * 100)
    light = round(light, 2)

    return light, moisture


#tested
def update_database(humidity, light, moisture, temperature):
    db.child("IOTGreenhouse").update({"humidity": humidity})
    db.child("IOTGreenhouse").update({"luminosity": light})
    db.child("IOTGreenhouse").update({"moisture": moisture})
    db.child("IOTGreenhouse").update({"temperature": temperature})


def fan(state):
    try:
        GPIO.output(17, state)
    except KeyboardInterrupt:
        print("done")


def sprinkle(state):
    try:
        GPIO.output(17, state)
    except KeyboardInterrupt:
        print("done")


def drip(state):
    try:
        GPIO.output(17, state)
    except KeyboardInterrupt:
        print("done")


def PWM():
    redLED = 18
    blueLED = 12

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(redLED, GPIO.OUT)
    GPIO.setup(blueLED, GPIO.OUT)

    red_pwm = GPIO.PWM(redLED, 1000)
    blue_pwm = GPIO.PWM(blueLED, 1000)

    red_pwm.start(0)
    blue_pwm.start(0)

    
#main code starts here

temp, humid = temp_humid_sensor()
light_level, moist = light_moisture_sensor()

update_database(humid, light_level, moist, temp)


automatic = db.child("IOTGreenhouse").child("automatic").get().val()

if automatic:
    temp_max = db.child("IOTGreenhouse").child("temp max").get().val()
    temp_min = db.child("IOTGreenhouse").child("temp max").get().val()
    humid_max = db.child("IOTGreenhouse").child("humid max").get().val()
    humid_min = db.child("IOTGreenhouse").child("humid min").get().val()
    moist_min = db.child("IOTGreenhouse").child("moist min").get().val()
    moist_max = db.child("IOTGreenhouse").child("moist max").get().val()

    if temp < temp_max:
        fan(True)
    elif temp < temp_min:
        fan(False)

    if humid > humid_max:
        sprinkle(True)
    elif humid < humid_min:
        sprinkle(False)

    if moist < moist_min:
        drip(True)
    elif moist > moist_max:
        drip(False)
else:
    turn_on_dripping = db.child("IOTGreenhouse").child("turn on dripping").get().val()
    turn_on_sprinkling = db.child("IOTGreenhouse").child("turn on sprinkling").get().val()
    turn_on_fan = db.child("IOTGreenhouse").child("turn on fan").get().val()

    if turn_on_dripping:
        drip(True)
    else:
        drip(False)
    if turn_on_sprinkling:
        sprinkle(True)
    else:
        sprinkle(False)
    if turn_on_fan:
        fan(True)
    else:
        fan(False)















