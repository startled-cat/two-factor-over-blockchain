
from brownie import PasswordlessAuthentication
from scripts.utils import get_account, measure_contract_stats
from brownie import compile_source, web3
import json
import numpy as np

solcVersions = [
    "0.8.15",
    "0.8.14",
    "0.8.13",
    "0.8.12",
    "0.8.11",
    "0.8.10",
    "0.8.9",
    "0.8.8",
    "0.8.7",
    "0.8.6",
    "0.8.5",
    "0.8.4",
    "0.8.3",
    "0.8.2",
    "0.8.1",
    "0.8.0",
    "0.7.6",
    "0.7.5",
    "0.7.4",
    "0.7.3",
    "0.7.2",
    "0.7.1",
    "0.7.0",
    "0.6.12",
    "0.6.11",
    "0.6.10",
    "0.6.9",
    "0.6.8",
    "0.6.7",
    "0.6.6",
    "0.6.5",
    "0.6.4",
    "0.6.3",
    "0.6.2",
    "0.6.1",
    "0.6.0",
    "0.5.17",
    "0.5.16",
    "0.5.15",
    "0.5.14",
    "0.5.13",
    "0.5.12",
    "0.5.11",
    "0.5.10",
    "0.5.9",
    "0.5.8",
    "0.5.7",
    "0.5.6",
    "0.5.5",
    "0.5.4",
    "0.5.3",
    "0.5.2",
    "0.5.1",
    "0.5.0",
    "0.4.26",
    "0.4.25",
    "0.4.24",
    "0.4.23",
    "0.4.22",
    "0.4.21",
    "0.4.20",
    "0.4.19",
    "0.4.18",
    "0.4.17",
    "0.4.16",
    "0.4.15",
    "0.4.14",
    "0.4.13",
    "0.4.12",
    "0.4.11",
    "0.4.10",
    "0.4.9",
    "0.4.8",
    "0.4.7",
    "0.4.6",
    "0.4.5",
    "0.4.4",
    "0.4.3",
    "0.4.2",
    "0.4.1",
    "0.4.0",
    "0.3.6",
    "0.3.5",
    "0.3.4",
    "0.3.3",
    "0.3.2",
    "0.3.1",
    "0.3.0",
    "0.2.2",
    "0.2.1",
    "0.2.0",
    "0.1.7",
    "0.1.6",
    "0.1.5",
    "0.1.4",
    "0.1.3",
    "0.1.2"
]

optimizeRuns = [*range(100, 4_001, 200)]
optimizeRunsLog = [None, 0, 1, 10, 100, 1_000,
                   10_000, 100_000, 1_000_000, 10_000_000]


def compile_from_source(source, settings):
    container = compile_source(
        source,
        solc_version=settings["solc_version"],
        optimize=settings["optimize"],
        runs=settings["runs"],
        evm_version=settings["evm_version"]
    )
    contract = container.PasswordlessAuthentication.deploy(
        {"from": get_account(), "allow_revert": True, "gas_limit": 2_000_000})

    return contract


# def compare_compiler_settings():
#     user1 = get_account(0)
#     app1 = get_account(1)
#     contractSourceCode = PasswordlessAuthentication._sources.get(
#         "PasswordlessAuthentication")
#     # https://eth-brownie.readthedocs.io/en/stable/api-project.html?highlight=compile#main.compile_source

#     # brownie supports solc versions from 0.4.22
#     brownieSolcVersions = solcVersions[:57]
#     compilerSettings = {
#         "solc_version": "0.8.15",
#         "optimize": True,
#         "runs": 200,
#         "evm_version": None,
#     }

#     stats = []

#     for solcVersion in brownieSolcVersions:
#         print(f"Testing solc version: {solcVersion}")
#         compilerSettings["solc_version"] = solcVersion
#         for runs in optimizeRuns:
#             print(f"Testing runs: {runs}")
#             compilerSettings["runs"] = runs
#             compilerSettings["optimize"] = True if runs is not None else False
#             contract = compile_from_source(
#                 contractSourceCode, compilerSettings)

#             s = measure_contract_stats(contract, n=1)
#             s.pop("time")
#             s.pop("userGasPrice")
#             s.pop("appGasPrice")
#             s["solcVersion"] = solcVersion
#             s["solcOptimizerRuns"] = runs
#             s["optimize"] = compilerSettings["optimize"]
#             s["contractDeployGasUsed"] = contract.tx.gas_used
#             stats.append(s)
#     return stats


def compare_compiler_versions(runs=10_000):
    contractSourceCode = PasswordlessAuthentication._sources.get(
        "PasswordlessAuthentication")
    # brownie supports solc versions from 0.4.22
    brownieSolcVersions = solcVersions[:57]
    compilerSettings = {
        "solc_version": "0.8.15",
        "optimize": True,
        "runs": runs,
        "evm_version": None,
    }

    stats = []

    for solcVersion in brownieSolcVersions:
        compilerSettings["solc_version"] = solcVersion
        contract = compile_from_source(contractSourceCode, compilerSettings)
        s = measure_contract_stats(contract, n=1)
        s.pop("time")
        s.pop("userGasPrice")
        s.pop("appGasPrice")
        s["solcVersion"] = solcVersion
        s["solcOptimizerRuns"] = compilerSettings["runs"]
        s["optimize"] = compilerSettings["optimize"]
        s["contractDeployGasUsed"] = contract.tx.gas_used
        stats.append(s)
    return stats


def compare_compiler_optimizations(solcVersion="0.8.15", runs_list=optimizeRunsLog):
    contractSourceCode = PasswordlessAuthentication._sources.get(
        "PasswordlessAuthentication")
    # https://eth-brownie.readthedocs.io/en/stable/api-project.html?highlight=compile#main.compile_source

    compilerSettings = {
        "solc_version": "0.8.15",
        "optimize": True,
        "runs": 200,
        "evm_version": None,
    }

    stats = []
    compilerSettings["solc_version"] = solcVersion
    for runs in runs_list:
        compilerSettings["runs"] = runs
        compilerSettings["optimize"] = True if runs is not None else False
        contract = compile_from_source(
            contractSourceCode, compilerSettings)

        s = measure_contract_stats(contract, n=1)
        s.pop("time")
        s.pop("userGasPrice")
        s.pop("appGasPrice")
        s["solcVersion"] = compilerSettings["solc_version"]
        s["solcOptimizerRuns"] = compilerSettings["runs"]
        s["optimize"] = compilerSettings["optimize"]
        s["contractDeployGasUsed"] = contract.tx.gas_used
        stats.append(s)
    return stats


def main():

    # print("compare_compiler_versions ...")
    # stats = compare_compiler_versions()
    # with open('../data/compare_compiler_versions.json', 'w') as f:
    #     json.dump(stats, f)

    print("compare_compiler_optimizations ...")
    stats = compare_compiler_optimizations("0.8.15", runs_list=optimizeRunsLog)
    with open('../data/compare_compiler_optimizations_1.json', 'w') as f:
        json.dump(stats, f)

    stats = compare_compiler_optimizations("0.8.15", runs_list=optimizeRuns)
    with open('../data/compare_compiler_optimizations_2.json', 'w') as f:
        json.dump(stats, f)
