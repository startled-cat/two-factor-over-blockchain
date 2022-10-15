
import os
import json
import sqlite3 as sql
from network_config import network_config
script_path = os.path.dirname(os.path.realpath(__file__))

# create sqlite databse


def create_db(db_path):
    conn = sql.connect(db_path)
    c = conn.cursor()
    # delete and create table
    c.execute('''DROP TABLE IF EXISTS benchmark_data''')
    conn.commit()
    c.execute('''CREATE TABLE benchmark_data (
        network text, 
        datetime datetime,
        user_time1 real,
        user_time2 real,
        user_time3 real,
        user_time4 real,
        user_time5 real,
        user_gas_used bigint,
        user_gas_price bigint,
        user_cost bigint,
        app_time1 real,
        app_time2 real,
        app_time3 real,
        app_time4 real,
        app_time5 real,
        app_gas_used bigint,
        app_gas_price bigint,
        app_cost bigint,
        
        user_cost_eth bigint,
        user_gas_price_eth bigint,
        app_cost_eth bigint,
        app_gas_price_eth bigint
        )''')
    conn.commit()
    conn.close()


def load_data():
    def swap_elements(l, a, b):
        l[a], l[b] = l[b], l[a]
        return l
    # path to directory where this script is located

    data_dir_path = f'{script_path}/../../data/benchmark/network'
    # networks_file_path = f'{data_dir_path}/networks.txt'

    # # read lines from networks file into a list
    # with open(networks_file_path, 'r') as f:
    #     networks = f.readlines()
    #     # remove newline characters from each line
    #     networks = [network.rstrip() for network in networks]
    
    networks = list(network_config.keys())
    # reorder networks
    networks = swap_elements(networks, 9, 4)
    networks = swap_elements(networks, 11, 5)
    
    # sort networks by their name
    # networks.sort(key=lambda x: network_config[x]["name"], reverse=True)

    # print(networks)

    network_data = []

    for network in networks:
        # print(f"Parsing data for {network}")
        # load json data from each network
        data_file_path = f'{data_dir_path}/{network}/{network}.json'
        with open(data_file_path, 'r') as f:
            data = json.load(f)["_default"]
            data_list = []
            # for each key in the data, add the value to the data_list
            for key in data:
                data[key]["user_cost_eth"] = data[key]["user_cost"] * network_config[network]["to_eth"]
                data[key]["user_gas_price_eth"] = data[key]["user_gas_price"] * network_config[network]["to_eth"]
                data[key]["app_cost_eth"] = data[key]["app_cost"] * network_config[network]["to_eth"]
                data[key]["app_gas_price_eth"] = data[key]["app_gas_price"] * network_config[network]["to_eth"]
                data_list.append(data[key])
                
            # filter out incomplete data
            data_list = [d for d in data_list if d["user_time"][-1] > 0]
            data_list = [d for d in data_list if d["app_time"][-1] > 0]
            data_list = [d for d in data_list if d["user_time"][0] > 0]
            data_list = [d for d in data_list if d["app_time"][0] > 0]
            

            print(f"{network}: {len(data_list)}")
            network_data.append((network, data_list))

    # print(f"loaded data from {len(network_data)} networks")
    # for entry in network_data:
    #     print(f"{entry[0]} : {len(entry[1])}")

    return network_data


def add_network_data_to_db(network_data, db_path):
    conn = sql.connect(db_path)
    c = conn.cursor()
    for (network, data) in network_data:
        for m in data:
            c.execute('''INSERT INTO benchmark_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (network, m["datetime"],
                       m["user_time"][0], m["user_time"][1], m["user_time"][2], m["user_time"][3], m["user_time"][4],
                       m["user_gas_used"], m["user_gas_price"], m["user_cost"],
                       m["app_time"][0], m["app_time"][1], m["app_time"][2], m["app_time"][3], m["app_time"][4],
                       m["app_gas_used"], m["app_gas_price"], m["app_cost"],
                       m["user_cost_eth"], m["user_gas_price_eth"], m["app_cost_eth"], m["app_gas_price_eth"]))
    conn.commit()
    conn.close()


def main():
    # create database
    db_path = f'{script_path}/benchmark_data.db'
    create_db(db_path)
    # load data
    network_data = load_data()
    # add data to database
    add_network_data_to_db(network_data, db_path)

def test():
    load_data()

if __name__ == "__main__":
    # main()
    test()
