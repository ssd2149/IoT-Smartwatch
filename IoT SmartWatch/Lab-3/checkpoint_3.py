# -*- coding: cp1252 -*-
import machine
import time
from machine import RTC, Pin, ADC, PWM
from ssd1306a import SSD1306 as ssd
d = ssd()
adc=machine.ADC(0)
d.poweron()
d.init_display()
rtc=RTC()
rtc.datetime((2016,2,3,4,10,7,34,300))
L1 = rtc.datetime()
s = “ “
state1=0
state2=0
rtc.datetime((2016,2,3,4,10,16,40,300))
L2=rtc.datetime()
rtc.datetime((2016,2,3,4,10,7,34,300))
while 1:
	L1 = rtc.datetime()
	s = “ “
	for i in L1:
		for j in L2:
            if L1.index(i)>3 and L1.index(i)<7 and L2.index(j)>3 and L2.index(j)<7:
				if L1.index(i)==4 and L2.index(j)==4 and i==j:
					state1=1
                if L1.index(i)==5 and L2.index(j)==5 and i==j:
					state2=1
		if L1.index(i)>3 and L1.index(i)<7:
			s=s+str(i)+”:”
    if state1==1 and state2==1:
		print(“KNOCK, KNOCK”)
		PWM2= PWM(Pin(2), freq=1000, duty=512)
	print(s)
	d.draw_text(1,1,s,size=1,space=1)
	d.display()
