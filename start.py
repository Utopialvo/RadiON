#!/usr/bin/python3
# -*- coding: utf-8 -*-
# RadiON -- version 1.3
# Author: Alexey


# Подключение библиотек
import time
import sys
import tempfile

from daemon3x import daemon
from main import MyDaemon
from sortD import sortD_daemon
from converting import converting_daemon
from playfile import playfile_daemon
from backup import backup_daemon


class StartDaemon(daemon):
    def run(self):
        while True:
            time.sleep(1)


if __name__ == "__main__":
    pidFile = tempfile.gettempdir() + '/StartDaemon.pid'
    one = StartDaemon(pidFile)

    pidFile2 = tempfile.gettempdir() + '/MainDaemon.pid'
    two = MyDaemon(pidFile2)

    pidFile3 = tempfile.gettempdir() + '/SortDdaemon.pid'
    three = sortD_daemon(pidFile3)

    pidFile4 = tempfile.gettempdir() + '/ConvertingDaemon.pid'
    four = converting_daemon(pidFile4)

    pidFile5 = tempfile.gettempdir() + '/PlayFileDaemon.pid'
    five = playfile_daemon(pidFile5)

    pidFile6 = tempfile.gettempdir() + '/BackupDaemon.pid'
    six = backup_daemon(pidFile6)


    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            one.start()
            two.start()
            three.start()
            four.start()
            five.start()
            six.start()
        elif 'stop' == sys.argv[1]:
            one.stop()
            two.stop()
            three.stop()
            four.stop()
            five.stop()
            six.stop()
        elif 'restart' == sys.argv[1]:
            one.restart()
            two.restart()
            three.restart()
            four.restart()
            five.restart()
            six.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
