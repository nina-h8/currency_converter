# Simple currency converter #

This tool converts amounts among 32 most common currencies using either 3-letter code or the currency symbol.
Currencies exchange rates are taken from [RATES API](https://ratesapi.io/). The converted amount is rounded respective to the decimal places given as input amount.

## Functionality ##
As one symbol might match mutliple currencies (e.g. ¥ stands for CNY as well as JPY), rates for all of them are reported.
If output currency is not specified it converts to all known currencies.
If unknown code or symbol is given, error will be thrown.

## Suported currencies ## 
 ... and their corresponding symbols:

		AUD	$
		BGN	лв
		BRL	R$
		CAD	C$
		CHF	CHF
		CNY	¥
		CZK	Kč
		DKK	kr
		EUR	€
		GBP	£
		HKD	HK$
		HRK	kn
		HUF	Ft
		IDR	Rp
		ILS	₪
		INR	Rs.
		ISK	kr
		JPY	¥
		KRW	₩
		MXN	$
		MYR	RM
		NOK	kr
		NZD	$
		PHP	₱
		PLN	zł
		RON	L
		RUB	руб
		SEK	kr
		SGD	S$
		THB	฿
		TRY	YTL
		ZAR	R
		
## Dependencies ##
 * python3.x

## Input parameters ##
 * required
 
		--amount [float]
		--input_currency [str]
 * optional
 
		--output_currency [str]
	


## Output ##
 * json string

		{
			"input": { 
				"amount": <float>,
				"currency": <3 letter currency code>
			}
			"output": {
				<3 letter currency code>: <float>
			}
		}


 
## Usage ##
 * **CLI**
 
		./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
		{
			"input": {
				"amount": 0.9,
				"currency": "CNY"
			},
			"output": {
				"AUD": 0.2
			}
		},
		{
			"input": {
				"amount": 0.9,
				"currency": "JPY"
			},
			"output": {
				"AUD": 0.0
			}
		}

 * **API**
 
		./api.py
 
	
 

