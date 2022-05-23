from datetime import datetime

class Customer:
    def __init__(self, customer_id, customer_name, address, contact, balance, account_type=None, date_created=None, position=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.address = address
        self.contact = contact
        self.balance = balance
        self.account_type = account_type if account_type is not None else 1
        self.date_created = date_created if date_created is not None else datetime.now().isoformat()
        self.position = position if position is not None else None
        
    def __repr__(self) -> str:
        return f"({self.customer_id}, {self.customer_name}, {self.address}, {self.contact}, {self.balance}, {self.account_type}, {self.date_created}, {self.position})"

class Bank:
    def __init__(self, bank_name, bank_location, active_customers):
        self.bank_name = bank_name
        self.bank_location = bank_location
        self.active_customers = active_customers

    def __repr__(self) -> str:
        return f"({self.bank_name}, {self.bank_location}, {self.active_customers})"

class Accounts:
    def __init__(self, account_number, customer_id, last_transaction, account_age, account_type):
        self.account_number = account_number
        self.customer_id = customer_id
        self.last_transaction = last_transaction
        self.account_age = account_age
        self.account_type = account_type

    def __repr__(self) -> str:
        return f"({self.account_number}, {self.customer_id}, {self.last_transaction}, {self.account_age}, {self.account_type})"
        