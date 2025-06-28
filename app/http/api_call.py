

class ApiCall:

    method = None
    url = None
    headers = None

    def get_method(self):
        return self.method

    def get_headers(self):
        return self.headers

    def get_url(self):
        return self.url
