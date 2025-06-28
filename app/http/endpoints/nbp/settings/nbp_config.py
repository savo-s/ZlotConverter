from app.http.api_call import ApiCall


class NbpConfig(ApiCall):

    NBP_API_BASE_URL = "https://api.nbp.pl/api/exchangerates/"
    WEIGHT_PER_MIN = 5  # max 5 calls per second

    @staticmethod
    def get_weights_class():
        from app.http.endpoints.nbp.settings.nbp_api_limits import NbpApiLimits
        return NbpApiLimits()







