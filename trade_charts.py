
from db import db
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Implement a “reporting” sub menu which helps to plot charts with the following options:


# 1)	Number of trades per broker (histogram)

# 2)	Share price history for a specified share_id (line chart / connected scatter graph)

# 3)	Proportion of trades traded on each exchange (pie chart)

# 4)	Return to main menu
@db
def trades_per_broker(conn):
    print("showing trades per broker histogram...")
    data = pd.read_sql(""" 
SELECT COUNT(t.trade_id) as number_of_trades, t.broker_id,
 b.first_name || ' ' || b.last_name AS broker_name
FROM trades t
INNER JOIN brokers b on b.broker_id = t.broker_id
GROUP BY t.broker_id, b.first_name, b.last_name; """, conn)
    # display histogram
    # Assuming you have the data in a pandas dataframe called 'data'
    sns.set_palette("husl")  # set color palette
    sns.set_style("whitegrid")  # set style
    # Create a bar plot with broker_name on the x-axis and number_of_trades on the y-axis
    sns.barplot(data=data, x='broker_name', y='number_of_trades', palette='husl')
    # Rotate x-axis labels for readability
    #plt.xticks(rotation=45, ha='right')
    plt.yticks(np.arange(1, 32, 1))
    plt.ylabel("Number of Trades")
    # Display the plot
    plt.show(block=True)
    print("Trades per broker histogram successfully displayed.")

@db
def shareprice_history(conn):
    # ask user for share_id
    share_id = input("Please enter a share_id: ")
    # validate share_id if not share_id does not exist
    if not share_id.isdigit():
        print("Please enter a valid share_id in digits.")
        return shareprice_history()
    # validate share_id if not share_id does not exist
    validate = pd.read_sql(""" SELECT share_id FROM shares; """, conn)
    if not int(share_id) in validate['share_id'].values:
        print(f"Share_id of '{share_id}' does not exist.")
        return shareprice_history()
    # read sql based on share_id
    print(f"Showing share price history line chart on {share_id}... ")
    data = pd.read_sql(f""" SELECT *
FROM shares_prices
WHERE share_id = {share_id};
 """, conn)
    # display connected scatter plot or line chart of data based on share_id
    # display with seaborn
    sns.set_palette("husl")  # set color palette
    sns.set_style("whitegrid")  # set style
    # Create a line plot with time_start and time_end on the x-axis and share_price on the y-axis
    # Convert time_start and time_end to datetime objects
    data['time_start'] = pd.to_datetime(data['time_start'])
    data['time_end'] = pd.to_datetime(data['time_end'])
    # Create the line plot with time_start and time_end as the x-axis and share_price as the y-axis
    # Melt the dataframe to create a new 'time' column
    melted_data = pd.melt(data, id_vars=['price'], value_vars=['time_start', 'time_end'],
                      var_name='time_type', value_name='time')

# Create the line plot with time as the x-axis and share_prices as the y-axis
    sns.lineplot(data=melted_data, x='time', y='price', hue='time_type')
# show selected share_id
    plt.title(f"Share Price History for Share ID '{share_id}'")
# Display the plot
    plt.show(block=True)
    print(f"Share price history for Share ID '{share_id}' line chart successfully displayed.")


@db
def trade_per_exchange(conn):
    print("Showing trades per exchange, pie chart... ")
    data = pd.read_sql("""
SELECT COUNT(t.trade_id) as number_of_trades, se.name || ' ' || se.symbol AS stock_exchange_name
FROM trades t
INNER JOIN
stock_exchanges se
ON t.stock_ex_id = se.stock_ex_id
GROUP BY se.name, se.symbol;""", conn)
    # convert string to float in sql query
    #data['number_of_trades'] = data['number_of_trades'].astype(float)
    # display pie chart
    # Assuming you have the data in a pandas dataframe called 'data'
    sns.set_palette("husl")  # set color palette
    sns.set_style("whitegrid")  # set style
    # Create a pie chart with stock_exchange_name on the x-axis and number_of_trades on the y-axis
    # Group the data by stock_exchange and calculate the total number of trades for each exchange
    exchange_data = data.groupby('stock_exchange_name')['number_of_trades'].sum()
    # Create the pie chart with stock_exchange_name as the labels and number_of_trades as the values
    #sns.pieplot(data=exchange_data, labels=exchange_data['stock_exchange_name'], 
    #        values=exchange_data['number_of_trades'])
    

    # Create the pie chart with stock_exchange_name as the labels and number_of_trades as the values
    plt.pie(exchange_data, labels=exchange_data.index, autopct='%1.1f%%')
# Add a title to the chart
    plt.title('Number of Trades by Stock Exchange')
    # Display the plot
    plt.show(block=True)
    print("Trades per exchange pie chart successfully displayed.")
    
    

def exit_chart_reporting():
    print('Returning to main home page.')
    return True

chart_menu_options = {
    '1': ('Trades per broker', trades_per_broker),
    '2': ('Share Price History', shareprice_history),
    '3': ('Trade Per Exchange', trade_per_exchange),
    '4': ('Exit Chart Reporting Page', exit_chart_reporting),
}

def chart_menu():
    print("\nChart Menu Page\n--------------------------------------------------------------------------")
    for chart_key, chart_menu_option in chart_menu_options.items():
        print(f"{chart_key}: {chart_menu_option[0]}")
    
    chart_choice = input("Please enter an option (1 to 4) for Chart: ")
    if not chart_choice.isdigit() or int(chart_choice) < 1 or int(chart_choice) > 4:
        print("Please enter your chart choice 1 to 4 only.")
        return chart_menu()
    return chart_choice
    

def proceed_chart_menu():
    while True:  
        chart_choice = chart_menu()
        exit = chart_menu_options[chart_choice][1]() 
        if exit:
            break   

proceed_chart_menu()
