"""
Kelvin's Agent
"""


class Config:
    def __init__(self):
        self.DD_API_KEY = ""
        self.DD_SITE = "datadoghq.com"

    def get_DD_API_KEY(self):
        return self.DD_API_KEY

    def get_DD_SITE(self):
        return self.DD_SITE

    def set_DD_API_KEY(self, api_key):
        self.DD_API_KEY = api_key

config = Config()