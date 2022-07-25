from tinydb import TinyDB, Query
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime

def main():
    data = load_data()
    
    # prepare data for chart
    x = [i for i in range(0, len(data))]
    x_labels = [s["timestamp"] for s in data]
    # format timestamps to  datetime
    x_labels = [datetime.fromtimestamp(int(s)).strftime('%y-%m-%d %H:%M:%S') for s in x_labels]
    
    
    user_times = [s["user_time"] for s in data]
    app_times = [s["app_time"] for s in data]
    
    confirmations = 2
    
    user_times = [s[confirmations-1] for s in user_times]
    app_times = [s[confirmations-1] for s in app_times]
    
    #prepare chart
    plt.rcParams["figure.figsize"] = (8, 5)
    fig, ax1 = plt.subplots()

    fig.tight_layout()
    plt.xticks(x, x_labels, rotation=90)
    plt.subplots_adjust(top=0.9, left=0.15, right=0.85, bottom=0.25)

    color1 = "tab:red"
    color2 = "tab:blue"
    label1 = "user_times"
    label2 = "app_times"

    ax1.set_xlabel(
        f"data")
    ax1.set_ylabel(label1, color=color1)
    line1, = ax1.plot(x, user_times, color=color1,
                      label=label1, marker="s", linestyle="dashed")
    ax1.tick_params(axis="y", labelcolor=color1)
    # ax1.xaxis.set_major_formatter(formatter)
    ax1.grid(which="major", alpha=0.7, axis="x")
    ax1.grid(which="major", alpha=0.7, axis="y")
    ax1.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2, color=color2)
    line2, = ax2.plot(x, app_times, color=color2,
                      label=label2, marker="o")
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))

    plt.title(
        f"czas akceptacji transacji dla {confirmations} potwierdzeń")

    plt.legend([line1, line2], [label1, label2], loc='center right')

    plt.show()

        
    
def load_data():
    db_path = "data/benchmark/xdai-test_36_220724-1718.json"
    r = []
    with TinyDB(db_path) as db:
        Result = Query()
        r = db.search(Result.network == "xdai-test")
    return r

if __name__ == "__main__":
    main()