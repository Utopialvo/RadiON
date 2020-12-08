#!/usr/bin/python3
# RadiON -- version 1.2
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

# Переменные
play_stereo = True
music_dir = os.path.join(os.getcwd(), "files/")
convert_dir = os.path.join(os.getcwd(), "convert/")
config_location = os.path.join(os.getcwd(), "radio.conf")

def find(music_dir, convert_dir):
    # Создаём каталоги и файлы, если их ещё нет
    if not os.path.exists(music_dir):
        os.mkdir(music_dir)
        print('Каталог успешно создан', music_dir)
    if not os.path.exists(convert_dir):
        os.mkdir(convert_dir)
        print('Каталог успешно создан', convert_dir)
    return None

def read_config(config_location):
    global convert_dir
    global music_dir
    global play_stereo
    try:
        config = configparser.ConfigParser()
        config.read(config_location)
    except:
        if not os.path.isfile(config_location):
            print("Error reading from config file.")
            os.abort()
    else:
        convert_dir = config.get("radio", 'convert_dir', fallback=convert_dir)
        music_dir = config.get("radio", 'music_dir', fallback=music_dir)
        play_stereo = config.getboolean("radio", 'play_stereo', fallback=True)
    return None


def convertingfiles(music_dir, convert_dir):
    for root, folders, files in os.walk(convert_dir):
        for filename in files:
            if re.search(".(aac|mp3|m4a|ogg|ac3)$", filename) is not None:
                file_music = filename[0:-3]
                command = "sox " + (root + filename) + " -r 192000 " + ("-c 2" if play_stereo else "-c 1") + " -b 16 -t wav " + (root + file_music) + "wav"
                subprocess.call(command, shell=True)
                os.rename(((root + file_music) + "wav"), ((music_dir + file_music) + "wav"))
                os.remove(root + filename)
            elif re.search(".(flac)$", filename) is not None:
                file_music = filename[0:-4]
                command = "sox " + (root + filename) + " -r 192000 " + ("-c 2" if play_stereo else "-c 1") + " -b 16 -t wav " + (root + file_music) + "wav"
                subprocess.call(command, shell=True)
                os.rename(((root + file_music) + "wav"), ((music_dir + file_music) + "wav"))
                os.remove(root + filename)
            else:
                os.remove(root + filename)
    return None

def daemonize():
    fpid = os.fork()
    if fpid != 0:
        os.abort()
    return None

def main():
    daemonize()
    while True:
        read_config(config_location)
        find(music_dir, convert_dir)
        if os.listdir(convert_dir):
            convertingfiles(music_dir, convert_dir)
        else:
            time.sleep(60)
    return 0


main()