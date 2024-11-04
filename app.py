from flask import Flask, render_template, request, redirect, url_for
from api_service import construct_url, convert_time_series
from graph_generator import generate_graph
import requests
import os

app = Flask(__name__)

# Home page with form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        stock_symbol = request.form.get('stock_symbol')
        chart_type = request.form.get('chart_type')
        time_series_function = request.form.get('time_series')
        begin_date = request.form.get('begin_date')
        end_date = request.form.get('end_date')
        
        # Convert form input to URL parameters
        time_series_name = convert_time_series(time_series_function)
        url = construct_url("https://www.alphavantage.co/query?", time_series_name, stock_symbol, "5min", "QEQT8WNAUX7DRILI")
        
        # Fetch stock data from Alpha Vantage
        try:
            response = requests.get(url)
            response.raise_for_status()
            stock_data = response.json()
            
            # Generate and save graph as SVG
            if not stock_data or "Error Message" in stock_data:
                return "Error fetching stock data: please check the stock symbol and try again."
            else:
                generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date)
                return redirect(url_for('show_graph'))
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching data: {e}"

    # Render the main form page
    return render_template('index.html')

# Route to display the generated graph
@app.route('/graph')
def show_graph():
    if os.path.exists("static/stock_prices_graph.svg"):
        return render_template('graph.html')
    else:
        return "Graph could not be generated."

if __name__ == '__main__':
    app.run(debug=True)
