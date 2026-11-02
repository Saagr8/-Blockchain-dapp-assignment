
import json
from pathlib import Path
from web3 import Web3

# Connect to our Ganache blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not web3.is_connected():
    raise ConnectionError("Cannot connect to Ganache")

print("Connected to Ganache:", web3.is_connected())

# Address of our deployed HotelBooking contract
contract_address = Web3.to_checksum_address(
    "0x7E7620B498e60193599b7965556dd18Ea6d7BDDC"
)

# Load the contract ABI from our project
abi_path = (
    Path(__file__).resolve().parent.parent
    / "contracts"
    / "HotelBooking.abi.json"
)

with open(abi_path, "r", encoding="utf-8") as file:
    contract_abi = json.load(file)

# Connect Python to the deployed contract
contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# Read Room 101 information
room = contract.functions.rooms(101).call()

print("\n--- Room 101 ---")
print("Price (wei):", room[0])
print("Room exists:", room[1])

# Check booking information
room_id = 101
night = 20261210

available = contract.functions.isAvailable(
    room_id, night
).call()

guest = contract.functions.bookedBy(
    room_id, night
).call()

print("\n--- Booking Information ---")
print("Room:", room_id)
print("Night:", night)
print("Available:", available)
print("Booked by:", guest)
