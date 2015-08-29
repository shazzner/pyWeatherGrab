#!/usr/bin/env python
# Read weather data from serial input such as an Arduino

import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

def help():
    help_msg = 'pyWeatherGrab - grab weather sensor data via serial\n'\
    '\n'\
    '-h                                 Show this help\n'\
    '-s, --serial-port <Serial Port>    Set the serial port: ie /dev/ttyUSB0\n'\
    '-b, --baud <Baud Rate>             Set the baud rate\n'

    return help_msg

#while True:
#    print(ser.readline())

def parse_options():    
    try:
        long_options = ['serial-port', 'baud', 'help']
        opts, args = getopt.getopt(sys.argv[1:], "shp:w:", long_options)
    except getopt.GetoptError, e:
        print help()
        sys.exit(3)
    
if __name__ == '__main__':
    baud, stream = parse_options()

    baud = 9600
    
