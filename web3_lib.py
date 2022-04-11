# web3_lib.py
"""
  NOTE: all the numbers in this file are in wei
"""
from web3 import Web3
from abis import (
  lending_pool_addresses_provider_abi,
  lending_pool_abi,
  protocol_data_provider_abi,
  erc20_abi,
)
from gas_station import top_up

# DTOs
from models import BalanceDTO

# Load Configs 
from pyaml_env import parse_config
CONFIGS = parse_config("./config.yaml")
NETWORK_CONFIGS = CONFIGS["networks"]
ADDRESS_CONFIGS = CONFIGS["tokens"]

# Supported tokens
USDC_ADDRESS = Web3.toChecksumAddress(ADDRESS_CONFIGS["USDC"]) # only USDC allowed

# ------------------------------------------------------------------------------
# Private methods
# ------------------------------------------------------------------------------

# boardcasts a raw transaction to the blockchain

def get_reserve_data():
  print(f"Fetching Aave reserve data...")
  data = PROTOCOL_DATA_PROVIDER.functions.getReserveData(USDC_ADDRESS).call()
  print(f"data... {data}")
  data = {
    "availableLiquidity": data[0],
    "totalStableDebt": data[1],
    "totalVariableDebt": data[2],
    "liquidityRate": data[3],
    "variableBorrowRate": data[4],
    "stableBorrowRate": data[5],
    "averageStableBorrowRate": data[6],
    "liquidityIndex": data[7],
    "variableBorrowIndex": data[8],
    "lastUpdateTimestamp": data[9],
  }

  SEC_IN_YEAR = 31536000
  apr = float(int(data['liquidityRate']) / pow(10, 25))
  data["liquidityRateYearly"] = ((1 + (apr / 100) / SEC_IN_YEAR) ** SEC_IN_YEAR - 1) * 100

  apr = float(int(data['variableBorrowRate']) / pow(10, 25))
  data["variableBorrowRateYearly"] = ((1 + (apr / 100) / SEC_IN_YEAR) ** SEC_IN_YEAR - 1) * 100
  return data


def get_coin_reserve_data(coin_name:str):
  coin_name = coin_name.upper()
  if(ADDRESS_CONFIGS.get(coin_name) == None):
       print(f"{coin_name} not found")
       return False
  print(f"Fetching Aave reserve data for {coin_name}...")
  TOKEN_ADDRESS = Web3.toChecksumAddress(ADDRESS_CONFIGS[coin_name])
  data = PROTOCOL_DATA_PROVIDER.functions.getReserveData(TOKEN_ADDRESS).call()
  print(f"reserve data received: {data}")
  data = {
    "availableLiquidity": data[0],
    "totalStableDebt": data[1],
    "totalVariableDebt": data[2],
    "liquidityRate": data[3],
    "variableBorrowRate": data[4],
    "stableBorrowRate": data[5],
    "averageStableBorrowRate": data[6],
    "liquidityIndex": data[7],
    "variableBorrowIndex": data[8],
    "lastUpdateTimestamp": data[9],
  }

  SEC_IN_YEAR = 31536000
  apr = float(int(data['liquidityRate']) / pow(10, 25))
  data["liquidityRateYearly"] = ((1 + (apr / 100) / SEC_IN_YEAR) ** SEC_IN_YEAR - 1) * 100

  apr = float(int(data['variableBorrowRate']) / pow(10, 25))
  data["variableBorrowRateYearly"] = ((1 + (apr / 100) / SEC_IN_YEAR) ** SEC_IN_YEAR - 1) * 100
  return data
# -----------------------------
# Balance
# -----------------------------

  # LENDING POOL
  lending_pool_address = lending_poll_addresses_provider.functions.getLendingPool().call()
  print("lending_pool_address", lending_pool_address)
  lending_pool = W3.eth.contract(address=lending_pool_address, abi=lending_pool_abi)

  # PROTOCOL DATA PROVIDER
  protocol_data_provider_address = NETWORK_CONFIGS["protocol_data_provider_address"]
  protocol_data_provider = W3.eth.contract(address=protocol_data_provider_address, abi=protocol_data_provider_abi)
  return lending_pool, protocol_data_provider

# ------------------------------------------------------------------------------
# Web3 setup
W3 = Web3(Web3.HTTPProvider(NETWORK_CONFIGS["rpc_url"]))
LENDING_POOL, PROTOCOL_DATA_PROVIDER = get_lending_pool()
