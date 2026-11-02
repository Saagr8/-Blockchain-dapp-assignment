
 // SPDX-License-Identifier: MIT
 pragma solidity ^0.8.20;

 contract HotelBooking {
     // The hotel owner's Ethereum address
     address public hotelOwner;

     // Each hotel room has a price
     struct Room {
         uint256 pricePerNight;
         bool exists;
     }

     // Store rooms by their room number
     mapping(uint256 => Room) public rooms;

     // Store the customer who booked each room on each date
     mapping(uint256 => mapping(uint256 => address)) public bookedBy;

     event RoomAdded(uint256 roomId, uint256 price);
     event RoomBooked(
         uint256 roomId,
         uint256 night,
         address guest,
         uint256 amount
     );

     constructor() {
         hotelOwner = msg.sender;
     }

     // Only the hotel owner can register rooms
     function addRoom(uint256 roomId, uint256 price) public {
         require(msg.sender == hotelOwner, "Only hotel owner");
         require(!rooms[roomId].exists, "Room already exists");
         require(price > 0, "Price must be positive");

         rooms[roomId] = Room(price, true);
         emit RoomAdded(roomId, price);
     }

     // Customer books a room and pays with ETH
     function bookRoom(uint256 roomId, uint256 night) public payable {
         require(rooms[roomId].exists, "Room does not exist");
         require(bookedBy[roomId][night] == address(0), "Already booked");
         require(msg.value == rooms[roomId].pricePerNight, "Incorrect payment");

         bookedBy[roomId][night] = msg.sender;

         // Send the payment to the hotel owner
         (bool success, ) = payable(hotelOwner).call{value: msg.value}("");
         require(success, "Payment failed");

         emit RoomBooked(roomId, night, msg.sender, msg.value);
     }

     // Check whether a room is available on a specific night
     function isAvailable(uint256 roomId, uint256 night)
         public
         view
         returns (bool)
     {
         return rooms[roomId].exists &&
                bookedBy[roomId][night] == address(0);
     }
 }
