#!/usr/bin/python3
# -*- coding: utf-8 -*-
# RadiON -- version 1.3
# Author: Alexey


# Подключение библиотек
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

finally:
    import os
    import time

from daemon import Daemon


class backup_daemon(Daemon):
    def __init__(self, pidfile):
        self.pidfile = pidfile
        super().__init__(pidfile)

        # Переменные
        self.timebackup = 3600
        self.backup_dir = os.path.join(os.getcwd(), "backup/")
        self.tmp_dir = os.path.join(os.getcwd(), "tmp/")
        self.config_location = os.path.join(os.getcwd(), "radio.conf")

    def find(self):
        # Создаём каталоги и файлы, если их ещё нет
        if not os.path.exists(self.backup_dir):
            os.mkdir(self.backup_dir)
            print('Каталог успешно создан', self.backup_dir)
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
            print('Каталог успешно создан', self.tmp_dir)
        return None

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_location)
        except:
            if not os.path.isfile(self.config_location):
                print("Error reading from config file.")
                os.abort()
        else:
            self.timebackup = config.get("radio", 'timebackup', fallback=3600)
            self.backup_dir = config.get("radio", 'backup_dir', fallback=self.backup_dir)
            self.tmp_dir = config.get("radio", 'tmp_dir', fallback=self.tmp_dir)
        return None

    def backup(self):
        # Текущая дата служит именем подкаталога в основном каталоге
        today = self.backup_dir + time.strftime('%Y.%m.%d')
        # Создаём каталог
        if not os.path.exists(today):
            os.mkdir(today)
            print('Каталог успешно создан', today)
        # Текущее время служит именем архива
        now = time.strftime('%H.%M.%S')
        # Файлы помещаются в архив.
        zip_command = "tar -zcvf " + today + os.sep + now + ".tar.gz" + " " + self.tmp_dir + '*'
        # Проверка создания резервной копии
        if os.system(zip_command) == 0:
            print('Резервная копия успешно создана')
        else:
            print('Создание резервной копии НЕ УДАЛОСЬ')

        # rm -fr /home/radioLiberty/backup/*
        rem_command = "rm -fr " + self.tmp_dir + "*"
        # Удаление файлов в папке
        if os.system(rem_command) == 0:
            print('Успешно удалено')
        else:
            print('Удаление НЕ УДАЛОСЬ')
        return None

    def starting_program(self):
        if os.listdir(self.tmp_dir):
            backup_daemon.read_config(self)
            backup_daemon.find(self)
            backup_daemon.backup(self)
            time.sleep(int(self.timebackup))
        else:
            time.sleep(int(self.timebackup))
        return 0

    def run(self):
        while True:
            backup_daemon.starting_program(self)

# pidFile3 = '/var/run/BackupDaemon.pid'
pidFile3 = os.path.join(os.getcwd(), '/BackupDaemon.pid')
a = backup_daemon(pidFile3)
a.start()
# a.run()
