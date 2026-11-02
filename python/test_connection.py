
from web3 import Web3

# Connect Python to our local Ganache blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Check if the connection works
print("Connected to Ganache:", web3.is_connected())

# Get information from the blockchain
if web3.is_connected():
    print("Chain ID:", web3.eth.chain_id)
    print("Total Accounts:", len(web3.eth.accounts))
    print("Latest Block:", web3.eth.block_number)
