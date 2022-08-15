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


def make_chart_cost(network_name, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.9, left=0.1, right=0.95, bottom=0.15)
    fig.set_size_inches(8, 5)

    # draw line chart
    ax.plot(data['date'], data['user_cost'], color=plot_colors[0],
            label="Koszt użytkownika (GiveAccess)")
    ax.plot(data['date'], data['app_cost'], color=plot_colors[1],
            label="Koszt aplikacji (ReceiveAccess)")

    # set title and labels
    ax.legend(loc="upper right")
    ax.grid(which="major", alpha=0.7, axis="x")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
    # set max y-axis value to triple the average cost
    ax.set_ylim(0, 3 * np.median(data['user_cost']))


    # rotate x-axis labels  and set date format
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
    plt.xticks(rotation=45)

    ax.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))

    # plt.show()
    # save chart
    plt.savefig(filename)
    
    plt.close(fig)


def make_chart_time(network_name, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.9, left=0.1, right=0.95, bottom=0.15)
    fig.set_size_inches(8, 5)

    # draw line chart
    ax.plot(data['date'], data['time2'],
            color=plot_colors[0], label="Czas 2 potwierdzen")
    ax.plot(data['date'], data['time5'],
            color=plot_colors[1], label="Czas 5 potwierdzen")

    # set title and labels
    ax.legend(loc="upper right")
    ax.grid(which="major", alpha=0.7, axis="x")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
    
    # set max y-axis so that all values are visible
    ax.set_ylim(0, 1.5 * max(sorted(data['time5'])[5:-6]))

    # rotate x-axis labels  and set date format
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

    for (name, data) in networks_data:
        print("Generating charts for", name)
        save_path_network = os.path.join(script_path, name)
        # create directory if it doesn't exist
        if not os.path.exists(save_path_network):
            os.makedirs(save_path_network)
            
        # convert cost to gwei
        for e in data:
            e['user_cost_eth'] = wei2gwei(e['user_cost_eth'])
            e['app_cost_eth'] = wei2gwei(e['app_cost_eth'])
        
        # prepare data
        data_cost = sorted(data, key=lambda x: x['timestamp'])
        # define dataframes
        data_cost = pd.DataFrame({
            'date': [datetime.datetime.fromtimestamp(d['timestamp']) for d in data_cost],
            'user_cost': [d['user_cost_eth'] for d in data_cost],
            'app_cost': [d['app_cost_eth'] for d in data_cost]
        })
        # save dataframe as csv
        data_cost.to_csv(os.path.join(
            save_path_network, "cost_over_time_%s.csv" % name), index=False)

        # make chart
        chart_filepath = os.path.join(save_path_network, "cost_over_time_%s.svg" % name)
        make_chart_cost(name, data_cost, title=f"Koszt transakcji dla sieci '{network_config[name]['name']}'",
                        x_label="Data", y_label="Koszt (gwei ETH)", filename=chart_filepath)

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

        # save dataframe as csv
        data_time.to_csv(os.path.join(
            save_path_network, "time_over_time_%s.csv" % name), index=False)
        chart_filepath = os.path.join(save_path_network, "time_over_time_%s.svg" % name)
        make_chart_time(
            name, data_time, title=f"Czas do uzyskania potwierdzen transakcji dla sieci '{network_config[name]['name']}'", x_label="Data", y_label="Czas (s)", filename=chart_filepath)

        


if __name__ == "__main__":
    main()
