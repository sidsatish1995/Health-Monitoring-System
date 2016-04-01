import serial
import RPi.GPIO as GPIO      
import os, time

import urllib3
import certifi

http = urllib3.PoolManager(
	cert_reqs='CERT_REQUIRED', 
	ca_certs=certifi.where(),  
)

url = ' https://iotmmsp1941830731trial.hanatrial.ondemand.com:443/com.sap.iotservices.mms/v1/api/http/data/2145786e-364d-4470-a298-bff0f92613da'

headers = urllib3.util.make_headers()

headers['Authorization'] = 'Bearer ' + '9ac910a0549d7751229ad780f5fea264'
headers['Content-Type'] = 'application/json;charset=utf-8'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(36,GPIO.OUT)                
GPIO.output(36,GPIO.HIGH)               

GPIO.setup(38,GPIO.OUT)                 
GPIO.output(38,GPIO.HIGH)               

GPIO.setup(31,GPIO.IN)                
GPIO.setup(33,GPIO.IN)                 
GPIO.setup(35,GPIO.IN)                 
GPIO.setup(37,GPIO.IN)              

while(1):
 port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
 
   
 data = port.read() 
 print data
 time.sleep(4)

 if( (data>30) and (data<120)):
     body='{"mode":"async", "messageType":"f290a1b549f5e0aaef10", "messages":[{"sensor":"Pulse Normal"}]}'
     try:
	r = http.urlopen('POST', url, body=body, headers=headers)
	print(r.status)
	print(r.data)
     except urllib3.exceptions.SSLError as e:
	print e

 else :
  body='{"mode":"async", "messageType":"f290a1b549f5e0aaef10", "messages":[{"sensor":"Pulse Abnormal"}]}'
  try:
	r = http.urlopen('POST', url, body=body, headers=headers)
	print(r.status)
	print(r.data)
  except urllib3.exceptions.SSLError as e:
	print e
	
  GPIO.output(36,GPIO.LOW)
 
  port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
  
  GPIO.output(36,GPIO.HIGH)
 
  port.write('AT'+'\r\n')
  rcv = port.read(10)
  print rcv
  time.sleep(1)
  
  port.write('ATD9663388967;'+'\r\n')
  rcv = port.read(15)
  print rcv

  time.sleep(20)

  D4=GPIO.input(31)
  D3=GPIO.input(33)
  D2=GPIO.input(35)
  D1=GPIO.input(37)
  
  print "S-----T------A------R-----T"
  print D4 
  print D3
  print D2
  print D1
  print "E-----------N-----------D"
  
  port.write('ATH'+'\r\n')
  rcv = port.read(10)
  print rcv
                         
  if( (D4==0) and (D3==0) and (D2==0) and (D1==1) ):

   GPIO.output(38,GPIO.LOW)
                        
   port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
   
   port.write('AT'+'\r\n')
   rcv = port.read(10)
   print rcv
   time.sleep(1)
   
   port.write('ATD9900174208;'+'\r\n')
   rcv = port.read(15)
   print rcv
   time.sleep(15)

   port.write('ATH'+'\r\n')
   rcv = port.read(10)
   print rcv
   
   GPIO.output(36,GPIO.HIGH)
   GPIO.output(38,GPIO.HIGH)
 
 else:
      GPIO.output(36,GPIO.HIGH)
      GPIO.output(38,GPIO.HIGH)
      
 GPIO.output(36,GPIO.HIGH)
 GPIO.output(38,GPIO.HIGH)



