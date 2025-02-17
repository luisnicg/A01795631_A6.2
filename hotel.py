"""The program to manage hotels."""

import json
import os


class Hotel:
    """Class representing a Hotel"""

    def __init__(self, filename="hotel_info.json"):
        self.filename = filename
        self.hotel_info = self.load_hotels()

    def load_hotels(self):
        """Method to load the data."""

        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"hotels": []}

    def save_data(self):
        """Method to save the data."""

        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(self.hotel_info, f, indent=4)

    def create_hotel(self, name, location, rooms):
        """Method to create a hotel.

            Args:
                name: The name of the hotel.
                location: The location of the hotel.
                rooms: Total amount of rooms.
        """
        hotel = self.get_hotel_info(name)
        if hotel:
            self.update_hotel(name, name, location, rooms)
        else:
            new_hotel = {"name": name,
                         "location": location,
                         "rooms": rooms,
                         "reservations": {}
                         }
            self.hotel_info["hotels"].append(new_hotel)
            self.save_data()
            print(f"Hotel '{name}' created successfully.")

    def update_hotel(self,
                     name,
                     new_name=None,
                     new_location=None,
                     new_rooms=None
                     ):
        """Method to update a hotel.

            Args:
                name: The name of the hotel.
                location: The location of the hotel.
                rooms: Total amount of rooms.
        """
        for hotel in self.hotel_info["hotels"]:
            if hotel["name"] == name:
                if new_name:
                    hotel["name"] = new_name
                if new_location:
                    hotel["location"] = new_location
                if new_rooms:
                    hotel["rooms"] = new_rooms
                self.save_data()
                print(f"Hotel '{name}' updated successfully.")
                return
        print(f"Hotel '{name}' not found.")

    def delete_hotel(self, name):
        """Method to delete a hotel.

            Args:
                name: The name of the hotel.
        """
        self.hotel_info["hotels"] = [h for h in self.hotel_info["hotels"]
                                     if h["name"] != name]
        self.save_data()
        print(f"Hotel '{name}' deleted successfully.")

    def get_hotel_info(self, name):
        """Method to get the information of a hotel.

            Args:
                name: The name of the hotel.
          Returns:
                hotel: The hotel information.
        """

        for hotel in self.hotel_info["hotels"]:
            if hotel["name"] == name:
                return hotel
        return None

    def display_hotel_info(self, name):
        """Method to display the information of a hotel.

            Args:
                name: The name of the hotel.
        """
        hotel = self.get_hotel_info(name)
        if hotel:
            print(hotel)
        else:
            print(f"Hotel '{name}' not found.")

    def reserve_room(self, hotel_name, room_number, customer_name):
        """Method to reserve a room.

            Args:
                hotel_name: The name of the hotel.
                room_number: The number of the room.
                customer_name: The customer name.
        """
        try:
            for hotel in self.hotel_info["hotels"]:
                if hotel["name"] == hotel_name:
                    if (room_number in hotel["rooms"] and
                       str(room_number) not in hotel["reservations"]):
                        hotel["reservations"][room_number] = customer_name
                        self.save_data()
                        r = room_number
                        h = hotel_name
                        c = customer_name
                        print(f"Room {r} in {h} reserved for {c}.")
                        return
                    elif room_number not in hotel["rooms"]:
                        r = room_number
                        h = hotel_name
                        print(f"Room {r} does not exist in {h}")
                        return
                    else:
                        r = room_number
                        h = hotel_name
                        print(f"Room {r} in {h} is already reserved.")
                        return
            print(f"Hotel '{hotel_name}' not found for this reservation.")
        except Exception as e:
            print(f"Error creating the reservation: {e}")

    def cancel_room(self, hotel_name, room_number):
        """Method to cancel a reservation.

            Args:
                hotel_name: The name of the hotel.
                room_number: The number of the room.
        """

        for hotel in self.hotel_info["hotels"]:
            if hotel["name"] == hotel_name:
                if room_number in hotel["reservations"]:
                    del hotel["reservations"][room_number]
                    self.save_data()
                    r = room_number
                    h = hotel_name
                    print(f"Reservation room {r} in {h} canceled.")
                    return
                else:
                    r = room_number
                    h = hotel_name
                    print(f"Room {r} in {h} is not reserved.")
                    return
        print(f"Hotel '{hotel_name}' not found.")
