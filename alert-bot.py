import psutil
import requests
from configparser import ConfigParser
import schedule
import time
import datetime
import os
import sys
import subprocess

# configtxt = genfromtxt('config.txt')
# print(configtxt)
# from ConfigParser import ConfigParser # for python3
data_file = 'config.ini'

config = ConfigParser()
config.read(data_file)
# Line Notify
VERSION = '1.1.1'
LINE_TOKEN = config['TOKEN']['LINE_TOKEN']
LINE_URL = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': 'Bearer ' + LINE_TOKEN,
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

if LINE_TOKEN == "":
    print("Please add your LINE TOKEN in config.ini")


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def check_bot_status():
    process_name = config['PROCESS']['PROCESS_NAME']
    now = datetime.datetime.now()

    if process_name == "":
        print("No process name in config.ini")
    else:
        # Check if any chrome process was running or not.
        if checkIfProcessRunning(process_name):
            print(process_name, 'was running at', now)
        else:
            msg = f"\n{process_name}\"was stopped at {now}"
            print(process_name, 'was stopped at', now)
            re = requests.post(LINE_URL, headers=headers,
                               data={'message': msg})
            return schedule.CancelJob


welcome = 'Alert bot version:' + VERSION
re = requests.post(LINE_URL, headers=headers, data={'message': welcome})
print(re.text)


def main():
    schedule.every(10).seconds.do(check_bot_status)
    while True:
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)

    os.chdir(config['APPLICATION']['FOLDER'])  # Go to folder before run file
    os.startfile(config['APPLICATION']['PATH'])  # run file
    time.sleep(5)

    main()


main()
