from unittest import TestCase
from calculate_valuation_data import calculate_valuation_data
import pandas as pd


class Test(TestCase):
    def test_empty_data(self):
        match_data = {
            "matching_id": [],
            "top_priced_count": []
        }

        test_data = {
            "id": [],
            "price": [],
            "currency": [],
            "quantity": [],
            "matching_id": []
        }

        currencies_data = {
            "currency": [],
            "ratio": []
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                 pd.DataFrame(match_data))
        if not data_to_file.empty:
            print("output: \n", data_to_file)
            self.fail('return is not empty')

    def test_one_data(self):
        match_data = {
            "matching_id": [1],
            "top_priced_count": [1]
        }

        test_data = {
            "id": [1],
            "price": [10],
            "currency": ['PLN'],
            "quantity": [1],
            "matching_id": [1]
        }

        currencies_data = {
            "currency": ['PLN'],
            "ratio": [1]
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                 pd.DataFrame(match_data))

        output = {
            "matching_id": [1],
            "total_price": [10.0],
            "avg_price": [10.0],
            "currency": ['PLN'],
            "ignored_products_count": [0]
        }

        expect = pd.DataFrame(output)
        if not (data_to_file.compare(expect)).empty:
            print("expected: \n", expect)
            print("got: \n", data_to_file)
            self.fail('output and input are different')

    def test_no_matching_id_data(self):
        match_data = {
            "matching_id": [2],
            "top_priced_count": [1]
        }
        test_data = {
            "id": [1],
            "price": [10],
            "currency": ['PLN'],
            "quantity": [1],
            "matching_id": [1]
        }
        currencies_data = {
            "currency": ['PLN'],
            "ratio": [1]
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                pd.DataFrame(match_data))
        output = {
            "matching_id": [2],
            "total_price": [0.0],
            "avg_price": [0],
            "currency": ['PLN'],
            "ignored_products_count": [0]
        }
        expect = pd.DataFrame(output)
        if not (data_to_file.compare(expect)).empty:
            print("expected:\n", expect)
            print("got: \n", data_to_file)
            self.fail('output and input are different')

    def test_too_much_quantity_data(self):
        match_data = {
            "matching_id": [1],
            "top_priced_count": [12]
        }
        test_data = {
            "id": [1],
            "price": [10],
            "currency": ['PLN'],
            "quantity": [1],
            "matching_id": [1]
        }
        currencies_data = {
            "currency": ['PLN'],
            "ratio": [1]
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                pd.DataFrame(match_data))
        output = {
            "matching_id": [1],
            "total_price": [0],
            "avg_price": [0],
            "currency": ['PLN'],
            "ignored_products_count": [0]
        }
        expect = pd.DataFrame(output)
        if not (data_to_file.compare(expect)).empty:
            print("expected: ", expect)
            print("got: ", data_to_file)
            self.fail('output and input are different')

    def test_split_quantity_data(self):
        match_data = {
            "matching_id": [1],
            "top_priced_count": [5]
        }
        test_data = {
            "id": [1, 2, 3, 4, 5],
            "price": [10, 3, 5, 6, 12],
            "currency": ['PLN', 'PLN', 'PLN', 'PLN', 'PLN'],
            "quantity": [1, 2, 3, 4, 3],
            "matching_id": [1, 2, 1, 2, 1]
        }
        currencies_data = {
            "currency": ['PLN'],
            "ratio": [1]
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                pd.DataFrame(match_data))
        output = {
            "matching_id": [1],
            "total_price": [51.0],
            "avg_price": 10.2,
            "currency": ['PLN'],
            "ignored_products_count": [2]
        }
        expect = pd.DataFrame(output)
        if not (data_to_file.compare(expect)).empty:
            print("expected: ", expect)
            print("got: ", data_to_file)
            self.fail('output and input are different')

    def test_split_quantity_too_much_data(self):
        match_data = {
            "matching_id": [1],
            "top_priced_count": [5]
        }
        test_data = {
            "id": [1, 2, 3, 4, 5],
            "price": [10, 3, 5, 6, 12],
            "currency": ['PLN', 'PLN', 'PLN', 'PLN', 'PLN'],
            "quantity": [1, 2, 2, 4, 1],
            "matching_id": [1, 2, 1, 2, 1]
        }
        currencies_data = {
            "currency": ['PLN'],
            "ratio": [1]
        }
        data_to_file = calculate_valuation_data(pd.DataFrame(test_data), pd.DataFrame(currencies_data),
                                                pd.DataFrame(match_data))
        output = {
            "matching_id": [1],
            "total_price": [0],
            "avg_price": [0],
            "currency": ['PLN'],
            "ignored_products_count": [0]
        }
        expect = pd.DataFrame(output)
        if not (data_to_file.compare(expect)).empty:
            print("expected: ", expect)
            print("got: ", data_to_file)
            self.fail('output and input are different')