import os
from config import ROOT_DIR
from src.utils import load_data, executed_transactions, sorts_date, formatted_date, group_card_numbers, mask_numbers, \
    make_result

path = os.path.join(ROOT_DIR)
file_name = 'test_operations.json'
os_path = os.path.join(path, 'tests', file_name)


def test_load_data():
    expected = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]

    assert load_data(os_path) == expected


def test_executed_transactions():
    data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 441945886,
            "state": "CANCELED",
        }
    ]

    expected = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 441945886,
            "state": "EXECUTED",
        }
    ]
    assert executed_transactions(data) == expected

    data_1 = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 441945886,
            "state": "EXECUTED",
        }
    ]

    expected_1 = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 441945886,
            "state": "EXECUTED",
        }
    ]
    assert executed_transactions(data) == expected


def test_sorts_date():
    data = [
        {
            "date": "2016-08-12T21:27:25.241689",
        },
        {
            "date": "2018-07-12T21:27:25.241689",
        },
        {
            "date": "2016-09-12T21:27:25.241689",
        }
    ]

    expected = [
        {
            "date": "2018-07-12T21:27:25.241689",
        },
        {
            "date": "2016-09-12T21:27:25.241689",
        },
        {
            "date": "2016-08-12T21:27:25.241689",
        }
    ]
    assert sorts_date(data) == expected


def test_formatted_date():
    data = [
        {
            "date": "2016-08-12T21:27:25.241689",
        },
        {
            "date": "2018-07-12T21:27:25.241689",
        },
        {
            "date": "2016-09-12T21:27:25.241689",
        }
    ]

    expected = [
        {
            "date": "12.08.2016",
        },
        {
            "date": "12.07.2018",
        },
        {
            "date": "12.09.2016",
        }
    ]
    assert formatted_date(data) == expected


def test_group_card_numbers():
    data = [
        {
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
        {
            "from": "Счет 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
        {
            "description": "Открытие вклада",
            "to": "Счет 96231448929365202391"
        },

    ]

    expected = [
        {
            "from": ['Visa Platinum', '1246 3773 7634 3588'],
            "to": ['Счет', '1421 1924 1444 2603 1657']
        },
        {
            "from": ['Счет', '1246 3773 7634 3588'],
            "to": ['Счет', '1421 1924 1444 2603 1657']
        },
        {
            "description": "Открытие вклада",
            "to": ['Счет', '9623 1448 9293 6520 2391']
        },

    ]

    assert group_card_numbers(data) == expected


def test_mask_numbers():
    data = [
        {
            "from": ['Visa Platinum', '1246 3773 7634 3588'],
            "to": ['Счет', '1421 1924 1444 2603 1657']
        },
        {
            "from": ['Счет', '1246 3773 7634 3588'],
            "to": ['Счет', '1421 1924 1444 2603 1657']
        },
        {
            "description": "Открытие вклада",
            "to": ['Счет', '9623 1448 9293 6520 2391']
        },

    ]

    expected = [
        {
            "from": ['Visa Platinum', '1246 37** **** 3588'],
            "to": ['Счет', '**1657']
        },
        {
            "from": ['Счет', '**3588'],
            "to": ['Счет', '**1657']
        },
        {
            "description": "Открытие вклада",
            "to": ['Счет', '**2391']
        },

    ]
    assert mask_numbers(data) == expected

    data_1 = [
        {
            "from": ['Visa Platinum', '1246 3773 7634 3588'],
            "to": ['Visa Platinum', '1246 3773 7634 3588']
        },
        {
            "from": ['Счет', '1246 3773 7634 3588'],
            "to": ['Счет', '1421 1924 1444 2603 1657']
        },
        {
            "description": "Открытие вклада",
            "to": ['Счет', '9623 1448 9293 6520 2391']
        },

    ]

    expected_2 = [
        {
            "from": ['Visa Platinum', '1246 37** **** 3588'],
            "to": ['Visa Platinum', '1246 37** **** 3588']
        },
        {
            "from": ['Счет', '**3588'],
            "to": ['Счет', '**1657']
        },
        {
            "description": "Открытие вклада",
            "to": ['Счет', '**2391']
        },

    ]
    assert mask_numbers(data_1) == expected_2
