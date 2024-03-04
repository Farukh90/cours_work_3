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

    executed_data = []
    for i in data:
        if not i or i.get('state') == 'CANCELED':
            continue
        executed_data.append(i)
    return executed_data



def sorts_date(data: list):
    '''сортирует по дате и оставляет только успешные транзакции и возвращает последние 5 операций'''

    data = sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=True)
    return data[:5]


def formatted_date(data: list):
    '''сортирует по дате и оставляет только успешные транзакции'''
    for el in data:
        date_str = el["date"].split('T')
        numbers = date_str[0].split('-')
        y_, m_, d_ = numbers
        el["date"] = '.'.join([d_, m_, y_])

    return data


def group_card_numbers(transactions: list):
    '''группирует номера по 4 цифры'''
    for transaction in transactions:
        for key in transaction:
            if key in ['from', 'to']:
                parts = transaction[key].rsplit(' ', 1)
                parts[-1] = ' '.join([parts[-1][i:i + 4] for i in range(0, len(parts[-1]), 4)])
                # parts = ' '.join(parts)
                transaction[key] = parts
    return transactions


def mask_numbers(data: list):
    '''маскирует номера'''
    for i in data:

        if i['to'][0] == 'Счет':
            i['to'][1] = '**' + i['to'][1][-4:]
        else:
            i['to'][1] = i['to'][1][:7] + '** **** ' + i['to'][1][-4:]

        if 'from' in i:
            if i['from'][0] == 'Счет':
                i['from'][1] = '**' + i['from'][1][-4:]
            else:
                i['from'][1] = i['from'][1][:7] + '** **** ' + i['from'][1][-4:]
    return data


def make_result(data: list):
    '''выводит обработанную инфу'''
    for i in data:
        if 'from' in i:
            print(f'''
    {i['date']} {i['description']}
    {i['from'][0]} {i['from'][1]} -> {i['to'][0]} {i['to'][1]}''')
        else:
            print(f'''
    {i['date']} {i['description']}
    {i['to'][0]}  {i['to'][1]} ''')

#
# if __name__ == "__main__":
#     data = load_data(os_path)
#
#     execute = executed_transactions(data)
#
#     sorted_ = sorts_date(execute)
#
#     formated = formatted_date(sorted_)
#
#     transactions = group_card_numbers(formated)
#     # for transaction in transactions:
#     #     print(transaction)
#
#     mask_num = mask_numbers(transactions)
#     for i in mask_num:
#         print(i)
#
#     result = make_result(mask_num)

    # for i in fin:
    #     if 'from' in i:
    #         print(f'''
    # {i['date']} {i['description']}
    # {i['from'][0]} {i['from'][1]} -> {i['to'][0]} {i['to'][1]}''')
    #     else:
    #         print(f'''
    # {i['date']} {i['description']}
    # {i['to'][0]}  {i['to'][1]} ''')

# пример вывода одной операции
# 14.10.2018 Перевод организации
# Visa Platinum 7000 79** **** 6361 -> Счет **9638
# 82771.72 руб.