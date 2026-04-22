"""Customer controller"""
from database.connection import DatabaseConnection


class CustomerController:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_customer(self, name, contact, email, address):
        """Add new customer"""
        try:
            query = """INSERT INTO customers (name, contact, email, address) 
                      VALUES (%s, %s, %s, %s)"""
            result = self.db.execute_query(query, (name, contact, email, address))
            return result > 0
        except Exception as e:
            print(f"Add Customer Error: {e}")
            return False

    def get_all_customers(self):
        """Get all customers"""
        try:
            query = "SELECT * FROM customers"
            return self.db.execute_query(query)
        except Exception as e:
            print(f"Get Customers Error: {e}")
            return []

    def get_customer(self, customer_id):
        """Get single customer"""
        try:
            query = "SELECT * FROM customers WHERE customer_id = %s"
            result = self.db.execute_query(query, (customer_id,))
            return result[0] if result else None
        except Exception as e:
            print(f"Get Customer Error: {e}")
            return None

    def update_customer(self, customer_id, name, contact, email, address):
        """Update customer"""
        try:
            query = """UPDATE customers SET name=%s, contact=%s, email=%s, address=%s 
                      WHERE customer_id=%s"""
            result = self.db.execute_query(query, (name, contact, email, address, customer_id))
            return result > 0
        except Exception as e:
            print(f"Update Customer Error: {e}")
            return False

    def delete_customer(self, customer_id):
        """Delete customer"""
        try:
            query = "DELETE FROM customers WHERE customer_id = %s"
            result = self.db.execute_query(query, (customer_id,))
            return result > 0
        except Exception as e:
            print(f"Delete Customer Error: {e}")
            return False