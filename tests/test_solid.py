import os
from shared.constants.paths import TESTS_FILES_DIR
from software_design_patterns.solid.single_responsibility_principle import *
from software_design_patterns.solid.open_closed_principle import *
from software_design_patterns.solid.liskov_substitution_principle import *
from software_design_patterns.solid.interface_segregation_principle import *


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


def test_liskov_substitution_principle():
    dog = Dog("Dog")
    cat = Cat("Cat")
    spider = Spider("Spider")

    assert str(dog) == "Dog Dog says Woof"
    assert str(cat) == "Cat Cat says Meow"

    try:
        print(spider)
    except Exception as e:
        assert str(e) == "Spiders don't make sounds"


def test_interface_segregation_principle():
    SWIMMING_DISTANCE = 3800
    RUNNING_DISTANCE = 42200
    CYCLING_DISTANCE = 180000

    SWIMMING_EXPECTED = f"Swimming Freestyle {SWIMMING_DISTANCE} meters"
    RUNNING_EXPECTED = f"Running {RUNNING_DISTANCE} meters"
    CYCLING_EXPECTED = f"Cycling Road {CYCLING_DISTANCE} meters"
    IRON_EXPECTED = f"Iron Man with swimming {SWIMMING_DISTANCE} meters, running {RUNNING_DISTANCE} meters, and cycling {CYCLING_DISTANCE} meters"
    RUGBY_EXPECTED = "Rugby with 7 players"

    swimming = Swimming(Location.OUTDOOR, SWIMMING_DISTANCE, SwimmingStyle.FREESTYLE)
    print(swimming)
    assert str(swimming) == SWIMMING_EXPECTED

    running = Running(Location.OUTDOOR, RUNNING_DISTANCE)
    print(running)
    assert str(running) == RUNNING_EXPECTED

    cycling = Cycling(Location.OUTDOOR, CYCLING_DISTANCE, BicycleType.ROAD)
    print(cycling)
    assert str(cycling) == CYCLING_EXPECTED

    iron_man = Triathlon(
        "Iron Man",
        TriathlonDistances(SWIMMING_DISTANCE, RUNNING_DISTANCE, CYCLING_DISTANCE),
        BicycleType.ROAD,
    )
    print(iron_man)
    assert str(iron_man) == IRON_EXPECTED
    assert str(iron_man.swimming) == SWIMMING_EXPECTED
    assert str(iron_man.running) == RUNNING_EXPECTED
    assert str(iron_man.cycling) == CYCLING_EXPECTED

    rugby_sevens = Rugby(RugbyType.SEVENS)
    print(rugby_sevens)
    assert str(rugby_sevens) == RUGBY_EXPECTED
