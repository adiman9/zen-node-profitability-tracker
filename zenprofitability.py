#!/usr/bin/env python

import csv
import os
from datetime import datetime
import requests

# Constants
DATA_SUBDIRECTORY = 'results'
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATA_SUBDIRECTORY,\
                           'zen_tracker.csv')

SUPER_NODE_API = 'https://supernodes1.eu.zensystem.io/api/srvstats'
SECURE_NODE_API = 'https://securenodes.eu.zensystem.io/api/srvstats'
ZEN_PRICE_API = 'https://api.coinmarketcap.com/v2/ticker/1698/'
SUPER_NODE_SERVER_COST = 40 # usd
SECURE_NODE_SERVER_COST = 10 # usd
SUPER_NODE_STAKE = 500
SECURE_NODE_STAKE = 42

ZEN_MINED_PER_MONTH = 216000
SUPER_NODE_REWARD_PERC = 0.1 # 10%
SECURE_NODE_REWARD_PERC = 0.1 # 10%

zen_price_data = requests.get(ZEN_PRICE_API).json()
super_node_data = requests.get(SUPER_NODE_API).json()
secure_node_data = requests.get(SECURE_NODE_API).json()

ZEN_PRICE = zen_price_data['data']['quotes']['USD']['price']

super_node_global = super_node_data['global']
secure_node_global = secure_node_data['global']
super_node_est_earn = super_node_data['estearn']
secure_node_est_earn = secure_node_data['estearn']

SUPER_NODE_MONTHLY_REWARD_ZEN = ZEN_MINED_PER_MONTH * SUPER_NODE_REWARD_PERC / \
                                                    super_node_global['up']
SECURE_NODE_MONTHLY_REWARD_ZEN = ZEN_MINED_PER_MONTH * SECURE_NODE_REWARD_PERC / \
                                                    secure_node_global['up']

SUPER_NODE_MONTHLY_REWARD_USD = SUPER_NODE_MONTHLY_REWARD_ZEN * ZEN_PRICE
SECURE_NODE_MONTHLY_REWARD_USD = SECURE_NODE_MONTHLY_REWARD_ZEN * ZEN_PRICE

SUPER_NODE_MONTHLY_PROFIT = SUPER_NODE_MONTHLY_REWARD_USD - SUPER_NODE_SERVER_COST
SECURE_NODE_MONTHLY_PROFIT = SECURE_NODE_MONTHLY_REWARD_USD - SECURE_NODE_SERVER_COST

SUPER_NODE_ANNUAL_PROFIT_USD = SUPER_NODE_MONTHLY_PROFIT * 12
SECURE_NODE_ANNUAL_PROFIT_USD = SECURE_NODE_MONTHLY_PROFIT * 12

SUPER_NODE_ANNUAL_PROFIT_ZEN = SUPER_NODE_ANNUAL_PROFIT_USD / ZEN_PRICE
SECURE_NODE_ANNUAL_PROFIT_ZEN = SECURE_NODE_ANNUAL_PROFIT_USD / ZEN_PRICE

SUPER_NODE_ANNUAL_ROI = SUPER_NODE_ANNUAL_PROFIT_ZEN / SUPER_NODE_STAKE
SECURE_NODE_ANNUAL_ROI = SECURE_NODE_ANNUAL_PROFIT_ZEN / SECURE_NODE_STAKE

final_result = {
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'super_node_annual_roi': SUPER_NODE_ANNUAL_ROI,
    'secure_node_annual_roi': SECURE_NODE_ANNUAL_ROI,
    'zen_price_usd': ZEN_PRICE,
    'super_node_data': super_node_global,
    'secure_node_data': secure_node_global,
    'super_node_stake': SUPER_NODE_STAKE,
    'secure_node_stake': SECURE_NODE_STAKE,
    'super_node_server_cost': SUPER_NODE_SERVER_COST,
    'secure_node_server_cost': SECURE_NODE_SERVER_COST,
}

def init_csv():
    if not os.path.isfile(OUTPUT_FILE):
        if not os.path.exists(DATA_SUBDIRECTORY):
            os.makedirs(DATA_SUBDIRECTORY)

        f = open(OUTPUT_FILE, 'a')
        w = csv.DictWriter(f, final_result.keys())
        w.writeheader()

if __name__ == '__main__':
    print('ZenCash ROI Tracker')
    init_csv()

    with open(OUTPUT_FILE, 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, final_result.keys())
        w.writerow(final_result)
