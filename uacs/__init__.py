#!/usr/bin/env python3.8

from uacs import function
import time


def main():
    print("Starting...")
    function.restore(True)
    running = True
    print("Started !")
    while running:
        time.sleep(30)
        print("New Verification")
        function.check_service(True)

    print("Stopped")


if __name__ == '__main__':
    main()
