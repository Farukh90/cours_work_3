import json
import os
from datetime import datetime
from config import ROOT_DIR

path = os.path.join(ROOT_DIR, 'src')
file_name = 'operations.json'
os_path = os.path.join(path, file_name)


def load_data(file: str):
    '''загружает данные из файла json'''
    with open(file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def executed_transactions(data: list):
    '''фильтрует успешные транзакции'''

    sorted_data = []
    for i in data:
        if not i or i.get('state') == 'CANCELED':
            continue
        sorted_data.append(i)
    return sorted_data