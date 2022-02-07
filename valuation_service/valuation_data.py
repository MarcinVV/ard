from calculate_valuation_data import calculate_valuation_data
import pandas as pd
import os



def valuation_data(data_file_name, currencies_file_name, matchings_file_name, file_to_save_name):
    try:
        data_file = pd.read_csv(data_file_name)
        currencies_file = pd.read_csv(currencies_file_name)
        matchings_file = pd.read_csv(matchings_file_name)
    except FileNotFoundError as e:
        print(e.errno)
        raise

    data_to_file = calculate_valuation_data(data_file, currencies_file, matchings_file)
    print(data_to_file)
    if not os.path.exists(file_to_save_name):
        data_to_file.to_csv(file_to_save_name)
    else:
        raise Exception("Output file exist", file_to_save_name)



