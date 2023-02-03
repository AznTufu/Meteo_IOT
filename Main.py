import network
import urequests
from machine import Pin, ADC
import utime
import ujson

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'iPhone de RORO'
password = 'qsdfghjklm'
wlan.connect(ssid, password)
url = "https://api.meteo-concept.com/api/forecast/daily/periods?token=ed20055cbe431f9fb8760ff0335ab484c0fb8ec0019214f6e39939e4f253568b&insee=92050"
url2 = "http://date.jsontest.com/"

day = 0
quart = 0

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))

firstime = True

while(True):
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    try:
        rr = urequests.get(url2)
        currentdatetime = rr.json()["time"]
        currentdatetime2 = currentdatetime[9:]
        currentdatetime = currentdatetime[:5]
        currentdatetime = currentdatetime.replace(":",".")
        currentdatetime = float(currentdatetime)
        rr.close()
        utime.sleep(1)
    except Exception as ee:
        print(ee)
    if firstime:
        if currentdatetime2 == "PM":
            currentdatetime = currentdatetime + 12.00
        if currentdatetime > 00.59 and currentdatetime < 07.00:
            quart = 0
            firstime = False
        elif currentdatetime > 06.59 and currentdatetime < 13.00:
            quart = 1
            firstime = False
        elif currentdatetime > 12.59 and currentdatetime < 19.00:
            quart = 2
            firstime = False
        elif currentdatetime > 18.59 and currentdatetime < 01.00:
            quart = 3
            firstime = False
        else:
            print('Bug')
    if xValue > 60000:
        if quart == 3:
            quart = 0
        else:
            quart = quart + 1
    elif xValue < 2000:
        if quart == 0:
            quart = 3
        else:
            quart = quart - 1
    print('Quart')
    print(quart)
    if yValue > 60000:
        if day == 13:
            day = 0
        else:
            day = day + 1
    elif yValue < 2000:
        if day == 0:
            day = 13
        else:
            day = day - 1
    print('Day')
    print(day)
    try:
        print('GETAPI')
        r = urequests.get(url)
        temperature = r.json()["forecast"][day][quart]["temp2m"]
        print(temperature)
        r.close()
        utime.sleep(1)
    except Exception as e:
        print(e)
