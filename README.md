# Hotel Booking DApp

This is a blockchain project I made for my university assignment. The idea is to create a simple hotel booking system where a hotel owner can add rooms and customers can book them using test Ethereum (ETH).

I used Solidity to write the smart contract and Python to interact with it. I also used Ganache to run a local blockchain and test the transactions.

## What My Project Does

- The hotel owner can add new rooms and set their prices.
- Customers can view room details and check availability.
- Customers can book a room for a selected night.
- The customer pays using test ETH when making a booking.
- Once a room is booked for a particular night, another customer cannot book the same room for that night.
- Booking transactions are recorded on the blockchain.
- The application allows me to switch between hotel owner and customer accounts for testing.

## Tools and Technologies Used

- **Solidity** – To write the hotel booking smart contract.
- **Python** – To create the application and interact with the blockchain.
- **Web3.py** – To connect Python with the smart contract.
- **Ganache** – To create a local blockchain and test transactions.
- **Remix IDE** – To compile, deploy and test the smart contract.
- **Shell Script** – To help run the Python application.
- **VS Code** – To write and manage my project files.
- **Git and GitHub** – To save my work and track changes.

## Project Files

- `contracts/HotelBooking.sol` – The Solidity smart contract.
- `contracts/HotelBooking.abi.json` – The contract ABI used by Python.
- `contracts/deployed_address.txt` – Stores the deployed contract address.
- `python/app.py` – The main hotel booking application.
- `python/test_connection.py` – Checks the connection to Ganache.
- `python/read_booking.py` – Reads room and booking details.
- `python/book_room.py` – Tests booking a room using Python.
- `scripts/run_app.sh` – Shell script to start the application.
- `screenshots/` – Screenshots of my project testing.

## How to Run the Project

**1. Download the project**

Clone the GitHub repository or download the project files.

**2. Install the Python requirements**

Create and activate a Python virtual environment, then run:

`pip install -r requirements.txt`

**3. Start Ganache**

Open Ganache and start the local blockchain. The application is configured to connect to:

`http://127.0.0.1:7545`

**4. Deploy the smart contract**

Open `HotelBooking.sol` in Remix IDE.

Compile the contract using the **Paris EVM version**, then connect Remix to Ganache using the External HTTP Provider.

Deploy the contract using a Ganache account and copy the new contract address into:

`contracts/deployed_address.txt`

Make sure `HotelBooking.abi.json` matches the compiled contract.

**5. Run the Python application**

Open the project folder in VS Code and run:

`python python/app.py`

You can also use the shell script through Git Bash:

`bash scripts/run_app.sh`

The application will display a menu where you can view rooms, check availability, book a room, add rooms as the hotel owner and switch accounts.

## Testing

I tested the smart contract using Remix, Ganache and Python.

Some of the tests I completed were:

- Checking the connection between Python and Ganache.
- Adding a new room using the hotel owner account.
- Checking that a customer cannot add rooms.
- Booking a room and paying with test ETH.
- Checking the booking details stored on the blockchain.
- Trying to book a room that was already booked for the same night.

The tests helped me understand how Python communicates with a smart contract and how transactions are stored on the blockchain.

## Current Limitations

This is a basic working project for learning and demonstration purposes.

At the moment, the application supports booking one room for one night at a time. It does not include booking cancellation, refunds, multi-night bookings or a website interface.

It uses Ganache test accounts and test ETH, so no real money is involved.

If the Ganache blockchain is reset, the smart contract needs to be deployed again, and the rooms and bookings need to be added again.

## What I Learned

Through this project, I learned how to create a basic smart contract using Solidity and connect it with Python using Web3.py.

I also learned how to use Ganache for testing, send transactions, work with different accounts and check information stored on the blockchain.

One important thing I understood is how the smart contract can prevent two customers from booking the same room for the same night.