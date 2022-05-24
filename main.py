#!/usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from model import Customer, Bank, Accounts
from database import bank_details, insert_user, get_all_info, bank_info, transact_withdraw

console = Console()
app = typer.Typer()

@app.command(short_help="Add an account")
def add(customer_name: str, address: str, contact: str, balance: int):
	typer.echo(f"Creating account for {customer_name} with amount {balance}")
	account = Customer(customer_name, address, contact, balance)
	insert_user(account)
	show()

@app.command(short_help="Add Bank details")
def addbank(bank_name: str, bank_location: str, active_customers: str):
	typer.echo(f"Created bank {bank_name} located at {bank_location} with {active_customers} customers")
	bank = Bank(bank_name, bank_location, active_customers)
	bank_details(bank)

@app.command(short_help="Show Bank details")
def bank():
	bank = bank_info()
	console.print("[bold magenta]Bank Details[/bold magenta]!", "💻")

	table = Table(show_header=True, header_style="bold blue")
	table.add_column("#", style="dim", width=6)
	table.add_column("Bank Name", min_width=20)
	table.add_column("Location", min_width=12, justify="right")
	table.add_column("Customers", min_width=12, justify="right")

	for index, info in enumerate(bank, start=1):
		table.add_row(str(index), info.bank_name, info.bank_location, info.active_customers)
	console.print(table)

@app.command(short_help="Withdraw some cash")
def withdraw(customer_id: int, amount: int):
	typer.echo(f"Withdrawing {amount} from account {customer_id}...")
	typer.echo(transact_withdraw(customer_id, amount))


@app.command(short_help="Print all accounts.")
def show():
	account = get_all_info()
	console.print("[bold magenta]Customer Details[/bold magenta]!", "💻")

	table = Table(show_header=True, header_style="bold blue")
	table.add_column("#", style="dim", width=6)
	table.add_column("Customer ID", min_width=12, justify="right")
	table.add_column("Name", min_width=20)
	table.add_column("Address", min_width=12, justify="right")
	table.add_column("Contact", min_width=12, justify="right")
	table.add_column("Balance", min_width=12, justify="right")
	table.add_column("Account Type", min_width=12, justify="right")
	table.add_column("Date Created", min_width=12, justify="right")
	table.add_column("Status", min_width=12, justify="right")

	def get_category_color(category):
		'''Return a color from a predifined set, you can add more below'''
		COLORS = {'Active': 'Cyan', 'Disabled': 'red'}
		if category in COLORS:
			return COLORS[category]
		return 'white'
	
	for idx, info in enumerate(account, start=1):
		c = get_category_color(info.account_type)
		is_active = 'Active ✅' if info.status == "1" else 'Disabled ❌'
		table.add_row(str(idx), info.customer_id, info.customer_name, info.address, info.contact, info.balance, info.account_type, info.date_created, is_active)
	console.print(table)

if __name__ == "__main__":
	app()