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
    import re
    import time

from daemon3x import daemon


class sortD_daemon(daemon):
    def __init__(self, pidfile):
        self.pidfile = pidfile
        super().__init__(pidfile)

        # Переменные
        self.music_dir = os.path.join(os.getcwd(), "files/")
        self.download_dir = os.path.join(os.getcwd(), "download/")
        self.convert_dir = os.path.join(os.getcwd(), "convert/")
        self.config_location = os.path.join(os.getcwd(), "radio.conf")

    def find(self):
        # Создаём каталоги и файлы, если их ещё нет
        if not os.path.exists(self.music_dir):
            os.mkdir(self.music_dir)
            print('Каталог успешно создан', self.music_dir)
        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)
            print('Каталог успешно создан', self.download_dir)
        if not os.path.exists(self.convert_dir):
            os.mkdir(self.convert_dir)
            print('Каталог успешно создан', self.convert_dir)
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
            self.download_dir = config.get("radio", 'download_dir', fallback=self.download_dir)
            self.convert_dir = config.get("radio", 'convert_dir', fallback=self.convert_dir)
            self.music_dir = config.get("radio", 'music_dir', fallback=self.music_dir)
        return None

    def refract(self):
        for root, folders, files in os.walk(self.download_dir):
            for filename in files:
                if re.search(".(wav)$", filename) is not None:
                    # Удаление пробелов и сортировка
                    name = self.music_dir + filename
                    name = name.split()
                    name = ''.join(name)
                    os.rename(os.path.join(root, filename), name)
                elif re.search(".(aac|mp3|flac|m4a|ogg|ac3)$", filename) is not None:
                    name = self.convert_dir + filename
                    name = name.split()
                    name = ''.join(name)
                    os.rename(os.path.join(root, filename), name)
                else:
                    os.remove(os.path.join(root, filename))
        return None

    def starting_program(self):
        if os.listdir(self.download_dir):
            sortD_daemon.read_config(self)
            sortD_daemon.find(self)
            sortD_daemon.refract(self)
        return 0

    def run(self):
        while True:
            sortD_daemon.starting_program(self)
            time.sleep(60)

#pidFile6 = '/var/run/SortDdaemon.pid'
#a = sortD_daemon(pidFile6)
#a.run()