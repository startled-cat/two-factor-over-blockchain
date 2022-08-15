import numpy as np
import matplotlib.pyplot as plt
from parse_data import load_data
import math
from datetime import datetime
import os
from network_config import network_config
networks_data = load_data()

script_path = os.path.dirname(os.path.realpath(__file__))

# list of nice, readable, aesthetic colors, that can be used in plots 
plot_colors = [
    '#1f77b4',  # muted blue
    '#bcbd22',  # curry yellow-green
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#17becf'   # blue-teal
]




def wei2gwei(n):
    return n / 1e9


def wei2ether(n):
    return n / 1e18


def plot_grouped_bar_chart_with_labels(labels, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    
    fig, ax = plt.subplots()
    # increase margins around chart
    plt.subplots_adjust(top=0.9, left=0.3, right=0.95, bottom=0.15)
    # make chart wide
    fig.set_size_inches(8, 5)
    
    y_pos = np.arange(len(labels))
    
    width = 0.6  # the width of the bars
    bar_width = width / len(data)  # the width of a single bar
    cell_text = []
    for i, d in enumerate(data):
        values = d['values']
        label = d['label']
        color = d['color']
        locations = y_pos + (-width/2 + bar_width/2 + bar_width*i)
        rectangle = ax.barh(locations, values, bar_width,
                           label=label, color=color)
        
    ax.set_yticks(y_pos, labels)
    # ax.invert_axis()
    ax.set_xlabel(y_label)
    # ax.set_ylabel(y_label)
    ax.set_title(title)

    # plt.xticks(rotation=45)
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    ax.legend()

    # ax.grid(which="major", alpha=0.7, axis="x")
    # ax.grid(which="major", alpha=0.7, axis="y")
    ax.xaxis.set_major_formatter(
        lambda x, pos=None: f"{wei2gwei(x):,}"[:-2].replace(",", " "))
    
    plt.savefig(f"{script_path}/{filename}.svg")
    
    # save data that was plotted as a csv file
    with open(f"{script_path}/{filename}.csv", 'w') as f:
        f.write(f"network,type,value\n")
        for i, d in enumerate(data):
            values = d['values']
            label = d['label']
            for j, v in enumerate(values):
                f.write(f"{labels[j]},{label},{v}\n")


def make_chart_cost_by_network():
    # for each network, calculate average cost for user and average cost for app

    networks_avg_cost = []
    network_names = []

    for (network, data) in networks_data:
        avg_cost_user = 0
        avg_cost_app = 0

        for m in data:
            avg_cost_user += m["user_cost_eth"]
            avg_cost_app += m["app_cost_eth"]

        avg_cost_user /= len(data)
        avg_cost_app /= len(data)

        network_names.append(network_config[network]["name"])
        networks_avg_cost.append((avg_cost_user, avg_cost_app))

    groups = [
        {
            "label": "GiveAccess",
            "color": plot_colors[0],
            "values": [avg_cost_user for avg_cost_user, avg_cost_app in networks_avg_cost]
        },
        {
            "label": "ReceiveAccess",
            "color": plot_colors[1],
            "values": [avg_cost_app for avg_cost_user, avg_cost_app in networks_avg_cost]
        }
    ]
    plot_grouped_bar_chart_with_labels(
        network_names, groups, "Sredni koszt wywolania metod kontraktu, dla kazdej sieci", "Siec", "Koszt (gwei ETH)", "avg_cost_by_network")


def main():
    make_chart_cost_by_network()


if __name__ == "__main__":
    main()
