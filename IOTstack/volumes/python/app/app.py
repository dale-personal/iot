import time
import board
import busio
import adafruit_sgp30
import paho.mqtt.client as mqtt

print("create python client")
client = mqtt.Client("python")

print("connect to localhost:1883")
client.connect("localhost", port=1883)

print("create i2c")
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

print("create sgp30")
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("Serial #", [hex(i) for i in sgp30.serial])

print("init")
sgp30.iaq_init()

print("set baseline")
sgp30.set_iaq_baseline(0x8973, 0x8AAE)

print("entering loop")

counter = 0

while True:
    eCO2, TVOC = sgp30.iaq_measure()
    print("eCO2: %d ppm, TVOC: %d ppb" % (eCO2, TVOC))
    counter += 1
    if counter > 12:
        counter = 0
        print("co2 base = 0x%x, tvoc base = 0x%x" % (sgp30.baseline_eCO2, sgp30.baseline_TVOC))
    client.publish("sensor/iaq", "{ \"eCO2\": %d, \"TVOC\": %d }" % (eCO2, TVOC))
    time.sleep(5)
