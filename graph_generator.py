import pygal
import datetime

def generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date, filename):
    """Generates and saves a graph as an SVG file based on the stock data and user inputs."""
    
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
    
    for date_str, data in time_series.items():
        dates.append(date_str)
        try:
            prices.append(float(data['1. open']))
        except KeyError:
            print(f"Missing '1. open' data for date: {date_str}")
    
    # Create the graph
    if chart_type == "1":
        graph = pygal.Bar()
        graph.title = f"{stock_symbol} Stock Prices (Bar Graph)"
    else:
        graph = pygal.Line()
        graph.title = f"{stock_symbol} Stock Prices (Line Graph)"
    
    graph.x_labels = dates
    graph.add('Opening Price', prices)
    graph.render_to_file(filename)
