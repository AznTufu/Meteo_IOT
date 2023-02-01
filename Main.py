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

day = 0
quart = 0

while(True):
    try:
        print('GET')
        r = urequests.get(url)
        datetimefromreq = r.json()["forecast"][day][quart]["datetime"]
        print(datetimefromreq)
        r.close()
        utime.sleep(1)
    except Exception as e:
        print(e)
