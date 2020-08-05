#!/usr/bin/env python

import BAC0, time, requests
from BAC0.core.utils.notes import note_and_log

from bacpypes.basetypes import EngineeringUnits, DateTime
from bacpypes.primitivedata import CharacterString, Date, Time, Real

from BAC0.core.devices.create_objects import (
    create_AV,
    create_MV,
    create_BV,
    create_AI,
    create_BI,
    create_AO,
    create_BO,
    create_CharStrValue,
    create_DateTimeValue,
)

from BAC0.tasks.RecurringTask import RecurringTask

import time
from meteo_parser import OpenWeather


def start_device():
    print("Starting BACnet device")
    new_device = BAC0.lite()
    new_device._log.info('Device ID : {}'.format(new_device.Boid))
    time.sleep(10)

    av = []
    current_humidity = create_AV(
        oid=0, name="Current_Humidity", pv=0, pv_writable=False
    )
    current_humidity.units = EngineeringUnits("percent")
    current_humidity.description = CharacterString(
        "Current Humidity in percent relative humidity"
    )
    av.append(current_humidity)

    current_temp = create_AV(oid=1, name="Current_Temp", pv=0, pv_writable=False)
    current_temp.units = EngineeringUnits("degreesFahrenheit")
    current_temp.description = CharacterString("Current Temperature in degF")
    av.append(current_temp)

    '''
    current_sunrise = create_AV(
        oid=3, name="Sunrise", pv=0, pv_writable=False
    )
    current_sunrise.description = CharacterString(
        "Sunrise time"
    )
    av.append(current_sunrise)

    current_sunset = create_AV(
        oid=4, name="Sunset", pv=0, pv_writable=False
    )
    current_sunset.description = CharacterString(
        "Sunset time"
    )
    av.append(current_sunset)
    '''
    current_windspd = create_AV(
        oid=5, name="Current_Wind_Speed", pv=0, pv_writable=False
    )
    current_windspd.units = EngineeringUnits("milesPerHour")
    current_windspd.description = CharacterString(
        "Current Wind Speed"
    )
    av.append(current_windspd)

    current_winddir = create_AV(
        oid=6, name="Current_Wind_Dir", pv=0, pv_writable=False
    )
    current_winddir.units = EngineeringUnits("degreesAngular")
    current_winddir.description = CharacterString(
        "Current Wind Direction in degrees"
    )
    av.append(current_winddir)

    current_pressure = create_AV(
        oid=7, name="Current_Pressure", pv=0, pv_writable=False
    )
    current_pressure.units = EngineeringUnits("hectopascals")
    current_pressure.description = CharacterString(
        "Current Barometric Pressure"
    )
    av.append(current_pressure)

    current_cloudcov = create_AV(
        oid=8, name="Current_Cloud_Cover", pv=0, pv_writable=False
    )
    current_cloudcov.units = EngineeringUnits("percent")
    current_cloudcov.description = CharacterString(
        "Current Cloud Cover in Percent"
    )
    av.append(current_cloudcov)


    for each in av:
        new_device.this_application.add_object(each)
    return new_device


class App:
    dev = start_device()
    weather = OpenWeather(city="duluth", units="imperial")


app = App()


def update():
    app.weather.update()
    current_humid = app.dev.this_application.get_object_name("Current_Humidity")
    current_temp = app.dev.this_application.get_object_name("Current_Temp")
    '''
    current_sunrise = app.dev.this_application.get_object_name("Sunrise")
    current_sunset = app.dev.this_application.get_object_name("Sunset")
    '''
    current_winddir = app.dev.this_application.get_object_name("Current_Wind_Dir")
    current_windspd = app.dev.this_application.get_object_name("Current_Wind_Speed")
    current_pressure = app.dev.this_application.get_object_name("Current_Pressure")
    current_cloudcov = app.dev.this_application.get_object_name("Current_Cloud_Cover")


    new_temp = app.weather.temp
    new_hum = app.weather.hum
    '''
    new_sunrise = app.weather.sunrise
    new_sunset = app.weather.sunset
    '''
    new_winddir = app.weather.winddir
    new_windspd = app.weather.windspd
    new_pressure = app.weather.press
    new_cloudcov = app.weather.cloudcov


    app.dev._log.info("Setting Temp to {}".format(new_temp))
    current_temp.presentValue = new_temp

    app.dev._log.info("Setting Humidity to {}".format(new_hum))
    current_humid.presentValue = new_hum
    '''
    app.dev._log.info("Setting Sunrise to {}".format(new_sunrise))
    current_sunrise.presentValue = new_sunrise

    app.dev._log.info("Setting Sunset to {}".format(new_sunset))
    current_sunset.presentValue = new_sunset
    '''
    app.dev._log.info("Setting Wind Dir to {}".format(new_winddir))
    current_winddir.presentValue = new_winddir

    app.dev._log.info("Setting Wind Spd to {}".format(new_windspd))
    current_windspd.presentValue = new_windspd

    app.dev._log.info("Setting B Press to {}".format(new_pressure))
    current_pressure.presentValue = new_pressure

    app.dev._log.info("Setting Cloud Cov to {}".format(new_cloudcov))
    current_cloudcov.presentValue = new_cloudcov

def main():
    task_device = RecurringTask(update, delay=900)
    task_device.start()
    while True:
        pass


if __name__ == "__main__":
    main()
