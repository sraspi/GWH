def pub(Zeit, Ti, Hi, Pi, Ta, Ha, Pa,V,ON_OFF,t_diff):  
    import machine
    import network
    import rp2
    import utime as time
    from umqtt_simple import MQTTClient
        
    # MQTT-Konfiguration
    mqttBroker = '192.168.178.27'
    mqttClient = 'pico'
    mqttUser = 'stefans_mqtt'
    mqttPW = 'pw'
    mqttTopic = "GWH-data"

    
    # Funktion: Verbindung zum MQTT-Server herstellen
    def mqttConnect():
        if mqttUser != '' and mqttPW != '':
            print("MQTT-Verbindung herstellen: %s mit %s als %s" % (mqttClient, mqttBroker, mqttUser))
            client = MQTTClient(mqttClient, mqttBroker, user=mqttUser, password=mqttPW)
        else:
            print("MQTT-Verbindung herstellen: %s mit %s" % (mqttClient, mqttBroker))
            client = MQTTClient(mqttClient, mqttBroker)
        client.connect()
        print()
        print('MQTT-Verbindung hergestellt')
        print()
        return client
    myValue = (str(Zeit) + " " + str(Ti) + " " + str(Hi) + " " + str(Pi) + " " + str(Ta) + " " + str(Ha) + " " + str(Pa) + " " + str(V) + " "+ str(ON_OFF) + " "+ str(t_diff))
    

    try:
        client = mqttConnect()
        client.publish(mqttTopic, myValue)
        print("An Topic %s gesendet: %s" %  (mqttTopic, myValue))
        print()
        client.disconnect()
        print('MQTT-Verbindung beendet')
        print()
    except OSError:
        print()
        print('Fehler: Keine MQTT-Verbindung')
        print()

