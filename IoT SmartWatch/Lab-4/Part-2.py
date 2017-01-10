import network
import urequests

sta_if= network.WLAN(network.STA_IF)
sta_if.connect('Columbia University', ' ')
#url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCxYJz0zsGf4H_yOwG83_5WkwdES042IeA"
#payload={"content type":"applications/jsonrequests","content length":"0"}
#r=urequests.post(url, json=payload)
#r.text
#list1=r.text.split("\n")
#lat=list1[2].split(":")
#latitude=lat[1]
#lng=list1[3].split(":")
#longitude=lng[1]

url2="http://api.openweathermap.org/data/2.5/weather?lat=40.8150932&lon=-73.9536048&appid=4f4ccc82856e9ac32a22042471051a0d"
payload={"content type":"applications/jsonrequests","content length":"0"}
r=urequests.post(url2, json=payload)
r.text
list1 = r.text.split(",")
print(list1)
desc=list1[4].split(":")
description=desc[1]
temp=list1[7].split(":")
temperature=temp[2]
hum=list1[8].split(":")
humidity=hum[1]
from ssd1306a import SSD1306 as ssd
d=ssd()
d.poweron()
d.init_display()
d.draw_text(1,1,
d.display()
