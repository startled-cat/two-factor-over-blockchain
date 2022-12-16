from statistics import mean, stdev
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from parse_data import load_data
import math
from datetime import datetime
import os
from network_config import network_config
import pandas as pd
import datetime
import scipy.stats as stats

TIMEFRAME_24H = False
FILENAME_POSTFIX = '24h' if TIMEFRAME_24H else '7d'
MAKE_CHART_COST = False
MAKE_CHART_TIME = False

networks_data = load_data()

script_path = os.path.dirname(os.path.realpath(__file__))
save_path = os.path.join(script_path, "cost_over_time")
# create directory if it doesn't exist
if not os.path.exists(save_path):
    os.makedirs(save_path)


# list of nice, readable, aesthetic colors, that can be used in plots
plot_colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]


def wei2gwei(n):
    return n / 1e9


def wei2ether(n):
    return n / 1e18


"""
https://www.statology.org/remove-outliers-python/
"""


def remove_outliers(data):
    z = stats.zscore(data)
    data_clean = [data[i] for i in range(len(data)) if abs(z[i]) < 3]
    if len(data_clean) > 0:
        return data_clean
    else:
        if stdev(data) == 0:
            return data
        return []


def variance(data):
    r = (
        data['time1'].var(),
        data['time2'].var(),
        data['time3'].var(),
        data['time4'].var(),
        data['time5'].var())
    return r


def make_chart_cost(network_name, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.9, left=0.20, right=0.95, bottom=0.15)
    if TIMEFRAME_24H:
        fig.set_size_inches(4.5, 3)
    else:
        fig.set_size_inches(8, 4)

    # draw line chart
    ax.plot(data['date'], data['user_cost'], color=plot_colors[0],
            label="Koszt użytkownika (createToken)")
    ax.plot(data['date'], data['app_cost'], color=plot_colors[1],
            label="Koszt aplikacji (receiveToken)")

    # set title and labels
    ax.legend(loc="upper right")
    ax.grid(which="major", alpha=0.7, axis="x")
    ax.grid(which="major", alpha=0.7, axis="y")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # set max y-axis value to triple the average cost
    if TIMEFRAME_24H:
        ax.set_ylim(0, 3 * np.median(data['user_cost']))

    # rotate x-axis labels  and set date format

    if TIMEFRAME_24H:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%-H"))
    else:
        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
        plt.xticks(rotation=45)

    ax.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))

    if network_name == 'harmony-devnet':
        ax.yaxis.set_major_formatter(
            lambda x, pos=None: f"{x:.2f}")
    if network_name == 'optimism-test':
        ax.yaxis.set_major_formatter(
            lambda x, pos=None: f"{x:.4f}")

    # plt.show()
    # save chart
    plt.savefig(filename)

    plt.close(fig)


