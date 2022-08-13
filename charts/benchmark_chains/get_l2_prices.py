
import requests
from network_config import network_config


# for each netowrk in network_config...
for network in network_config:
    eth_value = 1
    coin_symbol = network_config[network]["symbol"]
    # if coin is ETH, set eth_value to 1, else get value from internet
    if coin_symbol == "ETH":
        eth_value = 1
    else:
        url = f"https://api.coinmarketcap.com/v1/ticker/{coin_symbol}"
        response = requests.get(url)
        data = response.json()
        print(data)
        eth_value = data[0]["price_eth"]
    print(f"{network} : {eth_value}")