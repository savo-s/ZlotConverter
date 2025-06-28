import requests


class ApiCaller:

    @staticmethod
    def call(api_call):

        weights_manager = api_call.get_weights_class()

        if weights_manager.is_in_rate_limits():
            response = requests.request(
                method=api_call.get_method(),
                url=api_call.get_url(),
                headers=api_call.get_headers()
            )
            return response.json()

        else:
            print("API limits exceeded! Please wait and then try again.")


if __name__ == "__main__":
    from app.http.endpoints.nbp.current_exchange_rates import CurrentExchangeRates
    import time
    for i in range(0, 7):
        _response = ApiCaller.call(CurrentExchangeRates())
        print(_response)
    time.sleep(60)
    for i in range(0, 7):
        _response = ApiCaller.call(CurrentExchangeRates())
        print(_response)
