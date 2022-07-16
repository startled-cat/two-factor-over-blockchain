import json
import matplotlib.pyplot as plt
import numpy as np
import math

with open('../data/compilers_test.json') as f:
    stats = json.load(f)

    # filter data

    stats = list(filter(lambda x: x['solcVersion'] == "0.8.15", stats))
    # stats = list(filter(lambda x: x['solcOptimizerRuns'] == 0, stats))

    # prepare data

    x = [i for i in range(0, len(stats))]
    userGasUsed = [s["userGasUsed"] for s in stats]
    appGasUsed = [s["appGasUsed"] for s in stats]
    solcVersion = [s["solcVersion"] for s in stats]
    solcOptimizerRuns = [s["solcOptimizerRuns"] for s in stats]
    solcOptimizerRuns = list(
        map(lambda x: "none" if x is None else x, solcOptimizerRuns))
    contractDeployGasUsed = [s["contractDeployGasUsed"] for s in stats]

    totalGasUsed = [s["userGasUsed"]+s["appGasUsed"] for s in stats]

    # prepare chart
    fig, ax1 = plt.subplots()
    plt.xticks(x, solcOptimizerRuns, rotation=45)

    color = 'tab:red'
    ax1.set_xlabel('compiler optimization runs')
    ax1.set_ylabel('transaction gas used', color=color)
    ax1.plot(x, totalGasUsed, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    def formatter(x, pos=None):
        s = solcOptimizerRuns[x]
        if isinstance(s, str):
            return s

        return f"{solcOptimizerRuns[x]:,}"
    ax1.xaxis.set_major_formatter(formatter)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('contract deployment gas used', color=color)
    ax2.plot(x, contractDeployGasUsed, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()

    plt.title('usage of gas for transactions, depending of compiler settings')

    plt.legend()
    plt.show()
    # plt.savefig('compilers.test.svg', dpi=350)
    # plt.show()
