import pygal
from lxml import etree
import datetime
import webbrowser

def generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date):
    """Generates and displays a graph based on the stock data and user inputs."""
    
    # Prep data
    dates = []
    prices = []

    # Determine the time series to use
    if 'Time Series (5min)' in stock_data: 
        time_series = stock_data['Time Series (5min)']
    elif 'Time Series (Daily)' in stock_data:
        time_series = stock_data['Time Series (Daily)']
    elif 'Weekly Time Series' in stock_data:
        time_series = stock_data['Weekly Time Series']
    elif 'Monthly Time Series' in stock_data:
        time_series = stock_data['Monthly Time Series']
    else:
        print("No valid time series found in the stock data.")
        return
    
    # Filter data by date range
    for date_str, data in time_series.items():
        
        #date = datetime.strptime(date_str, '%Y-%m-%d')
        
        #if begin_date <= date <= end_date:
        dates.append(date_str)
        #print(date_str)
        try:
                prices.append(float(data['1. open']))  # Change this to the price you want to plot
                print(prices)
        except KeyError:
                print(f"Missing '1. open' data for date: {date_str}")
    
    # Generate the graph
    if chart_type == "1":
        graph = pygal.Bar()
        graph.title = f"{stock_symbol} Stock Prices (Bar Graph)"
    else:
        graph = pygal.Line()
        graph.title = f"{stock_symbol} Stock Prices (Line Graph)"

    # Set x_labels and add data
    graph.x_labels = dates
    graph.add('Opening Price', prices)

    # Save the graph
    graph.render_to_file('stock_prices_graph.svg')

    # Open the graph in the default web browser
    webbrowser.open('stock_prices_graph.svg')
