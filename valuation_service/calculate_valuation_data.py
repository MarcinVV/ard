import pandas as pd


def calculate_valuation_data(data_file, currencies_file, matchings_file):
    ignored_products_count_list = []
    avg_price_list = []
    total_price_list = []
    matching_id_list = []
    currency = []

    for index, row in data_file.iterrows():
        data_file.loc[index, 'price_pln'] = (row['price'] * currencies_file[currencies_file['currency']
                                                                            == row['currency']].ratio).squeeze()

    for index, row in matchings_file.iterrows():
        # prepare data to calculation
        # create price_pln column with price and add sort data by price
        sorted_data_file = data_file[data_file['matching_id'] == row['matching_id']].sort_values('price_pln',
                                                                                                 ascending=False)
        # add quantity of item in each column
        sorted_data_file['sum'] = sorted_data_file.quantity.cumsum()
        # calculate total price
        total_price = 0
        top_priced_count = row['top_priced_count']
        for indexS, rowS in sorted_data_file.iterrows():
            top_priced_count = top_priced_count - rowS['quantity']

            if rowS['sum'] >= row['top_priced_count']:
                if top_priced_count:
                    total_price = total_price + ((rowS['quantity'] + top_priced_count) * rowS['price_pln'])
                    break
                else:
                    total_price = total_price + (rowS['quantity'] * rowS['price_pln'])
                    break

            total_price = total_price + rowS['quantity'] * rowS['price_pln']

        # compute ignore products
        ignored_items = sorted_data_file['quantity'].sum() - row['top_priced_count']

        # add output to lists
        matching_id_list.append(row['matching_id'])
        total_price_list.append(total_price if ignored_items >= 0 else 0)
        avg_price_list.append(total_price / row['top_priced_count'] if ignored_items >= 0 else 0)
        currency.append('PLN')
        ignored_products_count_list.append(ignored_items if ignored_items > 0 else 0)

    # prepare output data
    output_data = {
        'matching_id': matching_id_list,
        'total_price': total_price_list,
        'avg_price': avg_price_list,
        'currency': currency,
        'ignored_products_count': ignored_products_count_list
    }
    df_output_data = pd.DataFrame(output_data)
    return df_output_data
