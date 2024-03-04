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


def sorts_date(data: list):
    '''сортирует по дате и оставляет только успешные транзакции и возвращает последние 5 операций'''

    data = sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=True)
    return data[:5]


def formatted_date(data: list):
    '''форматирует дату'''

    formatted_transactions = []
    for el in data:
        date_str = el["date"]
        formatted_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        el["date"] = formatted_date
        formatted_transactions.append(el)
    return formatted_transactions