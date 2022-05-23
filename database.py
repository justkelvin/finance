#!/usr/bin/env python3

import sqlite3
from typing import List
from datetime import datetime

conn = sqlite3.connect('finance.db')
c = conn.cursor()

def create_table():
    '''Create the sqlite table to store customer data.'''
    c.execute("""CREATE TABLE IF NOT EXISTS customer (
        customer_id integer,
        customer_name text,
        address text,
        contact integer,
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

