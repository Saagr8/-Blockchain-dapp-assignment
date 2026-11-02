
import json
from pathlib import Path
from decimal import Decimal
from web3 import Web3

# Connect to the local Ganache blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not web3.is_connected():
    raise ConnectionError("Ganache is not running.")

# Load the deployed smart contract
contract_address = Web3.to_checksum_address(
    "0x7E7620B498e60193599b7965556dd18Ea6d7BDDC"
)

abi_path = (
    Path(__file__).resolve().parent.parent
    / "contracts"
    / "HotelBooking.abi.json"
)

with open(abi_path, "r", encoding="utf-8") as file:
    abi = json.load(file)

if web3.eth.get_code(contract_address) == b"":
    raise RuntimeError("Contract not found on Ganache.")

contract = web3.eth.contract(
    address=contract_address,
    abi=abi
)

# Identify hotel owner and customer accounts
hotel_owner = contract.functions.hotelOwner().call()

customers = [
    account for account in web3.eth.accounts
    if account.lower() != hotel_owner.lower()
]

if hotel_owner.lower() not in [
    account.lower() for account in web3.eth.accounts
]:
    raise RuntimeError("Hotel owner account not available in Ganache.")

if not customers:
    raise RuntimeError("No customer account found.")

customer = customers[0]


# View hotel room details
def view_room():
    room_id = int(input("Enter room number: "))
    price, exists = contract.functions.rooms(room_id).call()

    if not exists:
        print("Room does not exist.")
        return

    print("Room Number:", room_id)
    print("Price per night:", web3.from_wei(price, "ether"), "ETH")


# Check room availability
def check_availability():
    room_id = int(input("Enter room number: "))
    night = int(input("Enter night (YYYYMMDD): "))

    available = contract.functions.isAvailable(
        room_id, night
    ).call()

    if available:
        print("Room is available!")
    else:
        print("Room is unavailable or does not exist.")


# Book room as customer
def book_room():
    room_id = int(input("Enter room number: "))
    night = int(input("Enter night (YYYYMMDD): "))

    available = contract.functions.isAvailable(
        room_id, night
    ).call()

    if not available:
        print("Booking rejected: Room unavailable.")
        return

    price, exists = contract.functions.rooms(room_id).call()

    print("Total payment:", web3.from_wei(price, "ether"), "ETH")

    # Send the booking transaction
    tx_hash = contract.functions.bookRoom(
        room_id, night
    ).transact({
        "from": customer,
        "value": price
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print("Booking successful!")
        print("Transaction:", tx_hash.to_0x_hex())
        print("Block:", receipt.blockNumber)
    else:
        print("Booking failed.")


# Add room as hotel owner
def add_room():
    room_id = int(input("Enter new room number: "))
    price_eth = Decimal(input("Enter price in ETH: "))

    price_wei = web3.to_wei(price_eth, "ether")

    tx_hash = contract.functions.addRoom(
        room_id, price_wei
    ).transact({"from": hotel_owner})

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print("Room added successfully!")
        print("Block:", receipt.blockNumber)
    else:
        print("Failed to add room.")


# Main application menu
while True:
    print("\n====== HOTEL BOOKING DAPP ======")
    print("1. View Room")
    print("2. Check Availability")
    print("3. Book Room")
    print("4. Add Room (Hotel Owner)")
    print("5. Exit")

    choice = input("Choose an option: ")

    try:
        if choice == "1":
            view_room()
        elif choice == "2":
            check_availability()
        elif choice == "3":
            book_room()
        elif choice == "4":
            add_room()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
    except Exception as error:
        print("Operation failed:", error)
