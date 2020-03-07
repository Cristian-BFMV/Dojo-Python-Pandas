import pandas as pd
from flask import g


class InitData:

    total_df_dict = {}
    general_average_df_dict = {}
    accounts_alerts_dict = {}
    accounts_criticality_dict = {}
    table_name_prefix = ""

    def __init__(self):
        self._total_df = pd.DataFrame()
        self._general_average_df = pd.DataFrame()
        self._accounts_alerts = pd.DataFrame()
        self._accounts_criticality = pd.DataFrame()

    # function to get value of _total_df
    def get_total_df(self):
        if g.environment == 'auth':
            return None
        return self.total_df_dict[g.environment]

    def load_accounts_data(self, environment, df):
        self.total_df_dict[environment] = df

        # function to set value of _total_df

    def set_total_df(self, t):
        self._total_df = t

        # function to delete _total_df attribute

    def del_total_df(self):
        del self._total_df


