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
def update_database():
    light, moisture = light_moisture_sensor()
    temperature, humidity = temp_humid_sensor()
    db.child("IOTGreenhouse").update({"humidity": humidity})
    db.child("IOTGreenhouse").update({"luminosity": light})
    db.child("IOTGreenhouse").update({"moisture": moisture})
    db.child("IOTGreenhouse").update({"temperature": temperature})


def fan(t):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    try:
        GPIO.output(17, True)
        time.sleep(t)
        GPIO.output(17, False)
    finally:
        GPIO.cleanup()


def sprinkle(t):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    try:
        GPIO.output(17, True)
        time.sleep(t)
        GPIO.output(17, False)
    finally:
        # cleanup the GPIO before finishing :)
        GPIO.cleanup()


def drip(t):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    try:
        GPIO.output(17, True)
        time.sleep(t)
        GPIO.output(17, False)
    finally:
        # cleanup the GPIO before finishing :)
        GPIO.cleanup()


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

    
update_flag = db.child("IOTGreenhouse").child("updateflag").get().val()
if update_flag == True:
    update_database()
    db.child("IOTGreenhouse").update({"updateflag": False})

automatic = db.child("IOTGreenhouse").child("automatic").get().val()

if automatic:
    humid_max = 65
    humid_min = 40

    temp, humid = temp_humid_sensor()
    if humid < humid_min:
        sprinkle(3)
    elif humid > humid_max:
        fan(3)

    moist_min = 80

    light, moisture = light_moisture_sensor()
    if moisture < moist_min:
        drip(3)
else:
    turn_on_dripping = db.child("IOTGreenhouse").child("turn on dripping").get().val()
    turn_on_sprinkling = db.child("IOTGreenhouse").child("turn on sprinkling").get().val()
    turn_on_fan = db.child("IOTGreenhouse").child("turn on fan").get().val()

    if turn_on_dripping:
        drip(3)
    if turn_on_sprinkling:
        sprinkle(3)
    if turn_on_fan:
        fan(3)
















