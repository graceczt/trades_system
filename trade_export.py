import datetime
import pandas as pd

from db import db

trade_export_parameters = {
    'broker_id': None,
    'share_id': None,
    'date_from': None,
    'date_to': None
}

def set_broker_id():
    broker_id = input("Please enter broker id: ")
    if broker_id == '':
        trade_export_parameters['broker_id'] = None
        return
    if not broker_id.isdigit():
        print("Please enter broker id in digit only.")
        return set_broker_id()  
    trade_export_parameters['broker_id'] = broker_id
    

def set_share_id():
    share_id = input("Please enter share id: ")
    if share_id == '':
        trade_export_parameters['share_id'] = None
        return
    if not share_id.isdigit():
        print("Please enter share id in digit only.")
        return set_share_id()  
    trade_export_parameters['share_id'] = share_id

def set_date_from():
    # date format: YYYY-MM-DD
    date_from = input("Please enter date from (YYYY-MM-DD): ")
    if date_from == '':
        trade_export_parameters['date_from'] = None
        return
    try:
        datetime.datetime.strptime(date_from, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return set_date_from()
    trade_export_parameters['date_from'] = date_from

def set_date_to():
    # date format: YYYY-MM-DD
    date_to = input("Please enter date to (YYYY-MM-DD): ")
    if date_to == '':
        trade_export_parameters['date_to'] = None
        return
    try:
        datetime.datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return set_date_to()
    trade_export_parameters['date_to'] = date_to    

@db
def export(conn):
    # generate WHERE clause dynamically from search parameters
    where_clause = []
    for key, value in trade_export_parameters.items():
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
    # if no export parameters are set, we don't want to search for all trades
    if len(where_clause) == 0:
        print("No search parameters set.")
        return
    where_clause = " AND ".join(where_clause)
    # perform search to find matching trades
    trades = pd.read_sql(f"SELECT * FROM trades WHERE {where_clause}", conn)
    # ask user on csv name to export
    csv_name = input("Please enter csv name to export: ")
    if csv_name == '':
        csv_name = 'trades.csv'
    else:
        csv_name = f"{csv_name}.csv"
    # export trades to excel file
    print(f"Exporting {len(trades)} trades to {csv_name}...")

    trades.to_csv(csv_name, index=False)

def back():
    print("Going back to query menu...")
    return True

export_trade_menu_options = {
    '1': ('Set Broker id', set_broker_id),
    '2': ('Set share id', set_share_id),
    '3': ('Set date_from', set_date_from),
    '4': ('Set date_to', set_date_to),
    '5': ('Export', export),
    '6': ('Back', back)
}

def export_trade_menu():
    print("\nExport Trade Menu Page\n--------------------------------------------------------------------------")
    for export_trade_key, export_trade_menu_option in export_trade_menu_options.items():
        print(f"{export_trade_key}: {export_trade_menu_option[0]}")
    
    # print export parameters
    print(f"Export parameters: {[i for i in trade_export_parameters.items() if i[1] is not None]}")

    #print("1) Set Broker id\n2) Set share id\n3) Set daterange\n4) Export\n5) Back")
    export_trade_choice = input("Please enter an option (1 to 6) in Export Trade Menu: ")
    if not export_trade_choice.isdigit() or int(export_trade_choice) < 1 or int(export_trade_choice) > 6:
        print("Please enter your search trade choice 1 to 6 only.")
        return export_trade_menu()
    return export_trade_choice

def proceed_export_trade_menu():
    # reset search parameters
    for key in trade_export_parameters.keys():
        trade_export_parameters[key] = None
    while True:
        export_trade_choice = export_trade_menu()
        #for choice in menu_option:
        exit = export_trade_menu_options[export_trade_choice][1]() 
        if exit:
            break
