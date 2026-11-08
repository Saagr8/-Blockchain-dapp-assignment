
import json
from pathlib import Path
from web3 import Web3

# Connect to local Ganache blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not web3.is_connected():
    raise ConnectionError("Cannot connect to Ganache")

print("Connected to Ganache successfully!")

# Load the latest deployed smart contract address
address_path = (
    Path(__file__).resolve().parent.parent
    / "contracts"
    / "deployed_address.txt"
)

contract_address = Web3.to_checksum_address(
    address_path.read_text(encoding="utf-8").strip()
)

# Load the contract ABI
abi_path = (
    Path(__file__).resolve().parent.parent
    / "contracts"
    / "HotelBooking.abi.json"
)

with open(abi_path, "r", encoding="utf-8") as file:
    contract_abi = json.load(file)

# Check whether the contract exists
if not web3.eth.get_code(contract_address):
    raise RuntimeError("Contract not found on Ganache.")

# Connect to the smart contract
contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# Identify hotel owner and customer
hotel_owner = contract.functions.hotelOwner().call()

customer = next(
    account for account in web3.eth.accounts
    if account.lower() != hotel_owner.lower()
)

# Booking details
room_id = 101
night = 20261211

# Check whether the room exists
room = contract.functions.rooms(room_id).call()

price = room[0]
exists = room[1]

if not exists:
    print("Room does not exist. Hotel owner must add it first.")

else:
    # Check availability
    available = contract.functions.isAvailable(
        room_id, night
    ).call()

    if not available:
        print("Room already booked for this night.")

    else:
        print("Customer:", customer)
        print("Room:", room_id)
        print("Night:", night)
        print("Price (ETH):", web3.from_wei(price, "ether"))

        # Send booking transaction from customer
        tx_hash = contract.functions.bookRoom(
            room_id, night
        ).transact({
            "from": customer,
            "value": price
        })

        # Wait for transaction confirmation
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            print("\nBooking successful!")
            print("Transaction Hash:", tx_hash.to_0x_hex())
            print("Block Number:", receipt.blockNumber)

            # Verify the guest address
            guest = contract.functions.bookedBy(
                room_id, night
            ).call()

            print("Booked By:", guest)

        else:
            print("Booking transaction failed.")
