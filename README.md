# iot
Documentation related to IOTstack setup on the raspberry pi 4.  

## Rapsberry Pi
[Start with a clean install from an image](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

After booting the pi, its usually a good idea to update it. ([docs](https://www.raspberrypi.org/documentation/raspbian/updating.md)):

```
sudo apt update
supo apt full-upgrade
```

Next enable some interfaces on the pi. ([docs](https://www.raspberrypi.org/documentation/remote-access/ssh/)):

```
sudo raspi-config
```

Select interfacing options and enable SSH, SPI, and I2C.

## IOTstack

Follow the steps [here](https://github.com/gcgarner/IOTstack):

```
sudo apt-get install git
git clone https://github.com/gcgarner/IOTstack.git ~/IOTstack
cd ~/IOTstack
./menu.sh
```

1. Install Docker
2. Build Stack: Portainer, Node-RED, InfluxDB, Grafana, Eclipse-Mosquitto, Python
3. Done.

Now set up the python [requirements.txt](https://github.com/gcgarner/IOTstack/wiki/Python):

```
RPI-GPIO
adafruit-blinka
paho-mqtt
```

These are optional step are needed if you want to use the ZigBee binding in OpenHAB:

Edit docker-compose.yml

```
openhab:
  environment:
    EXTRA_JAVA_OPTS: "-Duser.timezone=Europe/Berlin -Dgnu.io.rxtx.SerialPorts=/dev/ttyACM0:/dev/ttyAMA0"
  devices:
   - "/dev/ttyACM0:/dev/ttyACM0"
   - "/dev/ttyAMA0:/dev/ttyAMA0"
```

Edit scripts/start.sh ([docs](https://www.openhab.org/docs/installation/docker.html#explanation-of-arguments-passed-to-docker))

```
docker exec -d openhab /bin/chmod o+rw /dev/ttyACM0
docker exec -d openhab adduser openhab tty
```

Finally, start the containers and wait:

```
docker-compose up -d
```

Verify that containers are running (assuming your hostname is raspberrypi-iot:
portainer: http://raspberrypi-iot:9000
openhab: http://raspberrypi-iot:8080
node-RED: http://raspberrypi-iot:1880
graphana: http://raspberrypi-iot:3000

## OpenHAB Bindings

### [MQTT Binding](https://www.openhab.org/addons/bindings/mqtt/)
Thing: MQTT Broker
Broker Hostname/IP: localhost
Broker Port: 1883

### Thing: Generic MQTT Thing
Bridge Selection : previously configured Broker


Add Channel

Select Type

Enter a name and label.

MQTT command topic: openhab/test

link this to an existing item

 ### [Zigbee Binding](https://www.openhab.org/addons/bindings/zigbee/)
 
Thing: CC2531EMK Coordinator

Port: /dev/ttyACM0

Baud Rate: 115200

Channel: 11

PAN ID: 32867

Extended Pan Id: 91866D6B64CEA4ED

Network Security Key: A5F84382488DD12972F508F7448FB920

Magic Number: 239

## Sensors

[SGP30 air quality sensor](https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor)
