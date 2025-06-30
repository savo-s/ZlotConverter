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
