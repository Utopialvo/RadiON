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
    import re
    import random
    import os
    import time
    import subprocess

from daemon import Daemon


class playfile_daemon(Daemon):
    def __init__(self, pidfile):
        self.pidfile = pidfile
        super().__init__(pidfile)

        # Переменные
        self.on_off = ["off", "on"]
        self.frequency = 87.9
        self.shuffle = False
        self.play_stereo = True
        self.music_dir = os.path.join(os.getcwd(), "files/")
        self.tmp_dir = os.path.join(os.getcwd(), "tmp/")
        self.config_location = os.path.join(os.getcwd(), "radio.conf")
        self.start_file = os.path.join(os.getcwd(), "fm_tr")

    # Реализация функций
    def find(self):
        # Создаём каталоги и файлы, если их ещё нет
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
            print('Каталог успешно создан', self.music_dir)
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
            print('Каталог успешно создан', self.tmp_dir)
        # Проверка наличия файлаов
        if not os.path.exists(self.start_file):
            print('Нет файла с программой в каталоге!')
            os.abort()
        if not os.path.exists(self.config_location):
            print('Нет файла c конфигом в каталоге!')
            os.abort()
        return None

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_location)
        except:
            if not os.path.exists(self.config_location):
                print('Нет файла c конфигом в каталоге!')
                os.abort()
        else:
            self.play_stereo = config.getboolean("radio", 'play_stereo', fallback=True)
            self.frequency = config.get("radio", 'frequency', fallback=87.9)
            self.shuffle = config.getboolean("radio", 'shuffle', fallback=False)
            self.music_dir = config.get("radio", 'music_dir', fallback=self.music_dir)
            self.tmp_dir = config.get("radio", 'tmp_dir', fallback=self.tmp_dir)
        return None

    def build_file_list(self):
        file_list = []
        for root, folders, files in os.walk(self.music_dir):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(wav)$", filename) != None:
                    file_list.append(os.path.join(root, filename))
        return file_list

    def play_songs(self, file_list):
        f = open(self.tmp_dir + time.strftime('%Y.%m.%d') + '.(' + time.strftime('%H') + ').txt', 'a')
        print("Playing songs to frequency ", str(self.frequency))
        print("Shuffle is " + self.on_off[self.shuffle])
        print("Stereo playback is " + self.on_off[self.play_stereo])
        if self.shuffle == True:
            # Перемешать плейлист
            random.shuffle(file_list)
        for filename in file_list:
            command = self.start_file + " -f " + self.frequency + " -b 200 " + filename
            subprocess.call(command, shell=True)
            f.write(time.strftime('%Y.%m.%d') + ":" + time.strftime('%H.%M.%S') + " --> " + filename + '\n')
            os.rename(filename, self.tmp_dir + os.path.basename(filename))
        f.close()
        return None

    def starting_program(self):
        if os.listdir(self.music_dir):
            playfile_daemon.read_config(self)
            playfile_daemon.find(self)
            files = playfile_daemon.build_file_list(self)
            playfile_daemon.play_songs(self, files)
        return 0

    def run(self):
        while True:
            playfile_daemon.starting_program(self)
            time.sleep(60)

# pidFile5 = '/var/run/PlayFileDaemon.pid'
pidFile5 = os.path.join(os.getcwd(), '/PlayFileDaemon.pid')
a = playfile_daemon(pidFile5)
a.start()
# a.run()
