import network
import ujson
import machine
sta_if = network.WLAN(network.STA_IF)
sta_if.connect('Columbia University', ' ')
import usocket
import ussl
import ustruct
import time
addr= usocket.getaddrinfo('0.0.0.0', 80)[0][-1] # what does [0] signify
s1=usocket.socket()
s1.bind(addr)
s1.listen(1)
print('listening on', addr)

t=" "
w=" "

from machine import RTC,ADC,Pin,SPI
from ssd1306a import SSD1306 as ssd

global cs, vcc, grnd, spi
# Register constants for the ADXL345 accelerometer
POWER_CTL = const(0x2D)
DATA_FORMAT = const(0x31)
DATAX0 = const(0x32)
DATAX1 = const(0x33)
DATAY0 = const(0x34)
DATAY1 = const(0x35)
DATAZ0 = const(0x36)
DATAZ1 = const(0x37)

# Write to the DATA_FORMAT register to set to 4g.
# Write to POWER_CTL register to begin measurements
def setup():
    writeA(DATA_FORMAT, 0x01)
    writeA(POWER_CTL, 0x08)
# Write command/value to specified register
def writeA(register, value):
    global cs, vcc, grnd, spi
    # Pack register and value into byte format
    write_val = ustruct.pack('B',value)
    write_reg_val = ustruct.pack('B',register)
    # Pull line low and write to accelerometer
    cs.value(0)
    spi.write(write_reg_val)
    spi.write(write_val)
    cs.value(1)
# Read value from a specified register
def readA():
    global cs, vcc, grnd, spi
    # Set the R/W bit high to specify "read" mode
    reg = DATAX0
    reg = 0x80 | reg
    # Set the MB bit high to specify that we want to
    # do multi byte reads.
    reg = reg | 0x40
    # Pack R/W bit + MB bit + register value into byte format
    write_reg_val = ustruct.pack('B',reg)
    # Setup buffers for receiving data from the accelerometer.
    x1 = bytearray(1)
    x2 = bytearray(1)
    y1 = bytearray(1)
    y2 = bytearray(1)
    z1 = bytearray(1)
    z2 = bytearray(1)
    # Read from all 6 accelerometer data registers, one address at a time
    
    cs.value(0)
    spi.write(write_reg_val)
    spi.readinto(x1)
    spi.readinto(x2)
    spi.readinto(y1)
    spi.readinto(y2)
    spi.readinto(z1)
    spi.readinto(z2)
    cs.value(1)
    # Reconstruct the X, Y, Z axis readings from the received data.
    x = (ustruct.unpack('b',x2)[0]<<8) | ustruct.unpack('b',x1)[0]
    y = (ustruct.unpack('b',y2)[0]<<8) | ustruct.unpack('b',y1)[0]
    z = (ustruct.unpack('b',z2)[0]<<8) | ustruct.unpack('b',z1)[0]
    return (x,y,z)

rtc=RTC()
rtc.datetime((2016,2,3,4,10,7,34,300))
L=rtc.datetime()
adc=ADC(0)
flag= False

pinb = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
pinc = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
s1.settimeout(0.5)
d=ssd()
d.poweron()

# Setup SPI: cs = Pin13, clk = Pin5, mosi = Pin2, miso = Pin16
cs=Pin(13, Pin.OUT)
vcc = Pin(12, Pin.OUT)
grnd = Pin(14 , Pin.OUT)
vcc.value(1)
grnd.value(0)
spi = SPI(-1, baudrate=500000, polarity=1, phase=1, sck=Pin(0), mosi=Pin(2), miso=Pin(16))
cs.value(0)
cs.value(1)
# Initialize accelerometer
setup()
# Sample axis registers at 2 Hz

#Button
alarmflag=0
press=0
alarmactive=0
eq=0

   

