import sqlite3
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from db import db # set-up sqlite database
from trade_search import proceed_search_trade_menu # based on query menu option 1 and sub menu option 4


############################# query menu #########################################################
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
    return True

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