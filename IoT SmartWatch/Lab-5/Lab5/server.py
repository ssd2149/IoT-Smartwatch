import network
import time
import ujson
sta_if= network.WLAN(network.STA_IF)
sta_if.connect('Columbia University',' ')
#ngrok http 209.2.232.70:80
import socket
addr= socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s=socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
from ssd1306a import SSD1306 as ssd
d=ssd()
from machine import RTC
rtc=RTC()
rtc.datetime((2016,2,3,4,10,7,34,300))
L=rtc.datetime()
s1=" "
flag= False
d.poweron()
d.init_display()
j=0
html1= """<!DOCTYPE html>
<html>
    <head><title>200 OK</title></head>
    <body>
    <h1>Not found</h1>
    <p>The requested URL was not found</p>
    </body>
</html>
"""
s.settimeout(0.5)
while True:
    L=rtc.datetime()
    print(L)
    try:
        res=s.accept()
    except OSError:
        print("Nothing")
    else:
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
        data1=data.decode("utf-8") #byte to string conversion
        data2=data1.split("=",1) #split it using "=" sign
        data4=data2[1]
        data3=data2[0]
        data5=" "
        print(data3)
        print(data4)
        data5=data4
        data6=data5.replace("+"," ")
        del(req)
        success=" "
        if data3=="DisplayON":
            d.poweron()
            d.init_display()
            d.draw_text(1,1,"HELLO", size=1, space=1)
            d.display()
        if data3=="DisplayTime":
            flag=True
            print("Andar aaya")
        if data3=="message":    #max to max 21 characters
            if len(data6)>21:
                rohit="BIG MESSAGE"
                d.init_display()
                d.draw_text(1,1,rohit,size=1,space=1)
                d.display()
            else:
                d.poweron()
                d.init_display()
                d.draw_text(1,1,data6,size=1,space=1)
                d.display()
        if data3=="DisplayOFF":
            d.poweroff()
        #c1.send(success)
        resp12= "HTTP/1.1 200 OK\r\nContent-Type: application/text\r\nContent-Length: 10\r\n\r\n{'resp111re111234'}"
        c1.send(resp12)
        print("Bhej diya")
        time.sleep(7)
        c1.close()
    if flag==True:
            s1= " "
            L=rtc.datetime()
            print(L)
            for i in L:
                if L.index(i)>3 and L.index(i)<7:
                    s1=s1+str(i)+":"
            d.draw_text(1,1,s1,size=1,space=1)
            d.display()
            #j=j+1
            #j=0
            #success = "HTTP/1.1 200 OK"
            #flag=False
