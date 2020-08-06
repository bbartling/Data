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


    current_humidity = create_AV(
        oid=0, name="Current_Humidity", pv=0, pv_writable=False
    )
    current_humidity.units = EngineeringUnits("percent")
    current_humidity.description = CharacterString(
        "Current Humidity in percent relative humidity"
    )


    current_temp = create_AV(oid=1, name="Current_Temp", pv=0, pv_writable=False)
    current_temp.units = EngineeringUnits("degreesFahrenheit")
    current_temp.description = CharacterString("Current Temperature in degF")


    current_windspd = create_AV(
        oid=2, name="Current_Wind_Speed", pv=0, pv_writable=False
    )
    current_windspd.units = EngineeringUnits("milesPerHour")
    current_windspd.description = CharacterString(
        "Current Wind Speed"
    )


    current_winddir = create_AV(
        oid=3, name="Current_Wind_Dir", pv=0, pv_writable=False
    )
    current_winddir.units = EngineeringUnits("degreesAngular")
    current_winddir.description = CharacterString(
        "Current Wind Direction in degrees"
    )


    current_pressure = create_AV(
        oid=4, name="Current_Pressure", pv=0, pv_writable=False
    )
    current_pressure.units = EngineeringUnits("hectopascals")
    current_pressure.description = CharacterString(
        "Current Barometric Pressure"
    )


    current_cloudcov = create_AV(
        oid=5, name="Current_Cloud_Cover", pv=0, pv_writable=False
    )
    current_cloudcov.units = EngineeringUnits("percent")
    current_cloudcov.description = CharacterString(
        "Current Cloud Cover in Percent"
    )


    default_pv = CharacterString("empty")
    '''
    Strings for sunrise and sunset


    current_sunrise = create_CharStrValue(
        oid=6, name="Sunrise", pv=default_pv
    )
    current_sunrise.description = CharacterString(
        "Sunrise time"
    )


    current_sunset = create_CharStrValue(
        oid=7, name="Sunset", pv=default_pv
    )
    current_sunset.description = CharacterString(
        "Sunset time"
    )
    '''

    current_location = create_CharStrValue(
        oid=8, name="Weather_Station_City", pv=default_pv
    )
    current_location.description = CharacterString(
        "Location of Weather Station"
    )

    current_description = create_CharStrValue(
        oid=9, name="Current_Weather_Description", pv=default_pv
    )
    current_description.description = CharacterString(
        "Weather Station Description String"
    )



    # AV
    new_device.this_application.add_object(current_humidity)
    new_device.this_application.add_object(current_temp)
    new_device.this_application.add_object(current_windspd)
    new_device.this_application.add_object(current_winddir)
    new_device.this_application.add_object(current_pressure)
    new_device.this_application.add_object(current_cloudcov)

    # Strings
    #new_device.this_application.add_object(current_sunrise)
    #
    new_device.this_application.add_object(current_location)
    new_device.this_application.add_object(current_description)

    return new_device



class App:
    dev = start_device()
    weather = OpenWeather(city="duluth", units="imperial")


app = App()


def update():
    app.weather.update()
    current_humid = app.dev.this_application.get_object_name("Current_Humidity")
    current_temp = app.dev.this_application.get_object_name("Current_Temp")
    current_winddir = app.dev.this_application.get_object_name("Current_Wind_Dir")
    current_windspd = app.dev.this_application.get_object_name("Current_Wind_Speed")
    current_pressure = app.dev.this_application.get_object_name("Current_Pressure")
    current_cloudcov = app.dev.this_application.get_object_name("Current_Cloud_Cover")

    #current_sunrise = app.dev.this_application.get_object_name("Sunrise")
    #current_sunset = app.dev.this_application.get_object_name("Sunset")
    current_location = app.dev.this_application.get_object_name("Weather_Station_City")
    current_description = app.dev.this_application.get_object_name("Current_Weather_Description")




    new_temp = app.weather.temp
    new_hum = app.weather.hum
    new_winddir = app.weather.winddir
    new_windspd = app.weather.windspd
    new_pressure = app.weather.press
    new_cloudcov = app.weather.cloudcov

    #new_sunrise = app.weather.sunrise
    #new_sunset = app.weather.sunset
    new_location = app.weather.city
    new_description = app.weather.descrip


    app.dev._log.info("Setting Temp to {}".format(new_temp))
    current_temp.presentValue = new_temp

    app.dev._log.info("Setting Humidity to {}".format(new_hum))
    current_humid.presentValue = new_hum

    app.dev._log.info("Setting Wind Dir to {}".format(new_winddir))
    current_winddir.presentValue = new_winddir

    app.dev._log.info("Setting Wind Spd to {}".format(new_windspd))
    current_windspd.presentValue = new_windspd

    app.dev._log.info("Setting B Press to {}".format(new_pressure))
    current_pressure.presentValue = new_pressure

    app.dev._log.info("Setting Cloud Cov to {}".format(new_cloudcov))
    current_cloudcov.presentValue = new_cloudcov

    #app.dev._log.info("Setting Sunrise to {}".format(new_sunrise))
    #current_sunrise.presentValue = new_sunrise

    #app.dev._log.info("Setting Sunset to {}".format(new_sunset))
    #current_sunset.presentValue = new_sunset

    app.dev._log.info("Setting Location to {}".format(new_location))
    current_location.presentValue = new_location

    app.dev._log.info("Setting Description to {}".format(new_description))
    current_description.presentValue = new_description



def main():
    task_device = RecurringTask(update, delay=900)
    task_device.start()
    while True:
        pass


if __name__ == "__main__":
    main()
