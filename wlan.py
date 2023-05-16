def wifi_on(Zeit,R):
    # Bibliotheken laden
    import machine
    import network
    import rp2
    import sys
    import utime as time
    import usocket as socket
    import ustruct as struct
    import _thread
    import utime
    

    # WLAN-Konfiguration
    
    rp2.country('DE')
    # Winterzeit / Sommerzeit
    GMT_OFFSET = 3600 * 2 # 3600 = 1 h (Winterzeit)
    #GMT_OFFSET = 3600 * 2 # 3600 = 1 h (Sommerzeit)
    # Status-LED
    led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
    # NTP-Host
    NTP_HOST = 'pool.ntp.org'


    # Funktion: WLAN-Verbindung
    def wlanConnect():
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            print('wifi connected(1)/ WLAN-Status:', wlan.status())
            led_onboard.on()
            
        else:
            print('try to connect Fritzbox(1)')
            wlanSSID = 'FRITZBOX Keller'
            wlanPW = 'pw'
            wlan.active(True)
            wlan.connect(wlanSSID, wlanPW)
            for i in range(20):
                if wlan.status() == 3:
                    break
                
                led_onboard.toggle()
                print('.')
                time.sleep(1)
            led_onboard.off()
            
                
        
        if wlan.isconnected():
            #print('Try to connect Fritzbox(2) / Status:', wlan.status())
            led_onboard.on()    
        else:
            print("Fritzbox-connection failed")
            print('Try to connect Iphone')
            wlanSSID = 'Stefans Iphone'
            wlanPW = 'StJ19hot'
            wlan.active(True)
            wlan.connect(wlanSSID, wlanPW)
            for i in range(20):
                if wlan.status() == 3:
                    break
                
                led_onboard.toggle()
                print('.')
                time.sleep(1)
        
            led_onboard.off()
            print('Status:', wlan.status())
            
            if wlan.isconnected():
                print('wifi-connected(3) / Status:', wlan.status())
                led_onboard.on()

    # Funktion: Zeit per NTP holen
    def getTimeNTP():
        NTP_DELTA = 2208988800
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        ntp_time = struct.unpack("!I", msg[40:44])[0]
        return time.gmtime(ntp_time - NTP_DELTA + GMT_OFFSET)

    # Funktion: RTC-Zeit setzen
    def setTimeRTC():
        # NTP-Zeit holen
        tm = getTimeNTP()
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
        
        
    # WLAN-Verbindung herstellen

    wlanConnect()
    time.sleep(1)
    if R:
        print("RTC set!")
        setTimeRTC()
        a = machine.RTC().datetime()
        Zeit = (str(a[0]) + "." + str(a[1]) + "." + str(a[2]) + " " + str(a[4]) + ":" + str(a[5]) + ":" + str(a[6]))
        R=False
        
    return (Zeit, R)
            




 