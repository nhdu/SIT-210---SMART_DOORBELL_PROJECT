import smtplib,ssl  
from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
from datetime import datetime
import RPi.GPIO as GPIO 
import random 
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(17,GPIO.OUT)
GPIO.output(17, False)
camera = PiCamera()  
  
camera.stop_preview()  
def send_an_email():
    camera.start_preview()
    now = datetime.now()
    current = now.strftime("%d%m%Y%H:%M:%S")
    camera.capture('/home/pi/' + current +'.jpg')
    GPIO.output(17, True)
    toaddr = 'duongnhathoang9810@gmail.com'      # To id 
    me = 'duongnhathoang9810@gmail.com'          # your id
    subject = "Visitor"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open(current + ".jpg", "rb").read())  
    encoders.encode_base64(part)
    file_name = current + '.jpg'
    part.add_header('Content-Disposition', 'attachment; filename=.jpg')   # File name and format name
    msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'duongnhathoang9810@gmail.com', password = 'Hoangnhu1234')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()
       GPIO.output(17, False)
    except:  
       print ("Error: unable to send email")    
    #except SMTPException as error:  
          #print ("Error")                # Exception
while True:
	if GPIO.input(4) == GPIO.HIGH:
		 print("Email is being sent!")
		 send_an_email()    