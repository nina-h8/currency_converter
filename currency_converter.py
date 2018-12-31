#!/usr/bin/env python3

from collections import defaultdict
import requests
import decimal
import json
	

def convert(AMOUNT, IN_CURRENCY, OUT_CURRENCY):
	
	# create symbol-codes dictionary 
	symbol_code_dict = get_currencies_dict()
	
	# get input currency code
	cur_code_in = get_cur_code(IN_CURRENCY, symbol_code_dict)
	
	# if no output_currency parameter given, take all available currencies
	if OUT_CURRENCY is None:
		cur_code_out = symbol_code_dict.values()
		cur_code_out = [item for sublist in cur_code_out for item in sublist]
	else:
		# get output currency code
		cur_code_out = get_cur_code(OUT_CURRENCY, symbol_code_dict)

	if cur_code_in is None or cur_code_out is None:
		raise ValueError('UNSUPPORTED CURRENCY')
	
	# get current rates using rates API
	json_final = None	
	for single_code_in in cur_code_in:
		params = dict(
			base=single_code_in,
			symbols=",".join(cur_code_out)
		)
		url = 'https://ratesapi.io/api/latest'
		resp = requests.get(url=url, params=params)
		data = resp.json()
		all_rates = data['rates']
		json_partial = create_converted_json(AMOUNT, single_code_in, all_rates)
		# join partial json outputs in case of ambiguous input currency symbol corresponding to multiple currencies
		json_final = ",\n".join(filter(None,[json_final, json_partial]))

	return(json_final)
	
def get_cur_code(CURRENCY, symbol_code_dict):
	''' Get the currency code, return None if not available'''
	for symbol, code in symbol_code_dict.items():
		if CURRENCY in symbol:
			return symbol_code_dict[CURRENCY]
		elif CURRENCY in code:
			return [CURRENCY]
	return None


def create_converted_json(AMOUNT, single_code_in, all_rates):
	''' Get json formatted output for single input currency '''
	json_template = defaultdict(dict)
	json_template['input']['amount'] = AMOUNT
	json_template['input']['currency'] = single_code_in
	
	for single_code_out, rate in all_rates.items():
		decimal_places = abs(decimal.Decimal(str(AMOUNT)).as_tuple().exponent)
		output_amount = round(AMOUNT*rate, decimal_places)
		json_template['output'][single_code_out] = output_amount
	json_partial = json.dumps(json_template, sort_keys=True, indent=4, separators=(',', ': '))	
	return json_partial


def get_currencies_dict():
	''' Create symbol-codes dictionary - multiple codes allowed for a single symbol'''
	symbol_code_dict = defaultdict(list)
	with open("currency_symbols_table.csv", "r", encoding='utf-8') as cur_tbl:
		for line in cur_tbl:
			line = line.rstrip()
			code = line.split("\t")[0]
			symbol= line.split("\t")[1]
			symbol_code_dict[symbol].append(code) 
	return symbol_code_dict


def main(args):
	
	AMOUNT = args.amount
	IN_CURRENCY = args.input_currency
	OUT_CURRENCY = args.output_currency
	
	json_final = convert(AMOUNT, IN_CURRENCY, OUT_CURRENCY)
	print(json_final)
	

if __name__ == "__main__":
    import argparse	
    
    parser = argparse.ArgumentParser()
    parser.add_argument( '--amount', type=float, required=True,
						help='Amount which we want to convert')
    parser.add_argument('--input_currency', type=str, required=True,
						help='Input currency - 3 letters name or currency symbol')
    parser.add_argument('--output_currency', type=str,
						help='Requested/output currency - 3 letters or currency symbol')
  
    args = parser.parse_args()
    main(args)
