import json
from datetime import timedelta

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
from scipy import stats


def daterange(date1, date2):
    date1 = date1.replace(hour=0, minute=0, second=0, microsecond=0)
    date2 = date2.replace(hour=0, minute=0, second=0, microsecond=0)
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(days=n)

def plot_time_lime(account_id, total_df, end_date, alert_point=None):
    account_df = total_df[total_df['account_id'] == account_id][
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']]
    values_list = np.concatenate(account_df.values)
    values_list = values_list[np.logical_not(np.isnan(values_list))]
    init_date = end_date - timedelta(days=(len(values_list) - 1))
    dates_list = list(daterange(init_date, end_date))

    slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(values_list)), values_list)
    slope_line = slope * range(len(values_list)) + intercept

    time_series_trace = go.Scatter(x=dates_list, y=values_list, name='Saldo')
    slope_trace = go.Scatter(x=dates_list, y=slope_line, mode='lines', name='Pendiente')

    layout = dict(
        yaxis=dict(
            hoverformat='$,.2f'
        )
    )

    data = [time_series_trace, slope_trace]

    if alert_point is not None:
        alert_points = go.Scatter(x=[alert_point.date], y=[alert_point.new_value], mode='markers', name='Alertas')
        data.append(alert_points)

    fig = dict(data=data, layout=layout)
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return graph_json

