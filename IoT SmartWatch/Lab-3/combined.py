import network
#import urequests
import ujson
sta_if= network.WLAN(network.STA_IF)
sta_if.connect('Columbia University',' ')
import socket
addr= socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s=socket.socket()
s.bind(addr)
s.listen(5)
print('listening on', addr)
from ssd1306a import SSD1306 as ssd
d=ssd()
from machine import RTC
rtc=RTC()
rtc.datetime((2016,2,3,4,10,7,34,300))
L=rtc.datetime()
s1=" "
while True:
    L=rtc.datetime()
    res=s.accept()
    c1=res[0]
    addr=res[1]
    print('client connected from', addr)
    print('client socket', c1)
    print('request')
    req=c1.recv(4096)
    print(req)
    html=req
    html=html.split(b'\r\n\r\n') #converts it into list
    #_[-1]
    data=html[-1] #gets unsplited data
    data1=data.decode("utf-8")
    data2=data1.split("=",1)
    data3=data2[1]
    if data3=="display on":
        d.poweron()
        d.init_display()
    if data3=="display time":
        while True:
            L=rtc.datetime()
            for i in L:
                if L.index(i)>3 and L.index(i)<7:
                    s1=s1+str(i)+":"
            d.draw_text(1,1,s1,size=1,space=1)
            d.display()
    if data3=="IoT":        
        d.draw_text(1,1,s1,size=1,space=1)
        d.display()
    if data3=="display off":
        d.poweroff()        
    
