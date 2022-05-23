#!/usr/bin/env python3

import sqlite3
from typing import List
from datetime import datetime

from model import Accounts

conn = sqlite3.connect('finance.db')
c = conn.cursor()

def create_table():
    '''Create the sqlite table to store customer data.'''
    c.execute("""CREATE TABLE IF NOT EXISTS customer (
        customer_id integer,
        customer_name text,
        address text,
        contact text,
        balance integer
        account_type text,
        date_created text,
        position integer
    )""")

create_table()

def create_bank_table():
    '''Create bank details'''
    c.execute("""CREATE TABLE IF NOT EXISTS bank (
        bank_name text,
        bank_location text,
        active_customers integer
    )""")

create_bank_table()

def create_accounts():
    '''Creating customer accounts'''
    c.execute("""CREATE TABLE IF NOT EXISTS accounts (
        account_number int,
        customer_id integer,
        last_transaction text,
        account_age text,
        account_type text
    )""")

create_accounts()


def insert_user(accounts: Accounts):
    '''Insert data to the database'''
    c.execute('select count(*) FROM customer')
    count = c.fetchone()[0]
    accounts.position = count if count else 0

    with conn:
        c.execute('INSERT INTO customer VALUES (:customer_id, :customer_name, :address, :contact, :balance, :account_type, :date_created, :position)',
                  {'customer_id': accounts.customer_id, 'customer_name': accounts.customer_name, 'address': accounts.address, 'contact': accounts.contact,
                   'balance': accounts.balance, 'account_type': accounts.account_type, 'date_created': accounts.date_created, 'position': accounts.position})


def get_all_accounts() -> List[Accounts]:
    '''Fetch all data from the databse and return it as a list'''
    c.execute('select * from customer')
    results = c.fetchall()
    customer = []

    for result in results:
        customer.append(Accounts(*result))
    return customer