#!/usr/bin/python3
# -*- coding: utf-8 -*-
# RadiON -- version 1.3
# Author: Alexey


# Подключение библиотек
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os
import time

from daemon import Daemon


class MyDaemon(Daemon):
    def __init__(self, pidfile):
        self.pidfile = pidfile
        super().__init__(pidfile)

        # Переменные
        self.on_off = ["off", "on"]
        self.frequency = 87.9
        self.shuffle = False
        self.play_stereo = True
        self.timebackup = 3600
        self.music_dir = os.path.join(os.getcwd(), "files/")
        self.backup_dir = os.path.join(os.getcwd(), "backup/")
        self.tmp_dir = os.path.join(os.getcwd(), "tmp/")
        self.download_dir = os.path.join(os.getcwd(), "download/")
        self.convert_dir = os.path.join(os.getcwd(), "convert/")
        self.config_location = os.path.join(os.getcwd(), "radio.conf")
        self.start_file = os.path.join(os.getcwd(), "fm_tr")

        self.backup_location = os.path.join(os.getcwd(), "backup.py")
        self.converting_location = os.path.join(os.getcwd(), "converting.py")
        self.playfile_location = os.path.join(os.getcwd(), "playfile.py")
        self.sortD_location = os.path.join(os.getcwd(), "sortD.py")

    def find(self):
        # Создание каталогов и файлов, если их ещё нет
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
            print('Каталог успешно создан', self.music_dir)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            print('Каталог успешно создан', self.backup_dir)
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
            print('Каталог успешно создан', self.tmp_dir)
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            print('Каталог успешно создан', self.download_dir)
        if not os.path.exists(self.convert_dir):
            os.makedirs(self.convert_dir)
            print('Каталог успешно создан', self.convert_dir)
        # Проверка наличия файлаов
        if not os.path.exists(self.start_file):
            print('Нет файла с программой в каталоге!')
            os.abort()
        if not os.path.exists(self.config_location):
            MyDaemon.create_config(self)
            print('Файл успешно создан по пути ', self.config_location)
        return None

    def create_config(self):
        # Создание файла конфигурации
        config = configparser.ConfigParser()
        config.add_section("radio")
        tmp = str(self.play_stereo)
        config.set("radio", "play_stereo", tmp)
        config.set("radio", "frequency", str(self.frequency))
        config.set("radio", "shuffle", str(self.shuffle))
        config.set("radio", "timebackup", str(self.timebackup))
        config.set("radio", "music_dir", self.music_dir)
        config.set("radio", "backup_dir", self.backup_dir)
        config.set("radio", "tmp_dir", self.tmp_dir)
        config.set("radio", "download_dir", self.download_dir)
        config.set("radio", "convert_dir", self.convert_dir)
        with open(self.config_location, "w") as config_file:
            config.write(config_file)
        return None

    def read_config(self):
        global config
        try:
            config = configparser.ConfigParser()
            config.read(self.config_location)
        except:
            if not os.path.exists(self.config_location):
                print("Error reading from config file.")
                MyDaemon.create_config(self)
                print('Файл успешно создан по пути ', self.config_location)
            else:
                self.play_stereo = config.getboolean("radio", 'play_stereo', fallback=True)
                self.frequency = config.get("radio", 'frequency', fallback=87.9)
                self.shuffle = config.getboolean("radio", 'shuffle', fallback=False)
                self.timebackup = config.get("radio", 'timebackup', fallback=3600)
                self.music_dir = config.get("radio", 'music_dir', fallback=self.music_dir)
                self.backup_dir = config.get("radio", 'backup_dir', fallback=self.backup_dir)
                self.tmp_dir = config.get("radio", 'tmp_dir', fallback=self.tmp_dir)
                self.download_dir = config.get("radio", 'download_dir', fallback=self.download_dir)
                self.convert_dir = config.get("radio", 'convert_dir', fallback=self.convert_dir)
            return None

    def starting_program(self):
        print("Скрипт запущен:")
        MyDaemon.read_config(self)
        MyDaemon.find(self)
        return None

    def run(self):
        print("main ran")
        MyDaemon.starting_program(self)
        while True:
            time.sleep(1)


# pidFile2 = '/var/run/MainDaemon.pid'
pidFile2 = os.path.join(os.getcwd(),'/MainDaemon.pid')
a = MyDaemon(pidFile2)
a.start()
# a.run()
