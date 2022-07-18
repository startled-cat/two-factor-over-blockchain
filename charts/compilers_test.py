import json
import matplotlib.pyplot as plt
import numpy as np
import math


def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def chart_optimization_runs(data_path=None, show=False, save_as=None):

    # stats = load_data("../data/compilers_test_old.json")
    # stats = list(filter(lambda x: x["solcVersion"] == "0.8.15", stats))
    stats = load_data(data_path)
    stats = list(filter(lambda x: x["solcOptimizerRuns"] is not None, stats))

    solc_version = stats[0]["solcVersion"]

    # prepare data
    x = [i for i in range(0, len(stats))]
    solc_optimizer_runs = ["Brak" if s["solcOptimizerRuns"]
                           is None else s["solcOptimizerRuns"] for s in stats]
    deployment_gas_used = [s["contractDeployGasUsed"] for s in stats]
    tx_gas_used = [s["userGasUsed"]+s["appGasUsed"] for s in stats]

    def formatter(x, pos=None):
        return f"{solc_optimizer_runs[math.floor(x)]:,}".replace(",", " ")

    # prepare chart
    plt.rcParams["figure.figsize"] = (8, 5)
    fig, ax1 = plt.subplots()

    fig.tight_layout()
    plt.xticks(x, solc_optimizer_runs, rotation=90)
    plt.subplots_adjust(top=0.9, left=0.15, right=0.85, bottom=0.25)

    color1 = "tab:red"
    color2 = "tab:blue"
    label1 = "gas na wykonanie transakcji"
    label2 = "gas na wdrożenie kontraktu"

    ax1.set_xlabel(
        f"Wartość parametru \"Optimization runs\"")
    ax1.set_ylabel(label1, color=color1)
    line1, = ax1.plot(x, tx_gas_used, color=color1,
                      label=label1, marker="s", linestyle="dashed")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.grid(which="major", alpha=0.7, axis="x")
    ax1.grid(which="major", alpha=0.7, axis="y")
    ax1.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2, color=color2)
    line2, = ax2.plot(x, deployment_gas_used, color=color2,
                      label=label2, marker="o")
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))

    plt.title(
        f"Zapotrzebowanie na gas, zależnie od parametru \"Optimization runs\" \ndla kompilatora solc w wersji {solc_version}")

    plt.legend([line1, line2], [label1, label2], loc='center right')

    if show:
        plt.show()

    if save_as is not None:
        plt.savefig(save_as, dpi=350)


def chart_compiler_versions(show=False, save_as=None):
    stats = load_data("../data/compare_compiler_versions.json")

    optimization_runs = stats[0]["solcOptimizerRuns"]
    # prepare data
    x = [i for i in range(0, len(stats))]
    solc_version = [s["solcVersion"] for s in stats]
    deployment_gas_used = [s["contractDeployGasUsed"] for s in stats]
    tx_gas_used = [s["userGasUsed"]+s["appGasUsed"] for s in stats]

    # prepare chart
    plt.rcParams["figure.figsize"] = (14, 4)

    fig, ax1 = plt.subplots()
    fig.tight_layout()
    plt.xticks(x, solc_version, rotation=90)
    plt.subplots_adjust(top=0.9, left=0.08, right=0.9, bottom=0.25)

    color1 = "tab:red"
    label1 = "gas na wykonanie transakcji"
    ax1.set_xlabel(
        f"Wersja kompilatora Solidity")
    line1, = ax1.plot(x, tx_gas_used, color=color1, linestyle="dashed",
                      label=label1, marker="s")
    ax1.set_ylabel(label1, color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "tab:blue"
    label2 = "gas na wdrożenie kontraktu"
    ax2.set_ylabel(label2, color=color2)
    line2, = ax2.plot(x, deployment_gas_used, color=color2,
                      label=label2, marker="o")
    ax2.tick_params(axis="y", labelcolor=color2)

    # add grid to chart
    # ax1.grid(which="major")
    ax1.grid(which="major", alpha=0.7, axis="x")
    ax1.grid(which="major", alpha=0.7, axis="y")

    ax1.xaxis.set_major_formatter(lambda x, pos=None: solc_version[round(x)])
    ax1.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))
    ax2.yaxis.set_major_formatter(
        lambda x, pos=None: f"{x:,}"[:-2].replace(",", " "))

    plt.title(
        f"Zapotrzebowanie na gas, zależne od wersji kompilatora solc (\"Optimization runs\" : {optimization_runs})")

    ax1.legend([line1, line2], [label1, label2], loc='center left')

    if show:
        plt.show()

    if save_as is not None:
        plt.savefig(save_as, dpi=350)


def main():
    chart_optimization_runs(
        data_path="../data/compare_compiler_optimizations_1.json",
        show=False,
        save_as="images/compilers_optimization_1.svg")

    chart_optimization_runs(
        data_path="../data/compare_compiler_optimizations_2.json",
        show=False,
        save_as="images/compilers_optimization_2.svg")

    chart_compiler_versions(
        show=False,
        save_as="images/compilers_versions.svg")


if __name__ == "__main__":
    main()
