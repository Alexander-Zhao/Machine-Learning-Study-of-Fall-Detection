import machine
from imu import MPU6050
from machine import I2C, Pin
from utime import sleep, ticks_ms, ticks_diff
from ssd1306 import SSD1306_I2C
import time
import uos

#need this UART to read from MPU6050 and be abel to send data to local computer
#Key Points of UART Setup:
#The UART(0, baudrate=115200) initializes UART0 with a baud rate of 115200.
#Pins 0 and 1 are set as TX (transmit) and RX (receive) respectively,
#which will be used for UART communication.
#Once the data is obtained, you can send it over UART to the computer.
#Data Transmission to PC: The uos.dupterm(uart) duplicates the UART object
#to the MicroPython terminal, allowing you to use the UART connection
#to send data to your computer.
uart = machine.UART(0, baudrate=115200)
uart.init(115200, bits =8, parity= None, stop =1, tx=Pin(0), rx=Pin(1))
uos.dupterm(uart)

#setup I2C bus and mpu
#Reading MPU6050 Data: The MPU6050 sensor communicates via I2C, not UART.
#Therefore, you will need to use I2C to interface with the MPU6050 and read the sensor data.
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

def get_gyro():
    gx=mpu.gyro.x
    gy=mpu.gyro.y
    gz=mpu.gyro.z
    return gx, gy, gz


def get_accelerate():
    ax=mpu.accel.z
    ay=mpu.accel.y
    az=mpu.accel.z
    return ax, ay, az

while True:
    (gx, gy, gz) = get_gyro()
    (ax, ay, az) = get_accelerate()
    #print("az",az,"\t","az_after_calib",az_after_calib,"\t", "gx",gx,"\t","gx_after_calib",gx_after_calib,"\t","gy",gy,"\t","gy_after_calib",gy_after_calib,"\t","gz",gz,"\t","gz_after_calib",gz_after_calib,"\t\n")\
    #print('{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}', ax,ay, az, gx, gy, gz)
    print(ax,ay, az, gy, gy, gz)
    # Print values to UART
    uart.write(f"Acceleration: x={ax:.2f}, y={ay:.2f}, z={az:.2f}\n")
    uart.write(f"Gyroscope: x={gx:.2f}, y={gy:.2f}, z={gz:.2f}\n")
    time.sleep(0.005)

uart.write(b"EOF")