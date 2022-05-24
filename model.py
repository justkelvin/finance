from datetime import datetime
from random import randint, random

class Customer:
    def __init__(self, customer_name, address, contact, balance, account_type = None, date_created = None, max_w = None, 
    daily_spend = None, max_weekly_spend = None, customer_id = None, status = None):
        self.customer_name = customer_name
        self.address = address
        self.contact = contact
        self.balance = balance
        self.account_type = account_type if account_type is not None else "Standard" # 1 shows its standard account any other value is savings account
        self.date_created = date_created if date_created is not None else datetime.now().isoformat()
        self.max_w = max_w if max_w is not None else 0
        self.daily_spend = daily_spend if daily_spend is not None else 0
        self.max_weekly_spend = max_weekly_spend if max_weekly_spend is not None else 0
        self.customer_id = customer_id if customer_id is not None else None
        self.status = status if status is not None else 1
        
    def __repr__(self) -> str:
        return f"({self.customer_name}, {self.address}, {self.contact}, {self.balance}, {self.account_type}, {self.date_created}, {self.max_w}, {self.daily_spend}, {self.max_weekly_spend},{self.customer_id}, {self.status})"

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