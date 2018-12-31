#!/usr/bin/env python3

import currency_converter
from flask import Flask, request

app = Flask(__name__)

@app.route('/currency_converter')
def my_route():
  amount = request.args.get('amount', type=float)
  input_currency = request.args.get('input_currency', type=str)
  output_currency = request.args.get('output_currency', type=str)
  return currency_converter.convert(amount, input_currency, output_currency)


if __name__ == '__main__':
     app.run()

