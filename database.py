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


def insert_user(todo: Accounts):
    '''Insert data to the database'''
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0

    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
                  {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added, 'date_completed': todo.date_completed,
                   'status': todo.status, 'position': todo.position})


def get_all_info():
    pass