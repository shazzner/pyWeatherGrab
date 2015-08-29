#!/usr/bin/env python
# Read weather data from serial input such as an Arduino

import getopt
import sys
import serial
import time

#ser = serial.Serial('/dev/ttyACM0', 9600)

def help():
    help_msg = 'pyWeatherGrab - grab weather sensor data via serial\n'\
    '\n'\
    '-h                                 Show this help\n'\
    '-s, --serial-port <Serial Port>    Set the serial port - Default: /dev/ttyUSB0\n'\
    '-b, --baud <Baud Rate>             Set the baud rate - Default: 9600\n'

    return help_msg

#while True:
#    print(ser.readline())

def parse_options():
    try:
        long_options = ['serial-port', 'baud', 'help']
        opts, args = getopt.getopt(sys.argv[1:], "s:hb:", long_options)
    except getopt.GetoptError, e:
        print help()
        sys.exit(3)

    # Default options
    serial_port = '/dev/ttyACM0'
    baud = 9600
    #stream = False

    for o, a in opts:
        if o in ('-s', '--serial-port'):
            try:
                serial_port = str(a)
            except:
                print help()
                sys.exit(3)
        if o in ('-b', '--baud'):
            try:
                baud = int(a)
            except:
                print help()
                sys.exit(3)
        if o in ('-h', '--help'):
            print help()
            sys.exit(0)

    return (serial_port, baud)
    
if __name__ == '__main__':
    serial_port, baud = parse_options()
    print 'Serial port: ', serial_port
    print 'Baud: ', baud
    sys.exit(0)
