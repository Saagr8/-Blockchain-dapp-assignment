
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

# Start the application using a customer account
active_account = customers[0]


# Switch between hotel owner and customer test accounts
def switch_account():
    global active_account

    print("\n====== SELECT ACCOUNT ======")
    print("1. Hotel Owner")
    print("2. Customer")

    choice = input("Choose account: ")

    if choice == "1":
        active_account = hotel_owner
        print("Switched to Hotel Owner.")

    elif choice == "2":
        active_account = customers[0]
        print("Switched to Customer.")

    else:
        print("Invalid selection.")


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

    # Only customer role can book through this menu
    if active_account.lower() == hotel_owner.lower():
        print("Please switch to Customer to book a room.")
        return

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

    # Send booking transaction from active customer
    tx_hash = contract.functions.bookRoom(
        room_id, night
    ).transact({
        "from": active_account,
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

    # Only the hotel owner can add a room
    if active_account.lower() != hotel_owner.lower():
        print("Access denied: Only hotel owner can add rooms.")
        return

    room_id = int(input("Enter new room number: "))
    price_eth = Decimal(input("Enter price in ETH: "))

    if price_eth <= 0:
        print("Price must be greater than zero.")
        return

    price_wei = web3.to_wei(price_eth, "ether")

    tx_hash = contract.functions.addRoom(
        room_id, price_wei
    ).transact({
        "from": active_account
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print("Room added successfully!")
        print("Block:", receipt.blockNumber)
    else:
        print("Failed to add room.")


# Main application menu
while True:

    print("\n====== HOTEL BOOKING DAPP ======")

    role = (
        "Hotel Owner"
        if active_account.lower() == hotel_owner.lower()
        else "Customer"
    )

    print("Current Role:", role)
    print("1. View Room")
    print("2. Check Availability")
    print("3. Book Room")
    print("4. Add Room (Hotel Owner)")
    print("5. Switch Account")
    print("6. Exit")

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
            switch_account()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

    except Exception as error:
        print("Operation failed:", error)
