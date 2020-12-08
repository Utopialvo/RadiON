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
    import time

# Переменные
timebackup = 3600
backup_dir = os.path.join(os.getcwd(), "backup/")
tmp_dir = os.path.join(os.getcwd(), "tmp/")
config_location = os.path.join(os.getcwd(), "radio.conf")


def find(backup_dir, tmp_dir):
    # Создаём каталоги и файлы, если их ещё нет
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
        print('Каталог успешно создан', backup_dir)
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
        print('Каталог успешно создан', tmp_dir)
    return None


def read_config(config_location):
    global backup_dir
    global tmp_dir
    try:
        config = configparser.ConfigParser()
        config.read(config_location)
    except:
        if not os.path.isfile(config_location):
            print("Error reading from config file.")
            os.abort()
    else:
        timebackup = config.get("radio", 'timebackup', fallback=3600)
        backup_dir = config.get("radio", 'backup_dir', fallback=backup_dir)
        tmp_dir = config.get("radio", 'tmp_dir', fallback=tmp_dir)
    return None


def backup(backup_dir, tmp_dir):
    # Файлы и каталоги, которые необходимо скопировать.
    # Резервные копии должны храниться в основном каталоге резерва.
    # Текущая дата служит именем подкаталога в основном каталоге
    today = backup_dir + time.strftime('%Y.%m.%d')
    # Создаём каталог, если его ещё нет
    if not os.path.exists(today):
        os.mkdir(today)  # создание каталога
        print('Каталог успешно создан', today)
    # Текущее время служит именем zip-архива
    now = time.strftime('%H.%M.%S')
    # Файлы помещаются в zip-архив.
    # tar -zcvf /home/backup/2220.tar.gz /home/tmp/*
    zip_command = "tar -zcvf " + today + os.sep + now + ".tar.gz" + " " + tmp_dir + '*'
    # Запускаем создание резервной копии
    if os.system(zip_command) == 0:
        print('Резервная копия успешно создана')
    else:
        print('Создание резервной копии НЕ УДАЛОСЬ')

    # rm -fr /home/radioLiberty/backup/*
    rem_command = "rm -fr " + tmp_dir + "*"
    # Удаление файлов в папке
    if os.system(rem_command) == 0:
        print('Успешно удалено')
    else:
        print('Удаление НЕ УДАЛОСЬ')
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
        find(backup_dir, tmp_dir)
        if os.listdir(tmp_dir):
            backup(backup_dir, tmp_dir)
            time.sleep(int(timebackup))
        else:
            time.sleep(int(timebackup))
    return 0


main()
