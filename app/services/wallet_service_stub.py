from app.services.nbp_api_service import NbpApiService


class WalletServiceStub:

    def __init__(self):
        # self.current_user_id = <- get current (logged) user id
        nbp = NbpApiService()
        self.exchange_rates = nbp.get_exchange_rates()  # exchange rates are for Polish PLN
        self.currency_codes = nbp.get_exchange_currency_codes()
        self.ask_prices = nbp.get_ask_prices()

    def get_my_wallet(self):
        # get all currency/amount pairs from DB for current user as a dictionary,
        # calculate total_amount as sum of all amounts multiplied by related ask price for related currency
        # return as a dictionary all currency/amount pairs, and total/total_amount pair
        pass

    def add_currency_amount(self, currency: str, amount: int):
        # check if currency exists in self.currencies. If not, return error 'currency does not exist on exchange'
        # if there is no currency in database for current user, create one with that amount
        # add amount to existing currency amount for current user, and return pair currency/amount with new amount as dictionary
        pass

    def sub_currency_amount(self, currency: str, amount: int):
        # check if currency exists in self.currencies. If not, return error 'currency does not exist on exchange'
        # sub amount from existing currency for current user, and return pait currency/amount with new amount as dictionary
        # check if result is below zero - return an error that there are insufficient funds for that currency
        # if result is zero, delete that currency for that user from database
        pass

    def delete_currency(self, currency: str):
        # check if currency exists in self.currencies. If not, return error 'currency does not exist on exchange'
        # check if currency exists in user's wallet. If not, return error 'User has zero balance for {currency} currency"
        # delete row with currency for current user in database
        pass



