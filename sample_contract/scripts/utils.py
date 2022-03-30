from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_NETWORKS = ["development", "ganache-local"]
FORKED_LOCAL_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]


def is_network_local():
    return network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_NETWORKS:
        return accounts[0]
    acc = accounts.add(config["wallets"]["from_key"])
    print(f'get_account:  {acc.address}')
    return acc
