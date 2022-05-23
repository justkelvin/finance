#!/usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from model import Customer, Bank, Accounts
from database import insert_user, get_all_info

console = Console()
app = typer.Typer()

@app.command(short_help="Add an account")
def add(customer_id: int, customer_name: str, address: str, contact: str, balance: int):
	typer.echo(f"Creating account with id {customer_id}, for {customer_name} with amount {balance}")
	account = Accounts(customer_id, customer_name, address, contact, balance)
	insert_user(account)
	show()





@app.command(short_help="Print all tasks.")
def show():
	account = get_all_info()

if __name__ == "__main__":
	app()