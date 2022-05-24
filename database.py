#!/usr/bin/env python3

from random import randint
import sqlite3
from typing import List
from datetime import datetime
from model import Accounts, Bank, Customer

conn = sqlite3.connect('finance.db')
c = conn.cursor()

def create_customer_table():
    '''Create the sqlite table to store customer data.'''
    c.execute("""CREATE TABLE IF NOT EXISTS customer (
        customer_name text,
        address text,
        contact text,
        balance text,
        account_type text,
        date_created text,
        max_w text,
        daily_spend text,
        spending text,
        customer_id text,
        status text
    )""")

def create_bank_table():
    '''Create bank details'''
    c.execute("""CREATE TABLE IF NOT EXISTS bank (
        bank_name text,
        bank_location text,
        active_customers text
    )""")

def create_accounts():
    '''Creating customer accounts'''
    c.execute("""CREATE TABLE IF NOT EXISTS accounts (
        account_number int,
        customer_id text,
        last_transaction text,
        account_age text,
        account_type text
    )""")

create_customer_table()
create_accounts()
create_bank_table()

def bank_details(bank: Bank):
    '''Info about the bank'''
    with conn:
        c.execute('INSERT INTO bank VALUES (:bank_name, :bank_location, :active_customers)',
        {'bank_name': bank.bank_name, 'bank_location': bank.bank_location, 'active_customers': bank.active_customers})

def bank_info() ->  List[Bank]:
    '''Fetch all detail about a bank'''
    c.execute('select * from bank')
    results = c.fetchall()
    bank = []

    for result in results:
        bank.append(Bank(*result))
    return bank

def insert_user(accounts: Customer):
    '''Insert customer data to the database'''
    c.execute('select count(*) FROM customer')
    # count = c.fetchone()[0]
    accounts.customer_id = randint(1111111, 99999999) #if count else 0

    with conn:
        c.execute('INSERT INTO customer VALUES (:customer_name, :address, :contact, :balance, :account_type, :date_created, :max_w, :daily_spend, :spending, :customer_id, :status)',
                  {'customer_name': accounts.customer_name, 'address': accounts.address, 'contact': accounts.contact,
                   'balance': accounts.balance, 'account_type': accounts.account_type, 'date_created': accounts.date_created, 'max_w': accounts.max_w, 'daily_spend': accounts.daily_spend, 'spending': accounts.spending, 'customer_id': accounts.customer_id, 'status': accounts.status})

def get_all_info() -> List[Customer]:
    '''Fetch all data from the databse and return it as a list'''
    c.execute('select * from customer')
    results = c.fetchall()
    customer = []

    for result in results:
        customer.append(Customer(*result))
    return customer

def transact_withdraw(customer_id: int, amount: int, commit=True):
    '''Deduct cash from users balance'''
    c.execute('select account_type from customer where customer_id = :customer_id', {'customer_id': customer_id})
    account_type = c.fetchone()[0]
    if account_type == "Standard":
        c.execute('select balance from customer where customer_id = :customer_id', {'customer_id': customer_id})
        balance = c.fetchone()[0]
        new_balance = int(balance) - int(amount)
        if int(amount) <= int(balance):
            with conn:
                c.execute('UPDATE customer SET balance = :balance WHERE customer_id = :customer_id', {'balance': new_balance, 'customer_id': customer_id})
                return f"Success, new account balance {new_balance}."
        else:
            return f"Your account balance of {balance} is not enough to transact this amount of {amount}."
    else:
        """Check the transaction limit and amount they are transacting"""
        c.execute('select * from customer where customer_id = :customer_id', {'customer_id': customer_id})
        account_info = c.fetchall()
        details = []
        
        for info in account_info:
            details.append(Customer(*info))
        
        for idx, data in enumerate(details, start=1):
            balance = int(data.balance)
            max_withdraw_limit = int(data.max_w)
            daily_spend = int(data.daily_spend)
            spending = int(data.spending)

            if int(amount) > int(balance):
                return f"Your account balance of {balance} is not enough to transact this amount of {amount}."
            elif amount > max_withdraw_limit:
                return f"You can't withdraw this amount, its exceeding your limit of {data.max_w}"
            elif spending < daily_spend:
                new_balance = int(balance) - int(amount)
                new_spending = int(amount) + int(spending)
                with conn:
                    c.execute('UPDATE customer SET balance = :balance, spending = :spending WHERE customer_id = :customer_id', 
                    {'balance': new_balance, 'spending': new_spending, 'customer_id': customer_id})
                    return f"Success, new account balance {new_balance}."
            else:
                return "You have exceeded you todays amount of transaction"
                # if amount < i:
                #     print(f"You can only withdraw this amount {i}")
                #     ans = input("Do you accept(Y/n): ")
                #     if ans == "Y" or ans == "y":
                #         new_balance = balance - i
        
def make_savings(customer_id: int):
    '''This functions changes an account from standard to a savings'''
    c.execute('select account_type from customer where customer_id = :customer_id', {'customer_id': customer_id})
    account_type = c.fetchone()[0]
    if account_type == "Standard":
        with conn:
            print("We need this information to create a savings account.\n")
            a = "Savings"
            b = input("Enter your daily transaction amount limit: ")
            d = input("Maximum amount you can withdraw: ")

            c.execute('UPDATE customer SET account_type = :account_type, max_w = :max_w, daily_spend = :daily_spend WHERE customer_id = :customer_id', 
            {'account_type': a, 'max_w': d, 'daily_spend': b, 'customer_id': customer_id})
            return f"Success, you account is now a savings account with a daily withdraw limit of {b} and max amount you can withdraw at once is {d}."
    else:
        ans = input("Do you want to change to Standard(Y/N): ")
        if ans == "Y" or ans == "y":
            x = "Standard"
            with conn:
                c.execute('UPDATE customer SET account_type = :account_type WHERE customer_id = :customer_id', {'account_type': x, 'customer_id': customer_id})
                return f"Your account with {customer_id} is now a standard account."


def check_limit(customer_id: int):
    '''This functions checks the limit and prints it to the user'''
    c.execute('select * from customer where customer_id = :customer_id', {'customer_id': customer_id})
    account_info = c.fetchall()
    details = []
    
    for info in account_info:
        details.append(Customer(*info))
    return details