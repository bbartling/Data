
import asyncio
import pandas as pd
from datetime import datetime
import random
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import BAC0

daysOfData = 2
minuteCycles = 24*60*daysOfData
hourCycles = 24*daysOfData
secondsInDay = 86400
secondsInHour = 3600
secondsInMinute = 60

#start BACnet service, runs on seperate thread
bacnet = BAC0.lite()

#data storage for worker 1 & 2, worker 3 clears sends to sql
data = []

#used for weather data web scrape to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



async def firstWorker():#outsideAir Temp web scrape once per hour drybulb °F
    for _ in range(hourCycles):
        await asyncio.sleep(secondsInHour)
        things = {}
        stamp = datetime.now()
        r = requests.get('https://www.google.com/search?q=weather%20duluth', headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        outTemp = soup.find("span", {"class": "wob_t"}).text
        intOutTemp = int(outTemp)
        print(f'Outside temperature data {intOutTemp} deg F')
        things['Date'] = stamp
        things['Oat'] = intOutTemp
        data.append(things)



async def secondWorker():#electricMeter once per minute simulate kW
    for _ in range(minuteCycles):
        await asyncio.sleep(secondsInMinute)
        stuff = {}
        stamp = datetime.now()
        elctricMeterReading = bacnet.read('201:2 analogValue 300 presentValue')
        print(f'elctricMeterReading {elctricMeterReading} kW')
        stuff['Date'] = stamp
        stuff['MeterReading'] = elctricMeterReading
        data.append(stuff)



async def thirdWorker():#package data to sql and clear data list []
    for _ in range(daysOfData*3):#send to sql 3 times per day
        await asyncio.sleep(28800)#86400 (sec/day) / 3 = 28800, so 3 times per day

        master_data = pd.DataFrame(data)
        master_data.columns = ['Date','Oat','MeterReading']

        engine = create_engine('sqlite:///save_pandas.db', echo=True)
        sqlite_connection = engine.connect()
        sqlite_table = "OutsideTemp_MeterReading"
        master_data.to_sql(sqlite_table, sqlite_connection, if_exists='append')
        sqlite_connection.close()
        print("Data saved to sql!")

        data.clear()
        print("Data List Cleared!")


async def main():
    await asyncio.gather(firstWorker(), secondWorker(), thirdWorker())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

except KeyboardInterrupt:
    pass

finally:
    print("Closing Loop")
    loop.close()

    bacnet.disconnect()
    print("BACnet server shutdown")
        
