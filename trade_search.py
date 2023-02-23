import datetime
import pandas as pd

from db import db

# Phase 2

# Implement a “query” sub menu with the following options:

# 1)	List Brokers         #at trade_query.py

# 2)	List all Shares (should include company name)      # at trade_query.py

# 3)	Lookup trade by trade id (shows all trade details) # at trade_query.py

# 4)	Search for trade (specifying one or more of the following: share_id, broker_id, date_range)

# 5)	Return to main menu # at trade_query.py

############################# query option 4 menu #########################################################

trade_search_parameters = {
    'broker_id': None,
    'share_id': None,
    'date_from': None,
    'date_to': None
}

def set_broker_id():
    broker_id = input("Please enter broker id: ")
    if broker_id == '':
        trade_search_parameters['broker_id'] = None
        return
    if not broker_id.isdigit():
        print("Please enter broker id in digit only.")
        return set_broker_id()  
    trade_search_parameters['broker_id'] = broker_id
    

def set_share_id():
    share_id = input("Please enter share id: ")
    if share_id == '':
        trade_search_parameters['share_id'] = None
        return
    if not share_id.isdigit():
        print("Please enter share id in digit only.")
        return set_share_id()  
    trade_search_parameters['share_id'] = share_id

def set_date_from():
    # date format: YYYY-MM-DD
    date_from = input("Please enter date from (YYYY-MM-DD): ")
    if date_from == '':
        trade_search_parameters['date_from'] = None
        return
    try:
        datetime.datetime.strptime(date_from, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return set_date_from()
    trade_search_parameters['date_from'] = date_from

def set_date_to():
    # date format: YYYY-MM-DD
    date_to = input("Please enter date to (YYYY-MM-DD): ")
    if date_to == '':
        trade_search_parameters['date_to'] = None
        return
    try:
        datetime.datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return set_date_to()
    trade_search_parameters['date_to'] = date_to    

@db
def search(conn):
    # generate WHERE clause dynamically from search parameters
    where_clause = []
    for key, value in trade_search_parameters.items():
        if value is not None:
            # if date_from or date_to is set, we need to convert it to datetime
            # then we can search for trades between two dates
            if key == 'date_from' or key == 'date_to':
                value = f"datetime('{value}')"
                if key == 'date_from':
                    where_clause.append(f"transaction_time >= {value}")
                else:
                    where_clause.append(f"transaction_time <= {value}")
            else:
                where_clause.append(f"{key} = {value}")
    # if no search parameters are set, we don't want to search for all trades
    if len(where_clause) == 0:
        print("No search parameters set.")
        return
    where_clause = " AND ".join(where_clause)
    # pefrom search to find matching trades
    trades = pd.read_sql(f"SELECT * FROM trades WHERE {where_clause}", conn)
    print(trades)

def back():
    print("Going back to query menu...")
    return True

search_trade_menu_options = {
    '1': ('Set Broker id', set_broker_id),
    '2': ('Set share id', set_share_id),
    '3': ('Set date_from', set_date_from),
    '4': ('Set date_to', set_date_to),
    '5': ('Search', search),
    '6': ('Back', back)
}

def search_trade_menu():
    print("\nSearch Trade Menu Page\n--------------------------------------------------------------------------")
    for search_trade_key, search_trade_menu_option in search_trade_menu_options.items():
        print(f"{search_trade_key}: {search_trade_menu_option[0]}")
    
    # print search parameters
    print(f"Search parameters: {[i for i in trade_search_parameters.items() if i[1] is not None]}")

    #print("1) Set Broker id\n2) Set share id\n3) Set daterange\n4) Search\n5) Back")
    search_trade_choice = input("Please enter an option (1 to 6) in Search Trade Menu: ")
    if not search_trade_choice.isdigit() or int(search_trade_choice) < 1 or int(search_trade_choice) > 6:
        print("Please enter your search trade choice 1 to 6 only.")
        return search_trade_menu()
    return search_trade_choice

def proceed_search_trade_menu():
    # reset search parameters
    for key in trade_search_parameters.keys():
        trade_search_parameters[key] = None
    while True:
        search_trade_choice = search_trade_menu()
        #for choice in menu_option:
        exit = search_trade_menu_options[search_trade_choice][1]() 
        if exit:
            break
