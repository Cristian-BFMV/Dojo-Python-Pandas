from calendar import monthrange

import numpy as np
import pandas as pd

from .. import logger

column_names = ['cod_bank','year','month','cod_office','account_currency','empty','last_month_balance','1','2','3',
                '4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24',
                '25','26','27','28','29','30','31','cod_date']

dtypes_dict = {0: np.dtype('int64'),
 1: np.dtype('int64'),
 2: np.dtype('int64'),
 3: np.dtype('int64'),
 4: np.dtype('int64'),
 5: np.dtype('O'),
 6: np.dtype('float64'),
 7: np.dtype('float64'),
 8: np.dtype('float64'),
 9: np.dtype('float64'),
 10: np.dtype('float64'),
 11: np.dtype('float64'),
 12: np.dtype('float64'),
 13: np.dtype('float64'),
 14: np.dtype('float64'),
 15: np.dtype('float64'),
 16: np.dtype('float64'),
 17: np.dtype('float64'),
 18: np.dtype('float64'),
 19: np.dtype('float64'),
 20: np.dtype('float64'),
 21: np.dtype('float64'),
 22: np.dtype('float64'),
 23: np.dtype('float64'),
 24: np.dtype('float64'),
 25: np.dtype('float64'),
 26: np.dtype('float64'),
 27: np.dtype('float64'),
 28: np.dtype('float64'),
 29: np.dtype('float64'),
 30: np.dtype('float64'),
 31: np.dtype('float64'),
 32: np.dtype('float64'),
 33: np.dtype('float64'),
 34: np.dtype('float64'),
 35: np.dtype('float64'),
 36: np.dtype('float64'),
 37: np.dtype('float64'),
 38: np.dtype('int64')}


def transform_month_data_frame(month_df):
    month_df.columns = column_names
    account_id = month_df.get('account_currency').astype(str).str[:-1].astype(np.int64)
    currency_type = month_df.get('account_currency').astype(str).str[-1].astype(np.int64)
    month_df.insert(loc=0, column="account_id", value=account_id)
    month_df.insert(loc=1, column="currency_type", value=currency_type)
    month_df = month_df.drop(columns="empty")

    month_df = month_df.apply(fill_days_na, axis=1)
    month_df[['account_id','currency_type','cod_bank','year','month','cod_office','account_currency', 'cod_date']] = \
        month_df[['account_id','currency_type','cod_bank','year','month','cod_office','account_currency',
                  'cod_date']].astype('int')

    return month_df

def fill_days_na(data):
    last_month_day = monthrange(int(data['year']), int(data['month']))[1]
    if last_month_day != 31:
        data[[str(i) for i in range(last_month_day + 1, 32)]] = np.nan
    return data


def process_balances_file(balances_file, file_type='monthly', selected_date=None, controls_to_run=None, params_control=None):
    valid_data = True
    message = ""
    balances_df = pd.DataFrame()
    try:
        balances_df = pd.read_csv(balances_file, index_col=None, header=None, sep='\t', dtype=dtypes_dict,
                                  na_filter=False)
    except Exception as e:
        print(e)
        logger.error(e)
        valid_data = False
        message = "Alguno de los datos en las columnas no es valido."
        logger.error(message)

    if valid_data and len(balances_df.columns) != 39:
        valid_data = False
        print("El archivo no tiene todas las columnas requeridas")

    if valid_data:
        transform_month_data_frame(balances_df)
        duplicate_rows_df = balances_df[balances_df.duplicated(['account_id'])]
        balances_df.drop_duplicates(subset="account_id", keep=False, inplace=True)
        print("***+****************balances_df")
        print(balances_df)
        duplicate = balances_df.groupby("account_id", as_index=False)
        print("***+****************duplicate")
        print(duplicate)
        sum_dataframe = duplicate.sum()
        print("***+****************sum_dataframe")
        print(sum_dataframe)
        return balances_df

    else:
        return balances_df
