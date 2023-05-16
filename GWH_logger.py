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

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method
Ti=0
Hi=0
Pi=0
Ta=0
Ha=0
Pa=0
V=0

l=0
a=0
aw = [0]*100
amax=0
b=0
q=0
I=0
A=0

Zeit = []
Z = []
t = []
IP = []
water = 0


start_day = True
t_start = 0
W=True
F=False
R=True

T6=True
T7=True
T14=True
T20=True
T22=True
T11=True
T12=True

#Write in cmd found addresses
i2cScan = i2c.scan()
counter = 0
for i in i2cScan:
    print("I2C Address " + str(counter) + "     : "+hex(i).upper())
    counter+=1

print()
print()

#Definitions for OLED-Display
WIDTH = 128
HIGHT = 64
oled = SSD1306_I2C(WIDTH, HIGHT, i2c)


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
        Zeit=str(z[0]) + "." + str(z[1])+ "." + str(z[2])+ " " + str(z[3])+ ":" + str(z[4])
        oled.fill(0)
        oled.text(Zeit, 0,0)
        oled.text("INNEN: " + str(Ti),0,12)
        oled.text(str(Hi),0,24)
        oled.text(str(Pi),0,36)
        oled.text('Wasser[L]: ' + str(V),0,48)
        oled.show() 
        
def Aussen(Ti,Hi,Pi,Ta,Ha,Pa,V):
        oled.fill(0)
        oled.text(Zeit, 0,0)
        oled.text("AUSSEN: " + str(Ta),0,12)
        oled.text(str(Ha),0,24)
        oled.text(str(Pa),0,36)
        oled.show()        
        
while True:    
    t_start=time.ticks_ms()
    def AD(water):
        #read ADC GPIO26
        sensor = machine.ADC(26)
        conversion_factor = 3.3 / (65535)
        water = sensor.read_u16() * conversion_factor
        
        return water 
    
    for i in range(100):
        aw[i]=AD(water)
        b=AD(water)+a
        a=b
        time.sleep(0.01)
        
    l=len(aw)
    asum=sum(aw)
    amittel=asum/l
    amax=max(aw)
    print()
    print()
    print("asum: ", asum, "  amax: ", amax, " amittel: ", amittel)
    print()
    
    w = open("/data/log.txt", "a")
    w.write("\n" + str(Zeit) +"  asum: "+ str(asum) +"  amax: " + str(amax) +  "  amittel: " + str(amittel) + "\n")
    w.close()
    a=0
    #get IP-adress:
    try:
        addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
        addr = addr_info[0][-1]
        IP=(addr[0])
    except:
        print("IP-error")
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
        pub1.pub(Zeit, Ti, Hi, Pi, Ta, Ha, Pa, V)
        print("write logfile")
        d = open("/data/log.txt",  "a" )
        d.write("\n" + str(Zeit) + " " + str(Ti) + " " + str(Hi) + " " + str(Pi)+ " "  + str(Ta)+ " "  + str(Ha)+ " "  + str(Pa) + " " + str(V)+ " "  + str(water) + "\n")
        d.close()
        q=0
        
    if I<5:
        #print("OLED_Innen")
        Innen(Ti,Hi,Pi,Ta,Ha,Pa,V)
        I=I+1
        
    if I>=5:
        #print("OLED_Aussen")
        Aussen(Ti,Hi,Pi,Ta,Ha,Pa,V)
        I=I+1
        if I>11:
            I=0
    q=q+1                  
    if start_day == True:
        day0=str(str(z[2]))
        start_day =False
    h=(z[3])
    
    if h ==6 and T6:
        mail_attach.send_csv(Zeit, Ta)
        T6=False
    if h ==7 and T7:
        mail_attach.send_csv(Zeit, Ta)
        T7=False
    if h ==14 and T14:
        mail_attach.send_csv(Zeit, Ta)
        T14=False
    if h ==22 and T22:
        mail_attach.send_csv(Zeit, Ta)
        T22=False
    if h ==11 and T11:
        mail_attach.send_csv(Zeit, Ta)
        T11=False
    if h ==12 and T12:
        mail_attach.send_csv(Zeit, Ta)
        T12=False    
        
    day=str(z[2])
    t_stop=time.ticks_ms()
    t_diff=t_stop-t_start
    print("t_diff: ", t_diff)
    if day0 != day:
        mail_attach.send_csv(Zeit, Ta)
        f = open("/data/log.txt",  "w" )
        f.write("\n" +  str(Zeit) + ":  new day, new log.txt" + "\n")
        f.close()
        day0=day
        
        R=True

    




