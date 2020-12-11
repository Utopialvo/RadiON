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
    import subprocess
    import time

from daemon3x import daemon


class converting_daemon(daemon):
    def __init__(self, pidfile):
        self.pidfile = pidfile
        super().__init__(pidfile)

        # Переменные
        self.play_stereo = True
        self.music_dir = os.path.join(os.getcwd(), "files/")
        self.convert_dir = os.path.join(os.getcwd(), "convert/")
        self.config_location = os.path.join(os.getcwd(), "radio.conf")

    def find(self):
        # Создаём каталоги и файлы, если их ещё нет
        if not os.path.exists(self.music_dir):
            os.mkdir(self.music_dir)
            print('Каталог успешно создан', self.music_dir)
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
            self.convert_dir = config.get("radio", 'convert_dir', fallback=self.convert_dir)
            self.music_dir = config.get("radio", 'music_dir', fallback=self.music_dir)
            self.play_stereo = config.getboolean("radio", 'play_stereo', fallback=True)
        return None

    def convertingfiles(self):
        for root, folders, files in os.walk(self.convert_dir):
            for filename in files:
                if re.search(".(aac|mp3|m4a|ogg|ac3)$", filename) is not None:
                    file_music = filename[0:-3]
                    command = "sox " + (root + filename) + " -r 192000 " + (
                        "-c 2" if self.play_stereo else "-c 1") + " -b 16 -t wav " + (root + file_music) + "wav"
                    subprocess.call(command, shell=True)
                    os.rename(((root + file_music) + "wav"), ((self.music_dir + file_music) + "wav"))
                    os.remove(root + filename)
                elif re.search(".(flac)$", filename) is not None:
                    file_music = filename[0:-4]
                    command = "sox " + (root + filename) + " -r 192000 " + (
                        "-c 2" if self.play_stereo else "-c 1") + " -b 16 -t wav " + (root + file_music) + "wav"
                    subprocess.call(command, shell=True)
                    os.rename(((root + file_music) + "wav"), ((self.music_dir + file_music) + "wav"))
                    os.remove(root + filename)
                else:
                    os.remove(root + filename)
        return None

    def starting_program(self):
        if os.listdir(self.convert_dir):
            converting_daemon.read_config(self)
            converting_daemon.find(self)
            converting_daemon.convertingfiles(self)
        return 0

    def run(self):
        while True:
            converting_daemon.starting_program(self)
            time.sleep(60)


#pidFile4 = '/var/run/ConvertingDaemon.pid'
#a = converting_daemon(pidFile4)
#a.run()