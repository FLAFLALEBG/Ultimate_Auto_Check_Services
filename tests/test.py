import os
import datetime
import ssl
import smtplib

subject = "test"
# Envoie un mail
now = datetime.datetime.now()
cpu_usage = """grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}' """

cpu_temp = "cat /sys/class/thermal/thermal_zone*/temp"
cpu_temp = int(os.popen(cpu_temp).read())
cpu_temp = "{:,}".format(cpu_temp)


message = f"""\
Subject: Oh non le service {subject} à planté !

Bonjour, Je tiens à vous informer que ce jour le {now.day}/{now.month}/{now.year} à {now.hour}:{now.minute} le
service intitulé {subject} à planté.
3 operation affin de le relancer ont toutes échouées

Information système :
CPU Temp = {cpu_temp}°C
CPU Usage = {os.popen(cpu_usage).read()}
From Auto_Check_service Python Bot"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login("nethunter.server@gmail.com", "Gkj93drmi9vaj58rubv3")
    server.sendmail("nethunter.server@gmail.com", "flaviocomblez@gmail.com", message.encode("utf8"))

    print("Successful sending mail")
