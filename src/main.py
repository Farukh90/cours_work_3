import os
from utils import load_data, executed_transactions, sorts_date, formatted_date, \
    group_card_numbers, \
    mask_numbers, make_result
from config import ROOT_DIR

path = os.path.join(ROOT_DIR, 'src')
file_name = 'operations.json'
os_path = os.path.join(path, file_name)


def main():
    transactions = load_data(os_path)

    execute_transactions = executed_transactions(transactions)

    sorted_date = sorts_date(execute_transactions)

    format_date = formatted_date(sorted_date)

    group_by_4 = group_card_numbers(format_date)

    masked_numbers = mask_numbers(group_by_4)

    result = make_result(masked_numbers)


if __name__ == "__main__":
    main()