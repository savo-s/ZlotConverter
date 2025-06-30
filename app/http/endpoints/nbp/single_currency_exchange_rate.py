from app.http.endpoints.nbp.settings.nbp_api_limits import NbpApiLimits
from app.http.endpoints.nbp.settings.nbp_config import NbpConfig


class SingleCurrencyExchangeRate(NbpConfig):

    method = "GET"
    route = "rates"
    weight = 1

    def __init__(self, currency: str, table: str = "C", json=True):

        super().__init__()

        if table not in ['A', 'B', 'C']:
            raise Exception("Table is a mandatory parameter and should one of the letters 'A', 'B' or 'C'")
        else:
            self.url = f"{self.NBP_API_BASE_URL}/{self.route}/{table}/{currency}{'/?format=json' if json else ''}"

        NbpApiLimits().add_weight(self.weight)
