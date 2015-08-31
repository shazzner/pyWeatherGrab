#!/usr/bin/env python
# Read weather data from serial input such as an Arduino
# Stores data into a mysql database
# TODO: Add comments

import getopt
import sys
import serial
from interruptingcow import timeout
import forecastio
from decimal import Decimal
import numpy as np
import MySQLdb as mdb
import time

def help():
    help_msg = 'pyWeatherGrab - grab weather sensor data via serial\n'\
    '\n'\
    '-h                                 Show this help\n'\
    '-i, --settings                     Load a mysql settings file, see exampleSettings file\n'\
    '-s, --serial-port <Serial Port>    Set the serial port - Default: /dev/ttyUSB0\n'\
    '-b, --baud <Baud Rate>             Set the baud rate - Default: 9600\n'
    

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
    apikey = ''
    lat = ''
    log = ''

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

                            if str(key).startswith('sw_baud'):
                                baud = str(val).strip()
                            elif str(key).startswith('sw_serial'):
                                serial_port = str(val).strip()
                            # Probably should do a dict like with mysql
                            # TODO: forecastio dict
                            elif str(key).startswith('fr_apikey'):
                                apikey = str(val).strip()
                            elif str(key).startswith('fr_lat'):
                                lat = str(val).strip()                                
                            elif str(key).startswith('fr_log'):
                                log = str(val).strip()
                            else:
                                mysql_settings[str(key)] = str(val).strip()
            except:
                print help()
                sys.exit(3)
        if o in ('-h', '--help'):
            print help()
            sys.exit(0)

    return (serial_port, baud, mysql_settings, apikey, lat, log)

def convertFtoC (fahrenheit):
    return round(Decimal(((fahrenheit - 32) * 5) / 9),1)

def convertHumidPercent (humidity):
    return str(humidity * 100)

if __name__ == '__main__':
    serial_port, baud, mysql_settings, APIKEY, LAT, LOG = parse_options()

    try:
        ser = serial.Serial(serial_port, baud)
    except serial.SerialException:
        print 'Could not create serial connection'
        sys.exit(3)

    datatemp = []
    datahumid = []

    # Droping timeout for testing
    # TODO: Change it to 10 or be configurable
    try:
        with timeout(5, exception=RuntimeError):
            while True:
                line = ser.readline().rstrip()
                if line:
                    try:
                        (temp, humid) = line.split(' ')
                        datatemp.append(temp.split(':')[1].strip('C'))
                        datahumid.append(humid.split(':')[1].strip('%'))
                    except:
                        pass
    except RuntimeError:
        pass

    # Ok now we've got some data
    # We'll remove the first and last ones, just in case we grabbed them weirdly via serial
    del datatemp[0]
    del datatemp[len(datatemp) - 1]
    del datahumid[0]
    del datahumid[len(datahumid) - 1]

    # We should now look at the data and remove any highs or lows possibly
    # TODO: some basic data manipulations

    capture_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    datatemp = np.array(map(float, datatemp))
    datahumid = np.array(map(float, datahumid))
    insidetemp = round(Decimal(np.average(datatemp)),1)
    insidehumid = round(Decimal(np.average(datahumid)),1)

    forecast = forecastio.load_forecast(APIKEY, LAT, LOG)
    curforecast = forecast.currently()

    forecast_icon = curforecast.icon

    forecast_outside_temp = convertFtoC(curforecast.temperature)

    forecast_outside_humid = convertHumidPercent(curforecast.humidity)

    forecast_outside_apparent_temp = convertFtoC(curforecast.apparentTemperature)
    
    # Let's insert our data in mysql

    # Support multiple databases ?

    try:
        con = mdb.connect(host='localhost', user=mysql_settings['db_user'], passwd=mysql_settings['db_pw'], db=mysql_settings['db_name'])

        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO " + mysql_settings['db_table'] + " (capture_time,curr_room_temp,curr_room_humid,local_outside_icon,local_outside_temp,local_outside_humid,local_outside_apparent_temp) VALUES (%s, %s, %s, %s, %s, %s, %s)", (capture_time, insidetemp, insidehumid, forecast_icon, forecast_outside_temp, forecast_outside_humid, forecast_outside_apparent_temp) )
    
            print "Database updated!"
    
    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
            
        if con:    
            con.close()
    
