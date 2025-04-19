from flask import Flask, render_template, request, flash, url_for
from pymongo import MongoClient
import pygal
import csv
import APIConnector
import pandas

#create a Flask object
app = Flask(__name__)

#allow the application to update while the server is running
app.config["DEBUG"] = True

#flash the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

def get_symbols():
    symbols = []
    with open('stocks.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for row in reader:
            symbols = row[0]

    #symbols = pandas.read_csv('stocks.csv')
    return symbols

def get_form_data():
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    time_series = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if not symbol:
        flash('Symbol Name is required.')
    elif not chart_type:
        flash('Chart Type is required.')
    elif not time_series:
        flash('Time Series is required.')
    elif not start_date:
        flash('Start Date is required.')
    elif not end_date:
        flash('End Date is required')

    valid_end_date(start_date,end_date)
    
    return symbol, chart_type, time_series, start_date, end_date

def valid_end_date(start_date, end_date):
    if end_date >= start_date:
        return end_date
    else:
        flash('The End Date cannot be before the Start Date.')

def get_chart(symbol, chart_type, time_series, start_date, end_date):
    if (chart_type == "1"):
        chart = pygal.Bar()
        chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
        chart.x_labels = map(str, range(start_date, end_date))
        chart.add(symbol)
        chart.render()
    elif (chart_type == "2"):
        chart = pygal.Line()
        chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
        chart.x_labels = map(str, range(start_date, end_date))
        chart.add(symbol)
        chart.render()

    return chart.render_data_uri()

@app.route('/', methods=['GET'])
def index_get():
    symbols = get_symbols()
    return render_template("index.html", symbols=symbols)

@app.route('/', methods=['POST'])
def index_post():
    symbols = get_symbols()
    get_form_data()
    chart = get_chart()
    return render_template("index.html", symbols=symbols, chart=chart)

#run the application
app.run(port=5003, debug=True)

#Resources:
#https://www.geeksforgeeks.org/how-to-read-from-a-file-in-python/