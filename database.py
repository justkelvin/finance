#!/usr/bin/env python3

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
        customer_id text,
        max_weekly_spend text
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
    count = c.fetchone()[0]
    accounts.customer_id = count if count else 0

    with conn:
        c.execute('INSERT INTO customer VALUES (:customer_name, :address, :contact, :balance, :account_type, :date_created, :customer_id)',
                  {'customer_name': accounts.customer_name, 'address': accounts.address, 'contact': accounts.contact,
                   'balance': accounts.balance, 'account_type': accounts.account_type, 'date_created': accounts.date_created, 'customer_id': accounts.customer_id})

def get_all_info() -> List[Customer]:
    '''Fetch all data from the databse and return it as a list'''
    c.execute('select * from customer')
    results = c.fetchall()
    customer = []

    for result in results:
        customer.append(Customer(*result))
    return customer

