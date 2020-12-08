#!/usr/bin/python3
# RadiON -- version 1.2
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

# Переменные
on_off = ["off", "on"]
frequency = 87.9
shuffle = False
play_stereo = True
timebackup = 3600
music_dir = os.path.join(os.getcwd(), "files/")
backup_dir = os.path.join(os.getcwd(), "backup/")
tmp_dir = os.path.join(os.getcwd(), "tmp/")
download_dir = os.path.join(os.getcwd(), "download/")
convert_dir = os.path.join(os.getcwd(), "convert/")
config_location = os.path.join(os.getcwd(), "radio.conf")
start_file = os.path.join(os.getcwd(), "fm_tr")

def daemonize():
    fpid = os.fork()
    if fpid != 0:
        os.abort()
    return None

# Реализация функций
def main():
    daemonize()
    while True:
        # Чтение конфига
        read_config(config_location)
        # Скрипт проверяет наличие каталогов и конфига
        find(music_dir, backup_dir, tmp_dir, download_dir, convert_dir, start_file, config_location)
        if os.listdir(music_dir):
            # Плейлист
            files = build_file_list(music_dir)
            # Повтор файлов
            play_songs(files)
        else:
            time.sleep(60)
    return 0


def find(music_dir, backup_dir, tmp_dir, download_dir, convert_dir,  start_file, config_location):
    # Создаём каталоги и файлы, если их ещё нет
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        print('Каталог успешно создан', music_dir)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print('Каталог успешно создан', backup_dir)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print('Каталог успешно создан', tmp_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print('Каталог успешно создан', download_dir)
    if not os.path.exists(convert_dir):
        os.makedirs(convert_dir)
        print('Каталог успешно создан', convert_dir)
    # Проверка наличия файлаов
    if not os.path.exists(start_file):
        print('Нет файла с программой в каталоге!')
        os.abort()
    if not os.path.exists(config_location):
        name_location = "radio.conf"
        create_config(name_location)
        print('Файл успешно создан по пути ', config_location)
    return None


def create_config(name):
    # Создание файла конфигурации
    config = configparser.ConfigParser()
    config.add_section("radio")
    config.set("radio", "play_stereo", str(play_stereo))
    config.set("radio", "frequency", str(frequency))
    config.set("radio", "shuffle", str(shuffle))
    config.set("radio", "timebackup", str(timebackup))
    config.set("radio", "music_dir", music_dir)
    config.set("radio", "backup_dir", backup_dir)
    config.set("radio", "tmp_dir", tmp_dir)
    config.set("radio", "download_dir", download_dir)
    config.set("radio", "convert_dir", convert_dir)
    with open(name, "w") as config_file:
        config.write(config_file)
    return None

def read_config(config_location):
    global frequency
    global shuffle
    global play_stereo
    global timebackup
    global music_dir
    global backup_dir
    global tmp_dir
    global download_dir
    global convert_dir
    try:
        config = configparser.ConfigParser()
        config.read(config_location)
    except:
        if not os.path.exists(config_location):
            print("Error reading from config file.")
            os.abort()
    else:
        play_stereo = config.getboolean("radio", 'play_stereo', fallback=True)
        frequency = config.get("radio", 'frequency', fallback=87.9)
        shuffle = config.getboolean("radio", 'shuffle', fallback=False)
        timebackup = config.get("radio", 'timebackup', fallback=3600)
        music_dir = config.get("radio", 'music_dir', fallback=music_dir)
        backup_dir = config.get("radio", 'backup_dir', fallback=backup_dir)
        tmp_dir = config.get("radio", 'tmp_dir', fallback=tmp_dir)
        download_dir = config.get("radio", 'download_dir', fallback=download_dir)
        convert_dir = config.get("radio", 'convert_dir', fallback=convert_dir)
    return None


def build_file_list(music_dir):
    file_list = []
    for root, folders, files in os.walk(music_dir):
        folders.sort()
        files.sort()
        for filename in files:
            if re.search(".(wav)$", filename) != None:
                file_list.append(os.path.join(root, filename))
    return file_list


def play_songs(file_list):
    f = open(tmp_dir + time.strftime('%Y.%m.%d') + '.('+ time.strftime('%H') + ').txt', 'a')
    print("Playing songs to frequency ", str(frequency))
    print("Shuffle is " + on_off[shuffle])
    print("Stereo playback is " + on_off[play_stereo])
    if shuffle == True:
        # Перемешать плейлист
        random.shuffle(file_list)
    for filename in file_list:
        command = start_file + " -f " + frequency + " -b 200 " + filename
        subprocess.call(command, shell=True)
        f.write(time.strftime('%Y.%m.%d') + ":" + time.strftime('%H.%M.%S') + " --> " + filename + '\n')
        os.rename(filename, tmp_dir + os.path.basename(filename))
    f.close()
    return None


main()
