# Automated-Greenhouse
Automated Greenhouse developed for Engineering Design Project at SLTC research university in 2022.

## Features

- Monitor greenhouse conditions such as temperature, humidity, moisture and light.
- Control relays and fans to manually change the conditions.
- Automate conditions to stay within accepted ranges.
- Collect data for long term analysis.

## Setup

Raspberry Pi 3b or 4 recommended. Install the dependencies, connect hardware and run Greenhouse.py.

```bash
sudo apt-get install python3-smbus python3-dev i2c-tools
```

```bash
pip install -r requirements.txt
```
To modify the mobile application open IOTGreenhouse4.aia using kodular.

## Hardware

Following Hardware is used for the project. Please make adjustments to the script accordingly if the sensors are different.

- Raspberry Pi 3b
- DHT 11 remperature and humidity sensor
- Capacitive moisture sensor
- TEMT6000 professional light sensor
- Generic relays, fans and LEDs
