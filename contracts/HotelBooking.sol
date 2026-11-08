
 // SPDX-License-Identifier: MIT
 pragma solidity ^0.8.20;

 contract HotelBooking {

     // Hotel owner's Ethereum address
     address public hotelOwner;

     // Information about a hotel room
     struct Room {
         uint256 pricePerNight;
         bool exists;
     }

     // Store hotel rooms
     mapping(uint256 => Room) public rooms;

     // Store bookings by room number and date
     mapping(uint256 => mapping(uint256 => address)) public bookedBy;

     // Events
     event RoomAdded(uint256 roomId, uint256 price);

     event RoomBooked(
         uint256 roomId,
         uint256 night,
         address guest,
         uint256 amount
     );

     // Set hotel owner when contract is deployed
     constructor() {
         hotelOwner = msg.sender;
     }

     // Add a new hotel room
     function addRoom(uint256 roomId, uint256 price) public {
         require(msg.sender == hotelOwner, "Only hotel owner");
         require(!rooms[roomId].exists, "Room already exists");
         require(price > 0, "Price must be positive");

         rooms[roomId] = Room(price, true);

         emit RoomAdded(roomId, price);
     }

     // Book a hotel room using ETH
     function bookRoom(uint256 roomId, uint256 night) public payable {
         require(rooms[roomId].exists, "Room does not exist");
         require(bookedBy[roomId][night] == address(0), "Already booked");
         require(msg.value == rooms[roomId].pricePerNight, "Incorrect payment");

         bookedBy[roomId][night] = msg.sender;

         // Send payment to hotel owner
         (bool success, ) = payable(hotelOwner).call{value: msg.value}("");
         require(success, "Payment failed");

         emit RoomBooked(roomId, night, msg.sender, msg.value);
     }

     // Check room availability
     function isAvailable(uint256 roomId, uint256 night)
         public
         view
         returns (bool)
     {
         return rooms[roomId].exists &&
                bookedBy[roomId][night] == address(0);
     }
 }
