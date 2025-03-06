import os
from shared.constants.paths import TESTS_FILES_DIR
from software_design_patterns.solid.single_responsibility_principle import *
from software_design_patterns.solid.open_closed_principle import *


def test_single_responsibility_principle():
    EXPECTED_JOURNAL_CONTENT_EMPTY = "0: I cried today.\n1: I ate a bug."
    EXPECTED_JOURNAL_CONTENT_FILLED = (
        "0: I bought a cookie.\n1: I saw a cat.\n2: I pet a dog."
    )
    JOURNAL_FILE = "journal.txt"
    JOURNAL_FILE_PATH = os.path.join(TESTS_FILES_DIR, JOURNAL_FILE)

    journal_empty = Journal()

    journal_empty.add_entry("I cried today.")
    journal_empty.add_entry("I ate a bug.")

    assert str(journal_empty) == EXPECTED_JOURNAL_CONTENT_EMPTY
    assert journal_empty.count == 2

    PersistenceManager.save_to_file(journal_empty, JOURNAL_FILE_PATH)
    assert os.path.exists(JOURNAL_FILE_PATH)

    with open(JOURNAL_FILE_PATH, "r") as file:
        assert file.read() == EXPECTED_JOURNAL_CONTENT_EMPTY

    os.remove(JOURNAL_FILE_PATH)
    assert not os.path.exists(JOURNAL_FILE_PATH)

    journal_filled = Journal(["I bought a cookie.", "I saw a cat.", "I pet a dog."])

    assert str(journal_filled) == EXPECTED_JOURNAL_CONTENT_FILLED
    assert journal_filled.count == 3

    journal_filled.remove_entry(1)

    assert str(journal_filled) == "0: I bought a cookie.\n1: I pet a dog."
    assert journal_filled.count == 2

    try:
        journal_filled.remove_entry(2)
    except ValueError as e:
        assert str(e) == "Invalid position."


def test_open_closed_principle():
    api = CoinGeckoFreeApi()

    tokens = [token for token in Token]
    currencies = [currency for currency in Currency]

    prices = []

    try:
        prices = api.get_token_prices(tokens, currencies)
    except Exception as e:
        print(e)

    if prices:
        for token in prices:
            for currency in prices[token]:
                print(f"{token} price in {currency}: {prices[token][currency]}")
                assert prices[token][currency] > 0

    token_filter = Filter()

    btc_spec = TokenSpecification(Token.BTC)
    for token in token_filter.filter(tokens, btc_spec):
        assert token == Token.BTC

    eth_spec = TokenSpecification(Token.ETH) & TokenSpecification(Token.PEPE)
    for token in token_filter.filter(tokens, eth_spec):
        assert token in [Token.ETH, Token.PEPE]

    usd_token_spec = TokenSpecification(Token.USDC) & TokenSpecification(Token.USDT)
    for token in token_filter.filter(tokens, usd_token_spec):
        assert token in [Token.USDC, Token.USDT]

    stablecoin_spec = TokenTypeSpecification(TokenType.STABLECOIN)
    for token in token_filter.filter(tokens, stablecoin_spec):
        assert token in [Token.USDC, Token.USDT]

    crypto_spec = TokenTypeSpecification(TokenType.CRYPTO)
    for token in token_filter.filter(tokens, crypto_spec):
        assert token in [Token.BTC, Token.ETH]

    meme_spec = TokenTypeSpecification(TokenType.MEME)
    for token in token_filter.filter(tokens, meme_spec):
        assert token in [Token.PEPE, Token.WIF]
