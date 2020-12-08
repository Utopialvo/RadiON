#!/usr/bin/python3
# RadiON -- version 1.2
# Author: Alexey

import os

backup_location = os.path.join(os.getcwd(), "backup.py")
converting_location = os.path.join(os.getcwd(), "converting.py")
playfile_location = os.path.join(os.getcwd(), "playfile.py")
sortD_location = os.path.join(os.getcwd(), "sortD.py")


def main():
    print("Скрипт запущен:")
    os.system("python3 " + playfile_location)
    print("Скрипт: " + playfile_location + "запущен")
    os.system("python3 " + sortD_location)
    print("Скрипт: " + sortD_location + "запущен")
    os.system("python3 " + converting_location)
    print("Скрипт: " + converting_location + "запущен")
    os.system("python3 " + backup_location)
    print("Скрипт: " + backup_location + "запущен")
    return None

main()