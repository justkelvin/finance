#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('finance.db')
c = conn.cursor()

def get_info():
    c.execute('select balance from customer where customer_id = "99643067"')
    balance = c.fetchone()[0]
    print(balance)
get_info()