while True:
    L=rtc.datetime()
    d.contrast(1000*(adc.read()))
    #print(L)
    curr_pinc=pinc.value()
    if curr_pinc==0:
        press+=1
    else:
        press=0
    if press==5:
        alarmflag=1-alarmflag
        if alarmflag==1:
            alarmlist=list(L)
            alarmlist[5]+=1

        if alarmflag==0:
            alarmactive=0
            d.init_display()

    print(alarmflag)
    if alarmflag==0:
        if pinb.value()==0:
            list2=list(L)
            list2[4]+=1
            rtc.datetime(list2)

        if pinc.value()==0:
            list2=list(L)
            list2[5]+=1
            rtc.datetime(list2)
            
    if alarmflag==1 and alarmactive==0:
        if pinb.value()==0:
            alarmlist[4]+=1
            
        if pinc.value()==0:
            alarmlist[5]+=1


        litest=list(L)

        if litest==alarmlist:
            alarmactive=1
            
        st= " "
        for i in alarmlist:
            if alarmlist.index(i)>3 and alarmlist.index(i)<7:
                st=st+str(i)+":"
        d.draw_text(1,1,st,size=1,space=1)
        d.display()

    if alarmactive==1:
        d.draw_text(1,1,"Alarm",size=1,space=1)
        d.display()
    
    if flag==True and alarmflag==0:
        st= " "
        L=rtc.datetime()
        for i in L:
            if L.index(i)>3 and L.index(i)<7:
                st=st+str(i)+":"
        d.draw_text(1,1,st,size=1,space=1)
        d.display()
        
    x, y, z = readA()
    print("x:",x,"y:",y,"z:",z)

    url="http://ec2-35-162-91-20.us-west-2.compute.amazonaws.com/post"
    _, _, host, path = url.split('/', 3)
    addr = usocket.getaddrinfo(host, 80)[0][-1]
    s21 = usocket.socket()
    s21.connect(addr) 
    strjson='{"xcoordinate": '+str(x)+', "ycoordinate": '+str(y)+', "zcoordinate": '+str(z)+'}'    
    post='POST /%s HTTP/1.1\r\nContent-length: %d\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n%s' % (path,len(strjson),host,strjson)
    print(post)
    s21.send(bytes(post,'utf-8'))
    #data2=s2.read(550)
    time.sleep_ms(900)

    
    try:
        res=s1.accept()
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
        del data
        data2=data1.split("=",1) #split it using "=" sign
        del data1
        data3=data2[0]
        data4=data2[1]
        del data2
        data5=" "
        print(data3)
        print(data4)
        data5=data4
        data6=data5.replace("+"," ")
        del req
        del res
        d.init_display()
        if data3=="DisplayON":
            d.draw_text(1,1,"HELLO", size=1, space=1)
            d.display()
            flag=False
            #del d
        if data3=="DisplayTime":
            flag=True
            print("Andar aaya")
        if data3=="message":    #max to max 21 characters
            flag=False
            if len(data6)>21:
                d.draw_text(1,1,"BIG MESSAGE",size=1,space=1)
                d.display()
                #del d
                del data6
            else:
                d.draw_text(1,1,data6,size=1,space=1)
                d.display()
        if data3=="DisplayWEATHER":
            url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD2VG9MTweWjOxqzwhlEx2R8aX-UimxEHI"
            _, _, host, path = url.split('/', 3)
            addr = usocket.getaddrinfo(host, 443)[0][-1]
            s2 = usocket.socket()
            s2.connect(addr)
            s2 = ussl.wrap_socket(s2)
            s2.write('POST /%s HTTP/1.1\r\nContent-length:0\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n' % (path, host))
            data=s2.read(550)
            x=str(data)
            #del data
            #del addr
            #del url
            #del host
            latl=x.find("lat")
            latst=x[latl+6:latl+11]
            longl=x.find("lng")
            longst=x[longl+7:longl+11]
            #del x
            del s2
            #del lat1
            #del long1
            #del host
            url="http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=9579f82a537347b08c7e448409a8731f" % (latst,longst)
            _, _, host, path = url.split('/', 3)
            addr = usocket.getaddrinfo(host,80)[0][-1]
            s2=usocket.socket()
            s2.connect(addr)
            s2.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
            dat=s2.recv(550)
            del s2
            del url
            x=str(dat)
            del dat
            mainl=x.find("main")
            desc=x[mainl+6:mainl+13].upper()
            templ=x.find("temp")
            temp=x[templ+6:templ+12].upper()
            #del x
            #del main1
            #del temp1
            d.draw_text(1,1,desc.upper(),size=1,space=1)
            d.draw_text(1,10,str(temp),size=1,space=1)
            d.display()
            w=str(temp)
            flag=False
            #del d
        if data3=="showWEATHER":
            d.init_display()
            d.draw_text(1,1,w,size=1,space=1)
            d.display()
            flag=False
            
        if data3=="tweet":
            url = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=HT5XM8PWE824B01C&status="+data6
            tweetmsg= data6
            _, _, host, path = url.split('/', 3)
            addr = usocket.getaddrinfo(host,80)[0][-1]
            s3 = usocket.socket()
            s3.connect(addr)
            #s3.write('POST /%s HTTP/1.1\r\nContent-length:0\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n' % (path, host))
            s3.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
            data=s3.read(550)
            flag=False
            d.init_display()
            d.draw_text(1,1,"TWWEETED:"+data6,size=1,space=1)
            d.display()
            t=data6
            del s3
        if data3=="showPOST":
            d.init_display()
            d.draw_text(1,1,t,size=1,space=1)
            d.display()
            flag=False
            
        if data3=="DisplayOFF":
            d.poweroff()
            #del d
            resp12= "HTTP/1.1 200 OK\r\nContent-Type: application/text\r\nContent-Length: 10\r\n\r\n{'resp111re111234'}"
            c1.send(resp12)
            print("Bhej diya")
            time.sleep(7)
            c1.close()
            flag=False
            del resp12
            del c1
        
            #del d
            #del st
            #j=j+1
            #j=0
            #success = "HTTP/1.1 200 OK"
            #flag=False




    #accelerometer
    #s3 = usocket.socket()
    #addr = usocket.getaddrinfo(host, 443)[0][-1]
    #data={"x-coordinate":"1", "y-coordinate":"2", "z-coordinate":"1"}
    #url= "https://ec2-35-161-96-40.us-west-2.compute.amazonaws.com/"
    #r=urequests.post(url, json=data)


 
