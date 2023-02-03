from machine import Pin, SPI, ADC
import max7219
from time import sleep
import network
import urequests
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

spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi,cs,2)

display.brightness(10)

scrolling_message = "Waiting"
length = len(scrolling_message)
column = (length * 8)

display.fill(0)
display.show()
sleep(1)

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    try:
        print('Start')
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
    print("Quart = " + str(quart))
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
    print('Day = ' + str(day))
    try:
        print('GETAPI')
        r = urequests.get(url)
        temperature = r.json()["forecast"][day][quart]["temp2m"]
        print("Température : " + str(temperature)git)
        r.close()
    except Exception as e:
        print(e)
    for x in range(32, -column, -1):     
        display.fill(0)
        display.text(str(temperature) + ".C",x,0,1)
        display.show()
        sleep(0.1)