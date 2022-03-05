import requests
import json
from config import currency


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"It is impossible to convert to the same currency {base}")

        try:
            quoter = currency[quote]
        except KeyError:
            raise ConvertionException(f"Error in processing currency {quote}")

        try:
            baser = currency[base]
        except KeyError:
            raise ConvertionException(f"Error in processing currency {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Error in processing amount {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quoter}&tsyms={baser}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base