import urllib.request
from urllib.parse import urlencode


class UniApi():
    """
    Run api requests
    """
    API_BASE_DOMAIN = 'https://api.unisender.com/ru/api/'

    def __init__(self, api_key):
        self.api_key = api_key

    def run(self, method, options_dict):
        url = self.API_BASE_DOMAIN + method + "?format=json&api_key=" + self.api_key

        if options_dict:
            url = url + "&" + urlencode(options_dict)
        f = urllib.request.urlopen(url)

        return f.read().decode('utf-8')