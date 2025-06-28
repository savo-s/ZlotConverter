from app.http.api_caller import ApiCaller
from app.http.endpoints.nbp.current_exchange_rates import CurrentExchangeRates


class NbpApiService:

    exchange_rates = None

    def __init__(self):
        self.get_exchange_rates()

    def get_exchange_rates(self):
        self.exchange_rates = ApiCaller.call(CurrentExchangeRates())
        if self.exchange_rates is None:
            raise Exception('Error while obtaining currency data from NBP')

    def get_exchange_currency_codes(self) -> list:
        currency_codes = [rate['code'] for rate in self.response[0]['rates']]
        return currency_codes

    def get_ask_prices(self, code=None) -> float | dict:
        ask_prices = dict((rate['code'], rate['ask']) for rate in self.response[0]['rates'])
        if code is not None:
            return float(ask_prices[code])
        else:
            return ask_prices


if __name__ == "__main__":
    nbp = NbpApiService()
    print(nbp.get_exchange_currency_codes())
    print(nbp.get_ask_prices())
    print(nbp.get_ask_prices('HUF'))





