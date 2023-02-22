import sqlite3
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from db import db, setup
from trade_search import proceed_search_trade_menu
from trade_export import proceed_export_trade_menu


@db
def list_brokers(conn):
# Query database
    brokers = pd.read_sql("SELECT * FROM brokers", conn)
    print(brokers)

@db
def list_shares(conn):
        shares = pd.read_sql("""
select s.share_id, sp.price,cs.name as currency_name, c.name as company, sp.time_start as share_price_start, sp.time_end as share_price_end
from shares s
inner join
shares_prices sp
on s.share_id = sp.share_id
inner join 
companies c
on s.company_id = c.company_id
inner join
currencies cs
on s.currency_id = cs.currency_id;""", conn)
        print(shares)

@db
def trade_details(conn):
    
    trade_id = input("Please enter trade_id to search: ")
    if not trade_id.isdigit():
        print("Only single digits to enter Trade_id.") 
        return trade_details(conn)

    if len(trade_id) >1:
        print("Trade_id is valid for 1 digit only.")
        return trade_details(conn)
    trades_full = pd.read_sql(f"SELECT * FROM trades WHERE trade_id={trade_id}", conn)
    print("finding trade_details by trade_id...")
    print(trades_full)


def exit_query():
    print("Going to homepage menu.")
    return get_menu_option()



def reporting():
    print("\nReporting Menu Page\n--------------------------------------------------------------------------")
    for reporting_key, reporting_menu_option in reporting_option.items():
        print(f"{reporting_key}: {reporting_menu_option[0]}")
    
    reporting_choice = input("Please enter an option (1 to 4) for Reporting: ")
    if not reporting_choice.isdigit() or int(reporting_choice) < 1 or int(reporting_choice) > 4:
        print("Please enter your reporting choice 1 to 4 only.")
        return reporting()
    return reporting_choice
    #print("Generating reports...")

def proceed_reporting_menu():
    while True:
         
        reporting_choice = reporting()
        #for choice in menu_option:
        exit = reporting_option[reporting_choice][1]() 
        if exit:
            break



def exit_program():
    print("Exiting program...")
    quit()

def trades_per_broker():
    print("showing trades per broker histogram...")

def shareprice_history():
    print("Showing share price history line chart or connect scatter plot ")

def trade_exchange():
    print("Showing trades per exchange, pie chart ")

def exit_reporting():
    print('Returning to main home page.')
    return True

reporting_option = {
    '1': ('Trades per broker', trades_per_broker),
    '2': ('Share Price History', shareprice_history),
    '3': ('Trade Exchange', trade_exchange),
    '4': ('Exit Reporting Page', exit_reporting),
}


def get_menu_option():
    print("\nTrade System Tools\n------------------------------------------------------")
    for main_key, main_menu_option in menu_option.items():
        print(f"{main_key}: {main_menu_option[0]}")

    #print("1) Query\n2) Export trade data\n3) Reporting\n4) Exit")
    choice = input("Please enter an option (1 to 4) in main menu: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > 4:
        print("Please enter in within option 1 to 4 only.")
        return get_menu_option()
    return choice


# using dispatch map dictionary on query option
query_option = {
    '1': ('Brokers List', list_brokers),
    '2': ('Full Shares details', list_shares),
    '3': ('Full Trade details', trade_details),
    '4': ('Trade Search', proceed_search_trade_menu),
    '5': ('Exit Query Page', exit_query)
}

def query_menu():
    print("\nQuery Menu Page\n--------------------------------------------------------------------------")
    for query_key, query_menu_option in query_option.items():
        print(f"{query_key}: {query_menu_option[0]}")

    #print("1) List Brokers\n2) List all Shares (include company name)\n3) Lookup trade by trade_id (show all trade details)\n4) Trade Search\n5) Return to main home menu")
    query_choice = input("Please enter an option (1 to 5) in Query: ")
    if not query_choice.isdigit() or int(query_choice) < 1 or int(query_choice) > 5:
        print("Please enter your query choice 1 to 5 only.")
        return query_menu()
    return query_choice

def proceed_query_menu():
    while True:
        query_choice = query_menu()
        #for choice in menu_option:
        exit = query_option[query_choice][1]() 
        if exit:
            break 


# using dispatch map dictionary
menu_option = {
    '1': ('Query Menu', proceed_query_menu),
    '2': ('Export Trade Data', proceed_export_trade_menu),
    '3': ('Reporting Menu', proceed_reporting_menu ),
    '4': ('Exit Home Page', exit_program)
}

def proceed_menu():
    while True:
        choice = get_menu_option()
        menu_option[choice][1]() 


def main():
    setup()
    proceed_menu()



if __name__ == '__main__':
    main()







