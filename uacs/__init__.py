#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------* TO DO *-------------- #

# TODO : ajouter deepl API pour traduire les massages.
# TODO : possibilitée de retirer les services de la liste
# TODO : Optimiser le code :
#  - avec des objets pour le init
#  - optimiser les imports
# TODO : integration dans pip

# --------------* IMPORT *-------------- #

import os
import pickle
import smtplib
import ssl
import sys
import threading
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

# --------------* VARIABLES *-------------- #

service_check = []
services_restored = []
email_restored = []
file_ini_service = "/etc/uacs/service_monitored.conf"
file_ini_email = "/etc/uacs/email.conf"
service_name = "ultimate_auto_check_service"
path_config = "/etc/uacs/"
sender_email, email_password, receiver_email, smtp_server = "", "", "", ""
email_smtp_port = 0
running = True
number_restart = 3

# Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# --------------* Functions *-------------- #
def main():
    pass


def enablePrint():
    sys.stdout = sys.__stdout__


def restore(verbose):
    restore_email(verbose)
    restore_service(verbose)


def restore_service(verbose):  # Restauration des services depuis un fichier (file_ini)
    if verbose:
        enablePrint()

    global service_check, services_restored
    print("Service restoration")
    print(f"Searching for the file : {file_ini_service}")
    if os.path.isfile(file_ini_service):
        print("File found !")

        print("Opening the file ...")
        backup_file = open(file_ini_service, "rb")

        print(f"Reading variables in the file : " + file_ini_service)
        try:
            services_restored = pickle.load(backup_file)

        except:
            print("Error file empty")

        backup_file.close()

        print("Adding the backup to the buffer")
        service_check.append(services_restored)

        print(f"The {services_restored} services have been added")

    else:
        # The file does not exist
        print(f"File {file_ini_service} not found")
        os.system(f"sudo mkdir -p /etc/uacs/ && sudo touch {file_ini_service}")
        print(f"Created file {file_ini_service}")


# noinspection PyUnusedLocal
def restore_email(verbose):  # Restauration de l'email / mot de passe depuis le fichier
    if verbose:
        enablePrint()

    global sender_email, email_password, receiver_email, smtp_server, email_smtp_port, email_restored

    print("Restauration of the email address and its password")
    print(f"Searching for the file : {file_ini_email}")
    if os.path.isfile(file_ini_email):
        print("File found !")

        print("Opening the file ...")
        backup_file = open(file_ini_email, "rb")

        print(f"Reading variables in the file : " + file_ini_email)

        try:
            email_restored = pickle.load(backup_file)

            backup_file.close()

            sender_email = email_restored[0]
            email_password = email_restored[1]
            receiver_email = email_restored[2]
            smtp_server = email_restored[3]
            email_smtp_port = email_restored[4]

        except:
            print("Error file empty")

        print(f"The email adresse have been restored")

    else:
        # The file does not exist
        print(f"File {file_ini_email} not found")
        os.system(f"sudo mkdir -p /etc/uacs/ && sudo touch {file_ini_email}")
        print(f"Created file {file_ini_email}")


def append(append_service, verbose):  # Ajoute un service a la liste et l'ajoute également au fichier (file_ini)
    if verbose:
        enablePrint()

    # Verification de l'existence du service et l'enregistre
    print(f"Verification of the existence of the service {append_service} and registration ...")
    print(f""""systemctl list-unit-files | grep "^{append_service}" """)
    exist_service = os.system(f""""systemctl list-unit-files | grep "^{append_service}" """)
    if str(exist_service).find(".service"):
        print("Service exist \nSaving ...")

        print(f"Opening the file {file_ini_service}")
        backup_file = open(file_ini_service, "wb")

        print(f"Appending the service {append_service}")
        pickle.dump(append_service, backup_file)
        backup_file.close()
        service_check.append(append_service)
        print("Saved !")
    else:
        print("Service don't exist")
    print("The following services are monitored" + str(service_check))


def check_service(verbose):
    if verbose:
        enablePrint()

    # Surveille les services 1 par 1
    for i in range(len(service_check)):
        print(f"systemctl status {service_check[i]} | grep active")
        active = os.system(f"systemctl status {service_check[i]} | grep active")
        if str(active).find("inactive"):
            print(f"Service is inactive \nLaunch of the restart of the services {service_check[i]}")
            service_down(service_check[i], verbose)

        elif str(running).find("active"):
            print("Service is active")


def service_down(service, verbose):
    global active, number_restart
    if verbose:
        enablePrint()

    # Essaye de relancer 3x le service
    # et envoie un mail si il ne redémarre pas
    for i in range(number_restart):
        print(f"Relaunching n°{i}/{number_restart}")
        active = os.system(f"systemctl status {service}")
        if str(active).find("inactive"):
            os.system(f"systemctl restart {service}")
            continue
        elif str(active).find("running"):
            print(f"Successful restarting service {service}")
        else:
            print("Error, we do not know the status of this service")
            continue

    if str(active).find("inactive"):  # send mail
        print(f"Failed to restart the {service} service request to send the email")
        send_mail(service, verbose)
    else:
        pass


