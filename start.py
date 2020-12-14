#!/usr/bin/python3
# -*- coding: utf-8 -*-
# RadiON -- version 1.3
# Author: Alexey


# Подключение библиотек
import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) == 2:
        arr = ['main.py', 'sortD.py', 'converting.py', 'playfile.py', 'backup.py']
        if 'start' == sys.argv[1]:
            for i in range(len(arr)):
                command = ("python3 {0} " + sys.argv[1]).format(arr[i])
                subprocess.call(command, shell=True)
        elif 'stop' == sys.argv[1]:
            for i in range(len(arr)):
                command = ("python3 {0} " + sys.argv[1]).format(arr[i])
                subprocess.call(command, shell=True)
        elif 'restart' == sys.argv[1]:
            for i in range(len(arr)):
                command = ("python3 {0} " + sys.argv[1]).format(arr[i])
                subprocess.call(command, shell=True)
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
