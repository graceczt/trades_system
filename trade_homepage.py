import sqlite3
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from db import db, setup # set-up sqlite database
from trade_query import proceed_query_menu # based on query menu option 1
from trade_export import proceed_export_trade_menu # based on export menu option 2
from trade_charts import proceed_chart_menu # based on reporting menu option 3

############################# main menu #########################################################

def exit_program():
    print("Exiting program...")
    quit()

def get_menu_option():
    print("\nTrade System Tools\n------------------------------------------------------")
    for main_key, main_menu_option in menu_option.items():
        print(f"{main_key}: {main_menu_option[0]}")
    choice = input("Please enter an option (1 to 4) in main menu: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > 4:
        print("Please enter in within option 1 to 4 only.")
        return get_menu_option()
    return choice


# using dispatch map dictionary
menu_option = {
    '1': ('Query Menu', proceed_query_menu),
    '2': ('Export Trade Data', proceed_export_trade_menu),
    '3': ('Reporting Menu', proceed_chart_menu ),
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







