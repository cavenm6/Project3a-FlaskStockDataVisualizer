from flask import Flask, render_template, request, redirect, url_for
import requests
import csv
from datetime import datetime
from api_service import construct_url, convert_time_series, BASE_URL, INTERVAL, API_KEY
from graph_generator import generate_graph

app = Flask(__name__)

# Load stock symbols from CSV file
def load_stock_symbols():
    symbols = []
    with open('stocks.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for row in csvreader:
            symbols.append(row[0])  # Assuming the symbol is in the first column
    return symbols

# Store stock symbols globally
stock_symbols = load_stock_symbols()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol")
        chart_type = request.form.get("chart_type")
        time_series = request.form.get("time_series")
        begin_date = request.form.get("begin_date")
        end_date = request.form.get("end_date")

        print(f"Selected Stock Symbol: {stock_symbol}")  # Debugging line
        time_series_name = convert_time_series(time_series)
        url = construct_url(BASE_URL, time_series_name, stock_symbol, INTERVAL, API_KEY)
        print(f"Constructed URL: {url}")  # Debugging line

        try:
            response = requests.get(url)
            response.raise_for_status()
            stock_data = response.json()

            if not stock_data or "Error Message" in stock_data:
                print(f"API Response: {stock_data}")  # Print response for debugging
                return "Error fetching stock data: please check the stock symbol and try again."
            else:
                generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date)
                return redirect(url_for('show_graph'))

        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching data: {e}"

    return render_template("index.html", stock_symbols=stock_symbols)

@app.route("/graph")
def show_graph():
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(debug=True)
