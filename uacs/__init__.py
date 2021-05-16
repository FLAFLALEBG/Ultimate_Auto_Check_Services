#!/usr/bin/env python

from uacs.function import *
from uacs.uacs import *
import time

running = True


def run_daemon():
    print("Starting...")
    function.restore(True)
    print("Started !")
    while running:
        time.sleep(30)
        print("New Verification")
        function.check_service(True)

    print("Stopped")


if __name__ == '__main__':
    run_daemon()
