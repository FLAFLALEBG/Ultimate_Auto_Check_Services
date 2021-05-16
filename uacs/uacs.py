#!/usr/bin/env python

from uacs.function import *
import os
import __init__
import sys

sys.stdout = open(os.devnull, 'w')
restore(False)

# --------------* Variables *-------------- #

option = 1
command = 2
argument = 3
have_argument = False


# --------------* Argv *-------------- #

def main():
    global option, command, argument, verbose
    # ---* Option *--- #
    try:

        if str(sys.argv[1]) == "-v" or str(sys.argv[1]) == "--verbose":
            sys.stdout = sys.__stdout__
            verbose = True

        elif str(sys.argv[1]) != "-v" or str(sys.argv[1]) != "--verbose":
            option -= 1
            command -= 1
            argument -= 1
            verbose = False

    except:
        __init__.run_daemon()  # Run daemon

    # ---* Command *--- #
    try:
        if str(sys.argv[command]) == "append":
            try:
                argv_service = sys.argv[command + 1]
                append(argv_service, verbose)
            except:
                print("commande usage: uacs append 'service_to_append'")

        elif str(sys.argv[command]) == "--help" or str(sys.argv[command]) == "-h":
            sys.stdout = sys.__stdout__
            docs = open("../docs/help.txt", "r")
            print(docs.read())
            docs.close()

        elif str(sys.argv[command]) == "start":
            __init__.run_daemon()

        elif str(sys.argv[command]) == "send_mail":
            send_mail("test", verbose)

        elif str(sys.argv[command]) == "restore":
            restore(verbose)

        elif str(sys.argv[command]) == "restore_service":
            restore_service(verbose)

        elif str(sys.argv[command]) == "restore_email":
            restore_email(verbose)

        elif str(sys.argv[command]) == "init":
            init()

        elif str(sys.argv[command]) == "stop":
            pass  # running = False

    except:
        print("Command invalid or invalid arguments")


if __name__ == '__main__':
    main()
