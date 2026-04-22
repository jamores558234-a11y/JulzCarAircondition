
class Customer:
    def __init__(self, customer_id, name, contact, email=None, address=None):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        self.email = email
        self.address = address