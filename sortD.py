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
    import time

# Переменные
music_dir = os.path.join(os.getcwd(), "files/")
download_dir = os.path.join(os.getcwd(), "download/")
convert_dir = os.path.join(os.getcwd(), "convert/")
config_location = os.path.join(os.getcwd(), "radio.conf")

def find(music_dir, download_dir, convert_dir):
    # Создаём каталоги и файлы, если их ещё нет
    if not os.path.exists(music_dir):
        os.mkdir(music_dir)
        print('Каталог успешно создан', music_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
        print('Каталог успешно создан', download_dir)
    if not os.path.exists(convert_dir):
        os.mkdir(convert_dir)
        print('Каталог успешно создан', convert_dir)
    return None

def read_config(config_location):
    global download_dir
    global convert_dir
    global music_dir
    try:
        config = configparser.ConfigParser()
        config.read(config_location)
    except:
        if not os.path.isfile(config_location):
            print("Error reading from config file.")
            os.abort()
    else:
        download_dir = config.get("radio", 'download_dir', fallback=download_dir)
        convert_dir = config.get("radio", 'convert_dir', fallback=convert_dir)
        music_dir = config.get("radio", 'music_dir', fallback=music_dir)
    return None

def refract(music_dir, download_dir, convert_dir):
    for root, folders, files in os.walk(download_dir):
        for filename in files:
            if re.search(".(wav)$", filename) is not None:
                #Удаление пробелов и сортировка
                name = music_dir + filename
                name = name.split()
                name = ''.join(name)
                os.rename(os.path.join(root, filename), name)
            elif re.search(".(aac|mp3|flac|m4a|ogg|ac3)$", filename) is not None:
                name = convert_dir + filename
                name = name.split()
                name = ''.join(name)
                os.rename(os.path.join(root, filename), name)
            else:
                os.remove(os.path.join(root, filename))
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
        find(music_dir, download_dir, convert_dir)
        if os.listdir(download_dir):
            refract(music_dir, download_dir, convert_dir)
        else:
            time.sleep(60)
    return 0


main()
