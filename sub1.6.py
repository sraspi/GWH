# python
from __future__ import unicode_literals
from paho.mqtt import client as mqtt_client
import sys
import time
import datetime
import numpy as np
import statusmail

T1=True
T6=True
T8=True
T14=True
T18=True
T22=True

#print("Python-version:", sys.version)

#get pw
s = open("/home/pi/PW_mqtt.txt", "r")
pw = s.read()
s.close()


broker = '192.168.178.27'
port = 1883
topic = "GWH-data"
username = 'stefans_mqtt'
password = pw




def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print()
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global T1
        global T6
        global T8
        global T14
        global T18
        global T22
        
        print(f"Received `{msg.payload.decode()}` by `{msg.topic}` topic")
        p=(msg.payload.decode())
        o=p
        print(str(o))
        
        p=p.split()
        Ti=p[5]# Ti ist aber jetzt Aussentemperatur!!!!
        V=p[8]
        t_diff=p[10].replace("`","")
        print(Ti," ", V,"L  ", t_diff,"h")
        u = open("/home/pi/log.txt", "a")
        u.write("\n" + str(o) + "\n")
        u.close()
        
        #send Email at 6h,7h,14h,22h
        th = datetime.datetime.now()  
        t_mail = th.hour  
        
        if t_mail == 1 and T1:
            u = open("/home/pi/log.txt", "w")
            u.write("\n" + "new day, new log" + "\n")
            u.close()
            T1=False
            
        if t_mail == 6 and T6:
            try:
                statusmail.statusmail(Ti,V, t_diff)
            except:
                print("Email-error")
            T6=False
            
        if t_mail == 8 and T8:
            try:
                statusmail.statusmail(Ti,V, t_diff)
            except:
                print("Email-error")
            T8= False
            
        if t_mail == 14 and T14:
            try:
                statusmail.statusmail(Ti,V, t_diff)
            except:
                print("Email-error")
            T14 = False    
            
        if t_mail == 18 and T18:
            try:
                statusmail.statusmail(Ti,V, t_diff)
            except:
                print("Email-error")            
            T18 = False
            
        if t_mail == 22 and T22:
            try:
                statusmail.statusmail(Ti,V, t_diff)
            except:
                print("Email-error")            
            T22 = False    
            
        if t_mail == 0:
            T1=True
            T6=True
            T8=True
            T14=True
            T18=True
            T22=True
            
        
        time.sleep(5)       
        
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()

