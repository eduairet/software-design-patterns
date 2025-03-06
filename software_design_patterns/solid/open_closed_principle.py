import requests
from enum import Enum


class Currency(Enum):
    USD = "usd"
    EUR = "eur"


class TokenType(Enum):
    CRYPTO = "crypto"
    STABLECOIN = "stablecoin"
    MEME = "meme"


class Token(Enum):
    BTC = {"id": "bitcoin", "type": TokenType.CRYPTO}
    ETH = {"id": "ethereum", "type": TokenType.CRYPTO}
    PEPE = {"id": "pepe", "type": TokenType.MEME}
    WIF = {"id": "dogwifcoin", "type": TokenType.MEME}
    USDC = {"id": "usd-coin", "type": TokenType.STABLECOIN}
    USDT = {"id": "tether", "type": TokenType.STABLECOIN}


class TokenPriceApi:
    """
    Token price API client.

    Attributes:
    - api_url: The base URL of the API
    """

    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_api_url(self, tokens: list, currencies: list = [Currency.USD]):
        """
        Get the API URL for the given tokens and currencies.
        """
        pass

    def get_token_prices(self, tokens: list, currencies: list = [Currency.USD]):
        """
        Get the prices of the given tokens in the given currencies.
        """
        pass


class CoinGeckoFreeApi(TokenPriceApi):
    """
    CoinGecko API client.

    Attributes:
    - api_url: The base URL of the free CoinGecko API
    - headers: The headers to send with the requests.
    """

    def __init__(self):
        super().__init__("https://api.coingecko.com/api/v3/simple/price")
        self.headers = {"accept": "application/json"}

    def get_api_url(self, tokens: list, currencies: list = [Currency.USD]):
        tokens_ids = ",".join([token.value["id"] for token in tokens])
        currencies = ",".join([currency.value for currency in currencies])
        return f"{self.api_url}?ids={tokens_ids}&vs_currencies={currencies}"

    def get_token_prices(self, tokens: list, currencies: list = [Currency.USD]):
        api_url = self.get_api_url(tokens, currencies)
        response = requests.get(api_url, headers=self.headers)
        return response.json()


class Specification:
    def is_satisfied(self, item):
        pass

    def __and__(self, other: "Specification"):
        return AndSpecification(self, other)


class Filter:
    def filter(self, items, spec):
        pass


class TokenSpecification(Specification):
    def __init__(self, token: Token):
        self.token = token

    def is_satisfied(self, item):
        return item == self.token


class TokenTypeSpecification(Specification):
    def __init__(self, token_type: TokenType):
        self.token_type = token_type

    def is_satisfied(self, item):
        return item == self.token_type


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(lambda spec: spec.is_satisfied(item), self.args))


class Filter(Filter):
    def filter(self, items, spec):
        return [item for item in items if spec.is_satisfied(item)]