def make_chart_time(network_name, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    if TIMEFRAME_24H:
        plt.subplots_adjust(top=0.9, left=0.13, right=0.95, bottom=0.15)
        fig.set_size_inches(4.5, 3)
    else:
        plt.subplots_adjust(top=0.9, left=0.12, right=0.95, bottom=0.15)
        fig.set_size_inches(8, 4)

    # draw line chart
    ax.plot(data['date'], data['time2'],
            color=plot_colors[0], label="Czas 2 potwierdzen")
    ax.plot(data['date'], data['time5'],
            color=plot_colors[1], label="Czas 5 potwierdzen")

    # set title and labels
    ax.legend(loc="upper right")
    ax.grid(which="major", alpha=0.7, axis="x")
    ax.grid(which="major", alpha=0.7, axis="y")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # set max y-axis so that all values are visible
    if TIMEFRAME_24H:
        ax.set_ylim(0, 1.5 * max(sorted(data['time5'])[5:-6]))

    # rotate x-axis labels  and set date format
    if TIMEFRAME_24H:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%-H"))
    else:
        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
        plt.xticks(rotation=45)

    # ax.yaxis.set_major_formatter(
    #     lambda x, pos=None: f"{wei2gwei(x):,}"[:-2].replace(",", " "))

    # save chart
    # plt.show()
    plt.savefig(filename)
    plt.close(fig)


def main():

    x_label = "Data" if not TIMEFRAME_24H else "Godzina"

    variance_test = {}

    for (name, data) in networks_data:
        # if name != 'rinkeby':
        #     continue
        
        print("Generating charts for", name)
        save_path_network = os.path.join(script_path, name)
        # create directory if it doesn't exist
        if not os.path.exists(save_path_network):
            os.makedirs(save_path_network)

        eth_unit = "Gwei"  # if name not in ['optimism-test'] else "Wei"

        # convert cost to gwei
        if eth_unit == "Gwei":
            for e in data:
                e['user_cost_eth'] = wei2gwei(e['user_cost_eth'])
                e['app_cost_eth'] = wei2gwei(e['app_cost_eth'])

        if TIMEFRAME_24H:
            for x in data:
                # remvoe date from timestamp
                x['datetime'] = f"2022-07-31T{x['datetime'][11:]}"
                x['timestamp'] = int(datetime.datetime.strptime(
                    x['datetime'], '%Y-%m-%dT%H:%M:%S.%f').timestamp())
            # aggregate data by hour
            new_data = []
            fields_to_average = ['user_gas_used', 'user_gas_price', 'user_cost', 'app_gas_used',
                                 'app_gas_price', 'app_cost', 'user_cost_eth', 'user_gas_price_eth',
                                 'app_cost_eth', 'app_gas_price_eth']
            for hour in range(0, 24):
                data_in_hour = list(filter(lambda x: int(
                    x['datetime'][11:13]) == hour, data))
                new_entry = dict(data_in_hour[0])

                for i in range(new_entry['confirmations']):
                    user_times = remove_outliers(
                        [x['user_time'][i] for x in data_in_hour])
                    app_times = remove_outliers(
                        [x['app_time'][i] for x in data_in_hour])

                    new_entry['user_time'][i] = mean(user_times)
                    new_entry['app_time'][i] = mean(app_times)

                for field in fields_to_average:
                    new_entry[field] = mean(remove_outliers(
                        [x[field] for x in data_in_hour]))

                new_data.append(new_entry)

            data = new_data

        # prepare data
        data_cost = sorted(data, key=lambda x: x['timestamp'])
        # define dataframes
        data_cost = pd.DataFrame({
            'date': [datetime.datetime.fromtimestamp(d['timestamp']) for d in data_cost],
            'user_cost': [d['user_cost_eth'] for d in data_cost],
            'app_cost': [d['app_cost_eth'] for d in data_cost]
        })
        
        

        if MAKE_CHART_COST:

            # save dataframe as csv
            data_cost.to_csv(os.path.join(
                save_path_network, f"cost_over_time_{name}_{FILENAME_POSTFIX}.csv"), index=False)

            # make chart
            chart_filepath = os.path.join(
                save_path_network, f"cost_over_time_{name}_{FILENAME_POSTFIX}.svg")

            make_chart_cost(name, data_cost, title=f"Koszt transakcji dla sieci '{network_config[name]['name']}'",
                            x_label=x_label, y_label=f"Koszt ({eth_unit} ETH)", filename=chart_filepath)

        # prepare data for confimration time
        data_time = sorted(data, key=lambda x: x['timestamp'])
        # data_time = [{'timestamp': datetime.datetime.fromtimestamp(d['timestamp']), 'time2': d['user_time'][1] + d['app_time'][1],} for d in data]

        # define dataframes
        data_time = pd.DataFrame({
            'date': [datetime.datetime.fromtimestamp(d['timestamp']) for d in data_time],
            'time1': [(d['user_time'][0] + d['app_time'][0])/2 for d in data_time],
            'time2': [(d['user_time'][1] + d['app_time'][1])/2 for d in data_time],
            'time3': [(d['user_time'][2] + d['app_time'][2])/2 for d in data_time],
            'time4': [(d['user_time'][3] + d['app_time'][3])/2 for d in data_time],
            'time5': [(d['user_time'][4] + d['app_time'][4])/2 for d in data_time],
        })
        
        # if name == 'rinkeby':
        #     data_time = data_time[data_time['time5'] < 100]

        variance_test[network_config[name]['name']] = variance(data_time)

        if MAKE_CHART_TIME:
            # save dataframe as csv
            data_time.to_csv(os.path.join(
                save_path_network, f"time_over_time_{name}_{FILENAME_POSTFIX}.csv"), index=False)
            chart_filepath = os.path.join(
                save_path_network, f"time_over_time_{name}_{FILENAME_POSTFIX}.svg")
            make_chart_time(
                name, data_time, title=f"Czas potwierdzeń dla sieci '{network_config[name]['name']}'", x_label=x_label, y_label="Czas (s)", filename=chart_filepath)

    variance_pd = pd.DataFrame({
        'name': variance_test.keys(),
        'variance_1': [x[0] for x in variance_test.values()],
        'variance_2': [x[1] for x in variance_test.values()],
        'variance_3': [x[2] for x in variance_test.values()],
        'variance_4': [x[3] for x in variance_test.values()],
        'variance_5': [x[4] for x in variance_test.values()]
    })
    variance_pd['average'] = variance_pd.mean(numeric_only=True, axis=1)

    # variance_pd = variance_pd.sort_values('variance_5')
    variance_pd.to_csv(os.path.join(script_path, "variance-time.csv"), index=False)
    print(variance_pd)


if __name__ == "__main__":
    main()
