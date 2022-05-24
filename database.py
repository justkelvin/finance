#!/usr/bin/env python3

from random import randint
import sqlite3
from typing import List
from datetime import datetime

from numpy import greater
from sympy import LessThan
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
        max_weekly_spend text,
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
        c.execute('INSERT INTO customer VALUES (:customer_name, :address, :contact, :balance, :account_type, :date_created, :max_w, :daily_spend, :max_weekly_spend, :customer_id, :status)',
                  {'customer_name': accounts.customer_name, 'address': accounts.address, 'contact': accounts.contact,
                   'balance': accounts.balance, 'account_type': accounts.account_type, 'date_created': accounts.date_created, 'max_w': accounts.max_w, 'daily_spend': accounts.daily_spend, 'max_weekly_spend': accounts.max_weekly_spend, 'customer_id': accounts.customer_id, 'status': accounts.status})

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
        if int(amount) < int(balance):
            with conn:
                c.execute('UPDATE customer SET balance = :balance WHERE customer_id = :customer_id', {'balance': new_balance, 'customer_id': customer_id})
                return f"Success, new account balance {new_balance}."
        else:
            return f"Your account balance of {balance} is not enough to transact this amount of {amount}."
    else:
        """Check the transaction limit and amount they are transacting"""
        c.execute('select max_w from customer where customer_id = :customer_id', {'customer_id': customer_id})
        max_w = c.fetchone()[0]
        c.execute('select max_weekly_spend from customer where customer_id = :customer_id', {'customer_id': customer_id})
        max_weekly_spend = c.fetchone()[0]
        if int(amount) > int(balance):
            print(f"The amount exceeds your max withdraw limit of {max_w}.")
            quit()
        
