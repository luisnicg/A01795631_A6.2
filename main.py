"""This module is being used to handler all the requests."""

import unittest
from unittest.mock import patch
import os
from hotel import Hotel
from customer import Customer


class Reservation(Hotel, Customer):
    """Class representing a Reservation"""

    def __init__(self, customer_name, hotel_name, room_number=None):
        super().__init__()
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.room_number = room_number

    def create_reservation(self):
        """Method to create a reservation."""

        h = self.hotel_name
        n = self.room_number
        c = self.customer_name
        self.reserve_room(h, n, c)

    def cancel_reservation(self):
        """Method to cancel a reservation."""

        self.cancel_room(self.hotel_name, self.room_number)

    def display_reservation_details(self):
        """Method to display the reservation info."""
        a = self.customer_name
        b = self.hotel_name
        c = self.room_number
        print(f"Reservation:\nCustomer: {a}\nHotel: {b}\nRoom: {c}")


class TestReservation(unittest.TestCase):
    """Class representing a TestReservation"""

    def setUp(self):
        self.hotel = Hotel("hotel_info.json")
        self.customer = Customer("customer_info.json")
        # Create a test hotel
        self.hotel.create_hotel("TestHotel", "TestLocation", [1, 2, 3, 4, 5])

    def tearDown(self):
        # Clean up the test data file after each test
        if os.path.exists("hotel_info.json"):
            os.remove("hotel_info.json")
        if os.path.exists("customer_info.json"):
            os.remove("customer_info.json")

    def test_create_customer(self):
        """Test case: create customer."""

        self.customer.create_customer(1, 'John Doe', 'john@x.com', '0180012')
        customer_info = self.customer.load_customers()
        self.assertEqual(customer_info["customers"][0]['name'], "John Doe")

    def test_update_customer(self):
        """Test case: update customer."""

        self.customer.create_customer(1, 'John Doe', 'john@x.com', '01800')
        customer_info = self.customer.load_customers()
        self.assertEqual(customer_info["customers"][0]['name'], "John Doe")
        self.customer.modify_customer_info(1, 'John Smith')
        customer_info = self.customer.load_customers()
        self.assertEqual(customer_info["customers"][0]['name'], "John Smith")

    def test_delete_customer(self):
        """Test case: create customer."""

        self.customer.create_customer(1, 'John Doe', 'john@x.com', '0180')
        self.customer.create_customer(2, 'Jane Doe', 'jane@x.com', '0181')
        self.customer.delete_customer(2)
        customer_info = self.customer.load_customers()
        self.assertEqual(len(customer_info["customers"]), 1)

    def test_create_reservation(self):
        """Test case: create reservation."""

        reservation = Reservation("John", "TestHotel", 1)
        reservation.create_reservation()
        hotel_info = self.hotel.load_hotels()
        self.assertIn("1", hotel_info["hotels"][0]["reservations"])
        self.assertEqual(hotel_info["hotels"][0]["reservations"]["1"], "John")

    def test_create_reservation_room_does_not_exist(self):
        """Test case: reservation room dows not exist."""

        reservation = Reservation("Bob", "TestHotel", 10)
        reservation.create_reservation()
        hotel_info = self.hotel.load_hotels()
        # Check if the reservation was not created
        # because the room doesn't exist
        self.assertNotIn("10", hotel_info["hotels"][0]["reservations"])

    def test_create_reservation_already_reserved(self):
        """Test case: reservation already reserved."""

        reservation1 = Reservation("Alice", "TestHotel", 1)
        reservation1.create_reservation()
        reservation2 = Reservation("Bob", "TestHotel", 1)
        hotel_info = self.hotel.load_hotels()
        with patch('sys.stdout', new=open(os.devnull, 'w', encoding="utf-8")):
            reservation2.create_reservation()

        self.assertEqual(len(hotel_info["hotels"][0]["reservations"]), 1)
        self.assertEqual(hotel_info["hotels"][0]["reservations"]["1"], "Alice")

    def test_cancel_reservation(self):
        """Test case: cancel reservation."""

        reservation = Reservation("Jane Doe", "TestHotel", 2)
        reservation.create_reservation()
        reservation.cancel_reservation()
        hotel_info = self.hotel.load_hotels()
        self.assertNotIn("2", hotel_info["hotels"][0]["reservations"])

    def test_cancel_reservation_not_reserved(self):
        """Test case: reservation not reserved."""

        reservation = Reservation("Alice", "TestHotel", 1)
        with patch('sys.stdout', new=open(os.devnull, 'w', encoding="utf-8")):
            reservation.cancel_reservation()
        hotel_info = self.hotel.load_hotels()
        # Check that the reservation was not made, and no error is raised
        self.assertNotIn("1", hotel_info["hotels"][0]["reservations"])


if __name__ == '__main__':
    # hotel = Hotel()
    # hotel.create_hotel('Playa linda', 'At the beach', [1,2,3,4,5,6])
    # hotel.create_hotel('Fiesta Inn', 'At the beach', [1,2,3,4,5,6,7])
    # hotel.display_hotel_info('Playa linda')

    # customer = Customer()
    # customer.create_customer(1, 'John Doe', 'john@example.com', '018001231')
    # customer.create_customer(2, 'Jane Doe', 'jane@example.com', '018001232')

    # CUSTOME_NAME = "John Doe"
    # customer = Customer()
    # info = customer.get_customer_info_by_name(CUSTOME_NAME)

    # reservation = Reservation("John Doe", "Playa linda", str(info["customer_id"]))
    # reservation.create_reservation()
    # reservation.cancel_reservation()
    # reservation.display_reservation_details()

    unittest.main(argv=['first-arg-is-ignored'], exit=False)
