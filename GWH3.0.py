# Bibliotheken laden
import umail
import wlan
import temp
import network
import mail_attach
import utime as time
import socket
import machine
import rp2
from umqtt_simple import MQTTClient
import pub1
from machine import Pin, I2C        #importing relevant modules & classes
import machine
from time import sleep
import utime
import bme280
import bme280_77 #importing BME280 library
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

#Definitions for OLED-Display and fonts
WIDTH =128
HEIGHT= 64
i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
write15 = Write(oled, ubuntu_mono_15)
write20 = Write(oled, ubuntu_mono_20)

Ti=0
Hi=0
Pi=0
Ta=0
Ha=0
Pa=0
V=0  #Wasservolumen [L]

WO1=0
l=0           #len fÃ¼r aw
a=0           #Variable fÃ¼r AD(water)
aw = [0]*10  #array fÃ¼r AD(water)
amax=0       #Max-Wert AD(water)
t_diff = 0   #Differenz zwischen 2* WATER_ON
b=0           #Variable fÃ¼r AD(water)
q=0           #allgemeiner SchleifenzÃ¤hler
I=5           #nur OLED Innen


Zeit = []         #Datum/Zeit
t = []            
water = 0         #Spannung 0.325V Pumpe an
V=0               #"Wasservolumen pro Tag"

start_day = True
t_start = 0       #t_start uer time.ticks() in ms
W=True            #Variable fÃ¼r Water_ON
F=False           #Variable fÃ¼r Water_OFF
R=True

#Variable fÃ¼r set TRC True/False

#Write in cmd found addresses
i2cScan = i2c.scan()
counter = 0
for i in i2cScan:
    print("I2C Address " + str(counter) + "     : "+hex(i).upper())
    counter+=1

print()

pump = Pin(27, Pin.OUT)      #PGPIO 27 als dig_out defininiert
pump.off()                   #GPIO 27 LOW

def bmes(Ti,Hi,Pi,Ta,Ha,Pa):
        #BME280_77_Innen object created
        bme1 = bme280_77.BME280(i2c=i2c)          
        print(bme1.values)
        Ti = bme1.values[0]
        Hi = bme1.values[1]
        Pi = bme1.values[2]
        
        #BME280_77_Innen object created
        bme2 = bme280.BME280(i2c=i2c)          
        print(bme2.values)
        print()
        print()
        Ta = bme2.values[0]
        Ha = bme2.values[1]
        Pa = bme2.values[2]
        return (Ti,Hi,Pi,Ta,Ha,Pa)
        

def Innen(Ti,Hi,Pi,Ta,Ha,Pa,V):
        #Write data to display
        Zeit=str(z[3])+ ":" + str(z[4])
        oled.fill(0)
        write20.text(str(Zeit), 0, 0)
        write20.text(str(V), 60, 0)
        #oled.text("INNEN: " + str(Ti),0,12)
        write20.text("I: ", 0, 20)
        write20.text(str(Ti), 40, 20)
        write20.text("A: ", 0, 40)
        write20.text(str(Ta), 40, 40)
        #oled.text(str(Hi),0,24)
        oled.show() 
        
def Aussen(Ti,Hi,Pi,Ta,Ha,Pa,V):
        oled.fill(0)
        oled.text(Zeit, 0,0)
        oled.text("AUSSEN: " + str(Ta),0,12)
        oled.text(str(Ha),0,24)
        oled.text(str(Pa),0,36)
        oled.show()        
        
while True:    
    print("q: ", q)
    def AD(water):
        #read ADC GPIO26
        sensor = machine.ADC(26)
        conversion_factor = 3.3 / (65535)
        water = sensor.read_u16() * conversion_factor
        
        return water 
    l=len(aw)
    for i in range(l):
        aw[i]=AD(water)
        b=AD(water)+a
        a=b
        time.sleep(0.01)      
    
    asum=sum(aw)
    a=asum/l
      
    if a>0.2 and W:
        print("WATER_ON: ", water)
        print("Status WO1: ", WO1)
        
        if WO1==1:
            t_stop=time.ticks_ms()
            t_diff = round((t_stop-t_start)/1000/60/60,1)
            print("t_diff: ", t_diff)
            
            WO1=0
        if WO1==0:
            t_start=time.ticks_ms()
            WO1=1

        ON_OFF="-------ON-------"
        W=False
        F=True
        V=V+0.28
        V=round(V,2)
        pub1.pub(Zeit, Ti, Hi, Pi, Ta, Ha, Pa, V, ON_OFF,t_diff)
        
       
    if a<0.20 and F:
        print("WATER_OFF")
        ON_OFF="-------OFF-------"
        pub1.pub(Zeit, Ti, Hi, Pi, Ta, Ha, Pa, V,ON_OFF, t_diff)
        W=True
        F=False
        
    print("a: ", a)
    print("V: ", V)
    
    a=0
    
    z=(time.localtime())
    Zeit=str(z[0]) + "." + str(z[1])+ "." + str(z[2])+ " " + str(z[3])+ ":" + str(z[4]) + ":" + str(z[5])
    try:
        Zeit_R = wlan.wifi_on(Zeit,R)
        Zeit=Zeit_R[0]
        R=Zeit_R[1]
        print()
        print()
        
    except:
        print("wifi-error")
    values = bmes(Ti,Hi,Pi,Ta,Ha,Pa)
    Ti=values[0]
    Hi=values[1]
    Pi=values[2]
    Ta=values[3]
    Ha=values[4]
    Pa=values[5]
    
    
    if q>525:#ca.15min
        ON_OFF="---pub_15---"
        pub1.pub(Zeit, Ti, Hi, Pi, Ta, Ha, Pa, V, ON_OFF,t_diff)
        q=0
        
    if I==5:
        #print("OLED_Innen")
        Innen(Ti,Hi,Pi,Ta,Ha,Pa,V)
        #I=I+1
        
    if I>5:
        #print("OLED_Aussen")
        Aussen(Ti,Hi,Pi,Ta,Ha,Pa,V)
        I=I+1
        if I>11:
            I=0
    q=q+1                  
    if start_day == True:
        day0=str(str(z[2]))
        start_day =False  
        
    day=str(z[2])
    
    if day0 != day:
        V=0
        R=True

    




