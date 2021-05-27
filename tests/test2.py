import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import psutil
import subprocess

sender_email = "nethunter.server@gmail.com"
receiver_email = "flaviocomblez@gmail.com"
email_password = "Gkj93drmi9vaj58rubv3"
smtp_server = "smtp.gmail.com"
email_smtp_port = 465


def send_mail(subject, verbose):
    global sender_email, email_password, smtp_server, email_smtp_port, receiver_email

    # Envoie un mail
    now = time.ctime()

    cpu_usage = str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()), 2))

    ram_used = psutil.virtual_memory()[2]

    cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]

    disk_usage = psutil.disk_usage(os.sep).percent

    # Create the plain-text and HTML version of your message

    print(psutil.cpu_percent(percpu=False))
    print(cpu_usage)

    text = f"""\
Subject: The {subject} service is down
    
    
    
    
    
    
    

                                            
Cpu Temp : {cpu_temp.current}°C                                                                                   
Date : {now}
Service name : {subject}  
Ram Used = {ram_used}%     
Disk Used = {disk_usage}%     
Cpu Usage : {cpu_usage}%          

.................................

Send From https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services
"""

    # Create secure connection with server and send email
    print(text)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, email_smtp_port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, text.encode("utf-8"))

        print("Successful sending mail")


send_mail("plexmediaserver", True)
