#!/usr/bin/env python

import uacs
import os
import sys

uid = os.getuid()

sys.stdout = open(os.devnull, 'w')
uacs.restore(False)

if uid != 0:
    print("\033[1mYou must be root for execute this program")
    exit()

else:
    pass

# --------------* Variables *-------------- #

option = 1
command = 2
argument = 3
have_argument = False


# --------------* Argv *-------------- #

# ---* Option *--- #
try:
    global verbose
    if str(sys.argv[1]) == "-v" or str(sys.argv[1]) == "--verbose":
        sys.stdout = sys.__stdout__
        verbose = True

    elif str(sys.argv[1]) != "-v" or str(sys.argv[1]) != "--verbose":
        option -= 1
        command -= 1
        argument -= 1
        verbose = False

except:
    uacs.run_daemon()  # Run daemon

# ---* Command *--- #
if str(sys.argv[command]) == "append":
    try:
        argv_service = sys.argv[command + 1]
        uacs.append(argv_service, verbose)
    except:
        print("commande usage: uacs append 'service_to_append'")

elif str(sys.argv[command]) == "start":
    uacs.run_daemon()

elif str(sys.argv[command]) == "send_mail":
    uacs.send_mail("test", verbose)

elif str(sys.argv[command]) == "restore":
    uacs.restore(verbose)

elif str(sys.argv[command]) == "restore_service":
    uacs.restore_service(verbose)

elif str(sys.argv[command]) == "restore_email":
    uacs.restore_email(verbose)

elif str(sys.argv[command]) == "init":
    uacs.init()

elif str(sys.argv[command]) == "stop":
    pass  # running = False

elif str(sys.argv[command]) == "--help" or str(sys.argv[command]) == "-h":
    sys.stdout = sys.__stdout__
    print("""
Usage:  uacs [OPTIONS] COMMAND [ARGUMENT]

Options:
  -v, --verbose    Shows more details on what the command does

Commands:
  restore          Restore Email and Service
  restore_service  Restore Services
  restore_email    Restore Email and Email's password
  init             Init UACS
  send_mail        Sends mail when a service crashes
  start            Force run uacs
  append           Append new service
  -h, --help       Shows this message
  stop             Stop all background scripts

Run 'uacs COMMAND --help' for more information on a command.
""")

exit(0)
