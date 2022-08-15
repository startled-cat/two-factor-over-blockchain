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
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]




def wei2gwei(n):
    return n / 1e9


def wei2ether(n):
    return n / 1e18


def plot_grouped_bar_chart_with_labels(labels, data, title, x_label, y_label, filename):
    plt.rcdefaults()
    
    fig, ax = plt.subplots()
    # increase margins around chart
    plt.subplots_adjust(top=0.95, left=0.25, right=0.85, bottom=0.15)
    # make chart wide
    fig.set_size_inches(7, 5)
    
    ax.grid(which="major", alpha=0.7, axis="x")

    
    y_pos = np.arange(len(labels))
    
    width = 0.7  # the width of the bars
    bar_width = width / len(data)  # the width of a single bar
    cell_text = []
    # reverse data list
    data.reverse()
    for i, d in enumerate(data):
        values = d['values']
        label = d['label']
        color = d['color']
        locations = y_pos #- (-width/2 + bar_width/2 + bar_width*i)
        # locations = y_pos - (-width/2 + bar_width/2 + bar_width*i)
        rectangle = ax.barh(locations, values, width,
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

    # ax.grid(which="major", alpha=0.7, axis="y")
    # ax.xaxis.set_major_formatter(
    #     lambda x, pos=None: f"{wei2gwei(x):,}"[:-2].replace(",", " "))
    
    plt.savefig(f"{script_path}/{filename}.svg")
    
    # save data that was plotted as a csv file
    with open(f"{script_path}/{filename}.csv", 'w') as f:
        f.write(f"network,type,value\n")
        for i, d in enumerate(data):
            values = d['values']
            label = d['label']
            for j, v in enumerate(values):
                f.write(f"{labels[j]},{label},{v}\n")

def make_chart_time_by_network():

    # for each network, calculate average cost for user and average cost for app
    networks_median_time = []
    network_names = []
    confirmations = 5

    for (network, data) in networks_data:
        median_time_all_confirmations = []
        for c in range(confirmations):
            confirmation_times = []
            for m in data:
                confirmation_times.append(m["user_time"][c])
                confirmation_times.append(m["app_time"][c])
            median_time = np.median(confirmation_times)
            median_time_all_confirmations.append(median_time)
            
        network_names.append(network_config[network]["name"])
        networks_median_time.append((median_time_all_confirmations))
        
    groups = []
    for c in range(confirmations):
        groups.append({
            "label": f"{c+1} {'blok' if c+1 == 1 else 'bloki' if c+1 < 5 else 'bloków'}",
            "color": plot_colors[c],
            "values": [d[c] for d in networks_median_time]
        })
        
    plot_grouped_bar_chart_with_labels(
        network_names, groups, "Mediana czasu potwierdzenia transakcji, dla kazdej sieci", "Siec", "Czas (s)", "avg_time_by_network")

    
def main():
    make_chart_time_by_network()


if __name__ == "__main__":
    main()
