#!/usr/bin/env python
# Read weather data from serial input such as an Arduino
# Stores data into a mysql database

import getopt
import sys
import serial
import time

def help():
    help_msg = 'pyWeatherGrab - grab weather sensor data via serial\n'\
    '\n'\
    '-h                                 Show this help\n'\
    '-i, --settings                     Load a mysql settings file, see exampleSettings file\n'\
    '-s, --serial-port <Serial Port>    Set the serial port - Default: /dev/ttyUSB0\n'\
    '-b, --baud <Baud Rate>             Set the baud rate - Default: 9600\n'\
    '-w, --watch                        Just watch the raw serial output\n'

    return help_msg

def parse_options():
    try:
        long_options = ['serial-port', 'baud', 'help', 'settings']
        opts, args = getopt.getopt(sys.argv[1:], "s:hb:i:", long_options)
    except getopt.GetoptError, e:
        print help()
        sys.exit(3)

    # Default options
    serial_port = '/dev/ttyACM0'
    baud = 9600
    mysql_settings = {}

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
        if o in ('-i', '--settings'):
            try:
                # TODO: Add some exception handling here
                with open(a) as f:
                    for line in f:
                        line = line.rstrip()
                        if line and not line.startswith('#'):
                            (key, val) = line.split(':')
                            mysql_settings[str(key)] = str(val).strip()
            except:
                print help()
                sys.exit(3)
        if o in ('-h', '--help'):
            print help()
            sys.exit(0)

    return (serial_port, baud, mysql_settings)
    
if __name__ == '__main__':
    serial_port, baud, mysql_settings = parse_options()

    print mysql_settings
    sys.exit(0)
    print 'Serial port: ', serial_port
    print 'Baud: ', baud
    try:
        ser = serial.Serial(serial_port, baud)
    except serial.SerialException:
        print 'Could not create serial connection'
        sys.exit(3)

    while True:
        print(ser.readline())

    
