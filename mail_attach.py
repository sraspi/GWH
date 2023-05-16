def send_csv(Zeit, Ta):
    try:
        import umail
        import utime as time

        counter = 0
        content = 'there is no content' #  if reading ramdisk fails this keeps things alive

        smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) 

        time.sleep(1)

        while counter < 5:
            counter +=1
            
            try:
                #get PW
                s = open("/data/PW.txt", "r")
                pw = s.read()
                s.close()
                test1 = smtp.login('sraspi21@gmail.com', pw)
                result = str(test1).find('Accepted')
                

                if (result != -1): # meaning: if result!=-1>>then False
                    print('gmail-login OK')
                    counter = 0
                    
                    smtp.to('stefan.taubert.apweiler@gmail.com')
                    time.sleep(1)
                    smtp.write("From: GWH-pico>\n")
                    smtp.write("To: stefan <stefan.taubert.apweiler@gmail.com>\n")
                    smtp.write('Subject: GWH-data \n')
                    smtp.write('MIME-Version: 1.0\n')
                    smtp.write('Content-type: multipart/mixed; boundary=12345678900987654321\n')

                    smtp.write('--12345678900987654321\n')
                    smtp.write('Content-Type: text/plain; charset=utf-8\n')
                    smtp.write('\n' + "Temp-Aussen: " + str(Ta) +'\n')
                    smtp.write('\n' + str(Zeit) + '\n')
                    smtp.write('--12345678900987654321\n')


                    csv_file = 'log.txt\n'

                    content_type = 'Content-Type: text/csv; name=' + csv_file
                    content_disposition = 'Content-Disposition: attachment; filename=' + csv_file 
                    smtp.write(content_type)
                    smtp.write(content_disposition)

                    try:
                        f = open("/data/log.txt",  "a" )
                        content = f.read()#infile.read()
                        
                        
                        
                    except OSError:
                        print('Cannot read datalog.txt')
                        pass

                    smtp.write(content) #  my content has a \n at the end
                    smtp.write('...\n') #  suppose to be important??
                    smtp.send() # does the proper ending
                    smtp.quit()
                    f.close()
                    f = open("/data/log.txt",  "a" )
                    f.write("\n" +  str(Zeit) + " : Email sent" + "\n")
                    f.close()
                    print('Email with datalog.txt has been sent')
                    break
                
            except Exception:
                pass
            if (counter == 5):
                print("Email-error")
                f = open("/data/log.txt",  "a" )
                f.write("\n" +  str(Zeit) + ": Email error, counter =5  " + "\n")
                f.close()
                
    except:
        print("mail-error")

                       
   
  