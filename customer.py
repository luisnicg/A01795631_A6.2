"""The program to manage customers."""

import json
import os


class Customer:
    """Class representing a Customer"""

    def __init__(self, filename="customer_info.json"):
        self.filename = filename
        self.customer_info = self.load_customers()

    def load_customers(self):
        """Method to load the data."""

        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"customers": []}

    def save_data(self):
        """Method to save the data."""

        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(self.customer_info, f, indent=4)

    def get_customer_info(self, customer_id):
        """Method to get the information of a customer.

            Args:
                customer_id: The internal identifier of the customer
          Returns:
                hotel: The customer information.
        """

        for customer in self.customer_info["customers"]:
            if customer["customer_id"] == customer_id:
                return customer
        return None

    def get_customer_info_by_name(self, customer_name):
        """Method to get the information of a customer by name.

            Args:
                customer_name: The customer name.
          Returns:
                hotel: The customer information.
        """
        for customer in self.customer_info["customers"]:
            if customer["name"] == customer_name:
                return customer
        return None

    def create_customer(self, customer_id, name, email, phone):
        """Method to create a customer.

            Args:
                customer_id: The internal identifier of the customer.
                name: The name of the customer.
                email: The location of the customer.
                phone: The phone of the customer.
        """

        new_customer = {
          "customer_id": customer_id,
          "name": name,
          "email": email,
          "phone": phone
        }

        customer = self.get_customer_info(customer_id)
        if customer:
            print(f"Customer '{name}' already exists.")
        else:
            self.customer_info["customers"].append(new_customer)
            self.save_data()
            print(f"Customer '{name}' created successfully.")

    def delete_customer(self, customer_id):
        """Method to delete a customer.

            Args:
                customer_id: The internal identifier of the customer
        """

        self.customer_info["customers"] = [
          c for c in self.customer_info["customers"]
          if c["customer_id"] != customer_id
        ]
        self.save_data()
        print(f"Customer with ID '{customer_id}' deleted successfully.")

    def display_customer_info(self, customer_id):
        """Method to display the customer information.

            Args:
                customer_id: The internal identifier of the customer
        """

        customer = self.get_customer_info(customer_id)
        if customer:
            print(customer)
        else:
            print(f"Customer with ID '{customer_id}' not found.")

    def modify_customer_info(self,
                             customer_id,
                             new_name=None,
                             new_email=None,
                             new_phone=None
                             ):
        """Method to update the customer information.

            Args:
                customer_id: The internal identifier of the customer
        """

        for customer in self.customer_info["customers"]:
            if customer["customer_id"] == customer_id:
                if new_name:
                    customer["name"] = new_name
                if new_email:
                    customer["email"] = new_email
                if new_phone:
                    customer["phone"] = new_phone
                self.save_data()
                print(f"Customer ID '{customer_id}' updated successfully.")
                return
        print(f"Customer with ID '{customer_id}' not found.")
