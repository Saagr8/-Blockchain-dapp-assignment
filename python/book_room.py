
import json
from pathlib import Path
from web3 import Web3

# Connect to local Ganache blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not web3.is_connected():
    raise ConnectionError("Cannot connect to Ganache")

print("Connected to Ganache successfully!")

# Load our deployed smart contract
contract_address = Web3.to_checksum_address(
    "0x7E7620B498e60193599b7965556dd18Ea6d7BDDC"
)

abi_path = (
    Path(__file__).resolve().parent.parent
    / "contracts"
    / "HotelBooking.abi.json"
)

with open(abi_path, "r", encoding="utf-8") as file:
    contract_abi = json.load(file)

if not web3.eth.get_code(contract_address):
    raise RuntimeError("Contract not found. Check Ganache and its address.")

contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# Select a Ganache customer account, not the hotel owner
hotel_owner = contract.functions.hotelOwner().call()
customer = next(
    account for account in web3.eth.accounts
    if account.lower() != hotel_owner.lower()
)

# Booking details
room_id = 101
night = 20261211

# Check availability before booking
available = contract.functions.isAvailable(
    room_id, night
).call()

if not available:
    print("Room already booked for this night.")

else:
    # Read the room price from the smart contract
    room = contract.functions.rooms(room_id).call()
    price = room[0]

    print("Customer:", customer)
    print("Room:", room_id)
    print("Night:", night)
    print("Price (ETH):", web3.from_wei(price, "ether"))

    # Send booking transaction with test ETH
    tx_hash = contract.functions.bookRoom(
        room_id, night
    ).transact({
        "from": customer,
        "value": price
    })

    # Wait for the blockchain to confirm the transaction
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print("\nBooking successful!")
        print("Transaction Hash:", tx_hash.to_0x_hex())
        print("Block Number:", receipt.blockNumber)

        # Verify booking
        guest = contract.functions.bookedBy(
            room_id, night
        ).call()

        print("Booked By:", guest)
    else:
        print("Booking transaction failed.")