def send_mail(subject, verbose):
    if verbose:
        enablePrint()
    global sender_email, email_password, smtp_server, email_smtp_port, receiver_email

    # Envoie un mail
    now = time.ctime()

    cpu_usage = str(round(float(os.popen(
        '''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()), 2))

    ram_used = psutil.virtual_memory()[2]

    cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]

    disk_usage = psutil.disk_usage(os.sep).percent

    uuid = uuid.uuid1()

    print(psutil.cpu_percent(percpu=False))
    print(cpu_usage)

    text = f"""\
Subject: The {subject} service is down









Cpu Temp : {cpu_temp.current}°C                                                                                   
Date : {now}
Service name : {subject}  
Ram Used : {ram_used}%     
Disk Used : {disk_usage}%     
Cpu Usage : {cpu_usage}%  
 
.................................
id : {uuid}
.................................

Send From https://github.com/FLAFLALEBG/Ultimate_Auto_Check_Services
"""

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, email_smtp_port, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, text.encode("utf-8"))

            print("Successful sending mail")

    except:
        print(f"Mail with id {uuid} error")
        print(f"Sending error please check the sender's email ({sender_email}) and password or the receiver's "
              f"({receiver_email})")


def daemon():
    print("Starting...")
    restore(True)
    print("Started !")
    while running:
        time.sleep(30)
        print("New Verification")
        check_service(True)

    print("Stopped")


def run_daemon():
    threading.Thread(target=daemon()).start()


def init():
    print(f"{WARNING}This will guide you through the setup of the Ultimate Automatic Check Services.{ENDC}\n"
          f"{OKGREEN}If you wish to quit at any point, press Ctrl+C.{ENDC}")

    def config_email():
        print(f"{OKBLUE}Config email{ENDC}...")

        receiver_email = input(f"Enter your email address to which you will {BOLD}receive alerts{ENDC} : ")
        sender_email = input(f"Enter your sender address to which we will {BOLD}send alerts{ENDC} : ")
        email_password = input(f"Enter the {BOLD}password {ENDC}of the {BOLD}sender{ENDC}'s email address : ")
        smtp_server = input("List of the most famous SMTP server https://domar.com/smtp_pop3_server\n"
                            "Enter the address of your smtp server : ")
        try:
            email_smtp_port = int(
                input("Enter now the port of your SMTP server of preference the secure one (SSL)\nIt is more "
                      "commonly the port '465' : "))
        except:
            email_smtp_port = int(input(f"{FAIL}Please enter a numerical value{ENDC} : "))

        # Enregistrement des variables dans le fichier
        variables = [sender_email, email_password, receiver_email, smtp_server, email_smtp_port]
        backup_file = open(file_ini_email, "wb")
        pickle.dump(variables, backup_file)
        print("Saved !")
        time.sleep(1)

        def test_email():
            answer = input("Do you want to perform an email test ? [y/n]: ")

            if answer == "yes" or "y" or "Y":
                # Send mail
                try:
                    with smtplib.SMTP_SSL(smtp_server, email_smtp_port, context=ssl.create_default_context()) as server:
                        server.login(sender_email, email_password)

                        server.sendmail(sender_email, receiver_email,
                                        "Subject: You are done\n\nWell done you succeeded "
                                        "you will now receive alerts from your services on "
                                        "this email.")

                        print("Successful sending mail")

                        def checkup():
                            answer = input("Did you receive the email correctly ? [y/n]: ")
                            if answer == "yes" or "y" or "Y":
                                pass

                            elif answer == "no" or "n" or "N":
                                answer = input(
                                    f"Do you want to retry the test email [{OKCYAN}1{ENDC}] or do you want to "
                                    f"edit your email [{OKCYAN}2{ENDC}] ?: ")
                                if answer == "1":
                                    test_email()
                                elif answer == "2":
                                    init()
                                else:
                                    print("Error, please enter a correct value")

                            else:
                                print("Error, please enter a correct value")
                                checkup()

                        checkup()

                except:
                    print(
                        "Sending error please check the sender's email and password or the receiver's\nRelaunch of the "
                        "script"
                        f"{FAIL}Verify if less secure apps is been enable to sender address ({sender_email}) check here"
                        f": https://support.google.com/accounts/answer/6010255?hl=en {ENDC}")
                    init()

            elif answer == "no" or "n" or "N":
                pass

            else:
                print("Error, please enter a correct value")
                test_email()

        test_email()

    config_email()
    print(f"{WARNING}Successfully config email{ENDC}")

    print(f"Verification of the packages make sure that no task are active with the {BOLD}APT{ENDC} command ...")
    try:
        os.system("sudo apt install -y systemd sysstat")
        print("Verification and installation completed.")
    except:
        print("Installation failed retry another time with the command 'sudo apt install -y systemd'.")

    def config_service():
        print(f"{OKBLUE}Config service{ENDC} :")

        answer = input("Do you want to activate the autostart ? [y/n]: ")

        if answer == "yes" or "y" or "Y":
            print("")
            service = open(f"/lib/systemd/system/{service_name}.service", "w")
            service.write(f"[Unit]\n"
                          f"Description = Ultimate Auto Check Service\n"
                          f"[Service]\n"
                          f"ExecStart = /usr/local/bin/uacs -v start\n"
                          f"[Install]\n"
                          f"WantedBy = default.target\n")
            service.close()

        elif answer == "no" or "n" or "N":
            pass

        else:
            print("Error, please enter a correct value")
            config_service()

        def start_service():
            answer = input("Do you want to start the service now ? [y/n]: ")
            if answer == "yes" or "y" or "Y":
                commande = ["sudo systemctl daemon-reload", f"sudo systemctl enable {service_name}"]
                for i in range(len(commande)):
                    print(commande[i])
                    os.system(commande[i])

            elif answer == "no" or "n" or "N":
                pass

            else:
                print("Error, please enter a correct value")
                start_service()

        start_service()

        print("Configuration successful, add new service with : uacs -a 'service.service'")
        exit()

    config_service()


if __name__ == '__main__':
    main()
