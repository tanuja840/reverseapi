
from web3 import Web3
from abis import (
 
  protocol_data_provider_abi,

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



  # PROTOCOL DATA PROVIDER
  protocol_data_provider_address = NETWORK_CONFIGS["protocol_data_provider_address"]
  protocol_data_provider = W3.eth.contract(address=protocol_data_provider_address, abi=protocol_data_provider_abi)
  return lending_pool, protocol_data_provider

# ------------------------------------------------------------------------------
# Web3 setup
W3 = Web3(Web3.HTTPProvider(NETWORK_CONFIGS["rpc_url"]))
