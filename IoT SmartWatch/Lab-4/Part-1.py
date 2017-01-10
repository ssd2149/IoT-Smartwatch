import network
#import socket
#import json
import machine, ussl
import urequests
from ssd1306a as SSD1306 as ssd
d=ssd()
d.poweron()
d.init_display()
s=socket.socket()
sta_if= network.WLAN(network.STA_IF)
#ap_if= network.WLAN(network.AP_if)
#ap_if.ifconfig()
sta_if.connect('Columbia University', ' ')
#sta_if.ifconfig()
url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCxYJz0zsGf4H_yOwG83_5WkwdES042IeA"
#_,_,host,path=url.split('/',3)
payload={"content type":"applications/jsonrequests","content length":"0"}
r=urequests.post(url, json=payload)
r.text
#h1,h2=url.split('/',1)
#addr=socket.getaddrinfo(h1,443)[0][-1]
#s.connect(addr)
#ss=ussl.wrap_socket(s) #error here
#ss.write(bytes('POST /%s HTTP/1.1\r\nh1: %s\r\n\r\n Content-Encoding: identity, Content-Length: 72, Content-Type: application/jsonrequest'% (h2,h1), 'utf8'))
list1=r.text.split("\n")
lat=list1[2].split(":")
latitude=lat[1]
lng=list1[3].split(":")
longitude=lng[1]
str1="Latitude="+latitude+"Longitude"+longitude
print(str1)
d.draw_text(1,1,str1,size=1,space=1)
d.display()
