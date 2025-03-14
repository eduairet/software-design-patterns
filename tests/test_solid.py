import os
from shared.constants.paths import TESTS_FILES_DIR
from software_design_patterns.solid.single_responsibility_principle import *
from software_design_patterns.solid.open_closed_principle import *
from software_design_patterns.solid.liskov_substitution_principle import *
from software_design_patterns.solid.interface_segregation_principle import *
from software_design_patterns.solid.dependency_inversion_principle import *


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
        pass

    if prices:
        for token in prices:
            for currency in prices[token]:
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
        str(spider)
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
    assert str(swimming) == SWIMMING_EXPECTED

    running = Running(Location.OUTDOOR, RUNNING_DISTANCE)
    assert str(running) == RUNNING_EXPECTED

    cycling = Cycling(Location.OUTDOOR, CYCLING_DISTANCE, BicycleType.ROAD)
    assert str(cycling) == CYCLING_EXPECTED

    iron_man = Triathlon(
        "Iron Man",
        TriathlonDistances(SWIMMING_DISTANCE, RUNNING_DISTANCE, CYCLING_DISTANCE),
        BicycleType.ROAD,
    )
    assert str(iron_man) == IRON_EXPECTED
    assert str(iron_man.swimming) == SWIMMING_EXPECTED
    assert str(iron_man.running) == RUNNING_EXPECTED
    assert str(iron_man.cycling) == CYCLING_EXPECTED

    rugby_sevens = Rugby(RugbyType.SEVENS)
    assert str(rugby_sevens) == RUGBY_EXPECTED


def test_dependency_inversion_principle():
    customer1 = Customer("John")
    customer2 = Customer("Chris")
    customer3 = Customer("Alice")
    customer4 = Customer("Alice")

    steak1 = Steak("Ribeye")
    steak2 = Steak("T-bone")
    steak3 = Steak("Sirloin")

    order_book = OrderBook()
    order_book.add_order(customer1, steak1, SteakDoneness.RARE)
    order_book.add_order(customer2, steak2, SteakDoneness.MEDIUM)
    order_book.add_order(customer3, steak3, SteakDoneness.WELL_DONE)
    order_book.add_order(customer4, steak1, SteakDoneness.RARE)
    assert len(order_book.orders) == 4

    order_search = OrderSearch("Alice", order_book)
    orders = order_search.order_book
    assert len(orders) == 2
    assert orders[0][0].name == "Alice"
    assert orders[1][0].name == "Alice"
    assert orders[0][1].name == "Sirloin"
    assert orders[1][1].name == "Ribeye"
    assert orders[0][2] == SteakDoneness.WELL_DONE
    assert orders[1][2] == SteakDoneness.RARE
