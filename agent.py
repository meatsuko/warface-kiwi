import json
from termcolor import colored
from time import sleep

from requests_kiwi import RequestsKIWI

def worker(requests_kiwi):
    print('Если вы заполнили конфигурационный файл, напишите', colored('start', 'grey', 'on_white'))
    start = str(input())
    if start == '':
        activetask = requests_kiwi.getTasks(requests_kiwi.callback_activetask)
        if activetask != None:
            print('Выполняется задание:', activetask[0][0]['title'])
            remaining_time = activetask[0][0]['remaining_time']
            while remaining_time > 0:
                print('Время до завершения: {} секунд     '.format(remaining_time), end='\r')
                remaining_time -= 1
                sleep(1)
            print('Задание завершено!                     ')
        else:
            print(colored('Нет активных заданий!', 'magenta'))
    print('\nПодготовка к запуску заданий...')


def tasks_list(requests_kiwi):
    print('СПИСОК ЗАДАНИЙ:')
    allChains = requests_kiwi.getTasks(requests_kiwi.callback_avatartask)
    for chain in allChains:
        for task in chain:
            print('Задание:', colored(task['id'], 'green'), '| Название:', task['title'])
            if task['status'] == 'disabled':
                print('Статус:', colored('недоступно\n', 'red'))
            else:
                print('Статус:', colored('доступно\n', 'green'))
    print('Выберите нужные задания и добавьте в файл конфигурации.')
    print('Перезапустите программу после добавления заданий\n')


def auth(config):
    requests_kiwi = RequestsKIWI()
    requests_kiwi.auth(config['login'], config['password'])
    return requests_kiwi


def read_config():
    path = 'config_kiwi.json'
    with open(path, 'r') as f:
        config = json.loads(f.read())
    return config


if __name__ == "__main__":
    print(colored("Warface K.I.W.I. Agent", 'magenta'))
    print(colored("Powered by Python 3.7 with love by Meatsuko and Snoups.\n", 'magenta'))
    requests_kiwi = auth(read_config())
    tasks_list(requests_kiwi)
    worker(requests_kiwi)
