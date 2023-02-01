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

while(True):
    try:
        print('GET')
        rr = urequests.get(url2)
        currentdatetime = rr.json()["time"]
        currentdatetime2 = currentdatetime[9:]
        currentdatetime = currentdatetime[:5]
        currentdatetime = currentdatetime.replace(":",".")
        currentdatetime = float(currentdatetime)
        print(currentdatetime)
        print(currentdatetime2)
        rr.close()
        utime.sleep(1)
    except Exception as ee:
        print(ee)
    if currentdatetime2 == "PM":
        currentdatetime = currentdatetime + 12.00
    if currentdatetime > 00.59 and currentdatetime < 07.00:
        print("Quart1")
        quart = 0
    elif currentdatetime > 06.59 and currentdatetime < 13.00:
        print("Quart2")
        quart = 1
    elif currentdatetime > 12.59 and currentdatetime < 19.00:
        print("Quart3")
        quart = 2
    elif currentdatetime > 18.59 and currentdatetime < 01.00:
        print('Quart4')
        quart = 3
    else:
        print('Bug')
    try:
        print('GETAPI')
        r = urequests.get(url)
        temperature = r.json()["forecast"][day][quart]["temp2m"]
        print(temperature)
        r.close()
        utime.sleep(1)
    except Exception as e:
        print(e)
