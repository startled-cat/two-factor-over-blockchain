import numpy as np
import matplotlib.pyplot as plt
from parse_data import load_data
import math
from datetime import datetime

networks_data = load_data()


def wei2gwei(n):
    return n / 1e9

def wei2ether(n):
    return n / 1e18




# for each network, calculate average cost for user and average cost for app

networks_avg_cost = []
network_names = []

for (network, data) in networks_data:
    avg_cost_user = 0
    avg_cost_app = 0
    
    for m in data:
        avg_cost_user += m["user_cost"]
        avg_cost_app += m["app_cost"]
        
    avg_cost_user /= len(data)
    avg_cost_app /= len(data)
    
    network_names.append(network)
    networks_avg_cost.append((avg_cost_user, avg_cost_app))
    
# prepare data for chart
x = [i for i in range(0, len(networks_avg_cost))]
x_labels = network_names

y = [s[0] for s in networks_avg_cost]
y2 = [s[1] for s in networks_avg_cost]

# prepare chart
# plt.rcParams["figure.figsize"] = (8, 5)
fig, ax1 = plt.subplots()

plt.xticks(x, x_labels, rotation=90)

ax1.set_xlabel("network")

ax1.set_ylabel("user_cost", color="tab:red")
line1, = ax1.plot(x, y, color="tab:red", label="user_cost", marker="s", linestyle="dashed")
ax1.tick_params(axis="y", labelcolor="tab:red")
ax1.grid(which="major", alpha=0.7, axis="x")
ax1.grid(which="major", alpha=0.7, axis="y")
# display data points on chart
for i, txt in enumerate(y):
    ax1.annotate(round(wei2gwei(txt)), (x[i], y[i]))
    
ax1.yaxis.set_major_formatter(lambda x, pos=None: f"{wei2gwei(x):,}"[:-2].replace(",", " ")+" gwei")



ax2 = ax1.twinx()
ax2.set_ylabel("app_cost", color="tab:blue")
line2, = ax2.plot(x, y2, color="tab:blue", label="app_cost", marker="o")
ax2.tick_params(axis="y", labelcolor="tab:blue")
ax2.yaxis.set_major_formatter(lambda x, pos=None: f"{wei2gwei(x):,}"[:-2].replace(",", " ")+" gwei")

plt.title("średni koszt akceptacji transakcji dla różnych sieci")
plt.legend([line1, line2], ["user_cost", "app_cost"], loc="center right")
plt.show()

# def make_bar_chart(x_labels, y_values1, y)

