import json
import time
import random
from web3 import Web3

# 1. Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("❌ Ganache not connected")

# 2. Contract Details
contract_address = Web3.to_checksum_address(
    "0xDFb2618DaAf55DD95638924cfA5f18698C653c83"
)

# ABI clipped for brevity, ensure your logSensorData section is present
abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "moisture",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "status",
				"type": "string"
			}
		],
		"name": "DataLogged",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_moisture",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_n",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_p",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_k",
				"type": "uint256"
			}
		],
		"name": "logSensorData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "batchCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_batchId",
				"type": "uint256"
			}
		],
		"name": "getBatch",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "moisture",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "nitrogen",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "phosphorus",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "potassium",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "status",
						"type": "string"
					}
				],
				"internalType": "struct AgroContract.BatchData",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "systemStatus",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "traceabilityLedger",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "moisture",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "nitrogen",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "phosphorus",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "potassium",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]


contract = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.accounts[0]

def run_simulator():
    print("🚀 Starting IoT Sensor Simulation...")
    while True:
        moisture = random.randint(20, 60)
        temp = random.randint(25, 35) # This will be sent as Nitrogen (_n)

        print(f"📤 Sending Data: Moisture={moisture}% Temp={temp}°C")

        try:
            # FIX: Use 'logSensorData' name. 
            # We send 'temp' as the second argument (_n)
            # We send '0, 0' for P and K so the contract is satisfied without new variables.
            tx_hash = contract.functions.logSensorData(moisture, temp, 0, 0).transact({
                'from': account,
                'gas': 200000
            })

            w3.eth.wait_for_transaction_receipt(tx_hash)
            print("✅ Data Logged successfully")
            
        except Exception as e:
            print(f"❌ Blockchain Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    run_simulator()