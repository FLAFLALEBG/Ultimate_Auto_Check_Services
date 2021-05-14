#!/usr/bin/env python

# --------------* TO DO *-------------- #

# TODO : ajouter deepl API pour traduire les massages.
# TODO : possibilitée de retirer les services de la liste
# TODO : Optimiser le code :
#  - avec des objets pour le init
#  - optimiser les imports

# --------------* IMPORT *-------------- #

import datetime
import os
import smtplib
import ssl
import pickle
import sys
import time

# --------------* VARIABLES *-------------- #

service_check = []
exec_py_file = "uacs"
file_ini_service = "../config/service_monitored"
file_ini_email = "../config/email"
service_name = "ultimate_auto_check_service"
sender_email, email_password, receiver_email, smtp_server = "", "", "", ""
email_smtp_port = 0

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
def enablePrint():
    sys.stdout = sys.__stdout__


def restore(verbose):
    restore_email(verbose)
    restore_service(verbose)


def restore_service(verbose):  # Restauration des services depuis un fichier (file_ini)
    if verbose:
        enablePrint()

    global service_check
    print("Service restoration")
    print(f"Searching for the file : {file_ini_service}")
    if os.path.isfile(file_ini_service):
        print("File found !")

        print("Opening the file ...")
        backup_file = open(file_ini_service, "rb")

        print(f"Reading variables in the file : " + file_ini_service)
        services_restored = pickle.load(backup_file)
        backup_file.close()

        print("Adding the backup to the buffer")
        service_check.append(services_restored)

        print(f"The {services_restored} services have been added")

    else:
        # The file does not exist
        print(f"File {file_ini_service} not found")


# noinspection PyUnusedLocal
def restore_email(verbose):  # Restauration de l'email / mot de passe depuis le fichier
    if verbose:
        enablePrint()

    global sender_email, email_password, receiver_email, smtp_server, email_smtp_port

    print("Restauration of the email address and its password")
    print(f"Searching for the file : {file_ini_email}")
    if os.path.isfile(file_ini_email):
        print("File found !")

        print("Opening the file ...")
        backup_file = open(file_ini_email, "rb")

        print(f"Reading variables in the file : " + file_ini_email)
        email_restored = pickle.load(backup_file)
        backup_file.close()

        sender_email = email_restored[0]
        email_password = email_restored[1]
        receiver_email = email_restored[2]
        smtp_server = email_restored[3]
        email_smtp_port = email_restored[4]

        print(f"The email adresse have been restored")

    else:
        # The file does not exist
        print(f"File {file_ini_email} not found")


def append(append_service, verbose):  # Ajoute un service a la liste et l'ajoute également au fichier (file_ini)
    if verbose:
        enablePrint()

    # Verification de l'existence du service et l'enregistre
    print(f"Verification of the existence of the service {append_service} and registration ...")
    print(f""""systemctl list-unit-files | grep "^{append_service}" """)
    exist_service = os.system(f""""systemctl list-unit-files | grep "^{append_service}" """)
    if str(exist_service).find(".service"):
        print("Service exist \nSaving ...")

        service_to_append = append_service

        print(f"Opening the file {file_ini_service}")
        backup_file = open(file_ini_service, "wb")

        print(f"Appending the service {append_service}")
        pickle.dump(service_to_append, backup_file)
        backup_file.close()
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
        if str(active).find("active"):
            print("Service is active")
            pass

        elif str(active).find("inactive"):
            print(f"Service is inactive \nLaunch of the restart of the services {service_check[i]}")
            service_down(service_check[i], verbose)


def service_down(service, verbose):
    if verbose:
        enablePrint()

    # Essaye de relancer 3x le service
    # et envoie un mail si il ne redémarre pas
    number_restart = 3
    for i in range(number_restart):
        print(f"Relaunching n°{i}/{number_restart}")
        active = os.system(f"systemctl status {service} | grep active")
        if str(active).find("inactive"):
            os.system(f"systemctl restart {service}")
            continue
        elif str(active).find("active"):
            print(f"Successful restarting service {service}")
            break
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

    # Envoie un mail
    now = datetime.datetime.now()
    message = f"""\
        Subject: Oh non le service {subject} à planté !

        Bonjour, Je tiens à vous informer que ce jour le {now.day}/{now.month}/{now.year} à {now.hour}:{now.minute} le 
        service intitulé {subject} à planté avec ceci en log : '{os.popen(f"systemctl status {subject}")}'.
        Plusieurs operation affin de le relancer ont toutes échouées
        From Auto_Check_service Python Bot"""

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, email_smtp_port, context=context) as server:
            server.login(sender_email, email_password)

            server.sendmail(sender_email, receiver_email, message)

            print("Successful sending mail")

    except:
        print("Sending error please check the sender's email and password or the receiver's")


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

        sys.stdout.write("Saving")

        # Enregistrement des variables dans le fichier
        variables = [sender_email, email_password, receiver_email, smtp_server, email_smtp_port]
        sys.stdout.write("..")
        time.sleep(0.5)
        backup_file = open(file_ini_email, "wb")
        sys.stdout.write("..")
        time.sleep(0.5)
        pickle.dump(variables, backup_file)
        sys.stdout.write("..")
        time.sleep(0.5)
        backup_file.close()
        sys.stdout.write("\b\b\b\b\b\b\b\b\b\b")  # Erase "Saving..."
        sys.stdout.write("Saved !\n")
        time.sleep(0.5)

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
        os.system("sudo apt install -y systemd")
        print("Verification and installation completed.")
    except:
        print("Installation failed retry another time with the command 'sudo apt install -y systemd'.")

    def config_service():
        print(f"{OKBLUE}Config service{ENDC} :")

        answer = input("Do you want to activate the autostart ? [y/n]: ")

        if answer == "yes" or "y" or "Y":
            print("")
            service = open(f"/lib/systemd/system/{service_name}.service", "w")
            service.write(f"[Unit]"
                          f"Description = Ultimate Auto Check Service"
                          f"[Service]"
                          f"ExecStart = {os.path.join(os.path.dirname(__file__), exec_py_file)} run"
                          f"[Install]"
                          f"WantedBy = default.target")
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

        print("Configuration successful, add new service with : uacs -a 'service.service'")

    config_service()
