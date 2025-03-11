from abc import abstractmethod
from enum import Enum


class SteakDoneness(Enum):
    BLUE = 1
    RARE = 2
    MEDIUM = 3
    WELL_DONE = 4


class Customer:
    def __init__(self, name: str):
        self.name = name


class Steak:
    def __init__(self, name: str):
        self.name = name


class CookingStrategy:
    @abstractmethod
    def cook(self, steak: Steak):
        pass


class OrderBrowser:
    @abstractmethod
    def find_all_orders_of_customer(self, customer: Customer):
        pass


class OrderBook(OrderBrowser):
    orders: list[tuple[Customer, Steak, SteakDoneness]] = []

    def add_order(self, customer: Customer, steak: Steak, doneness: SteakDoneness):
        self.orders.append((customer, steak, doneness))

    def find_all_orders_of_customer(self, customer: Customer):
        return [order for order in self.orders if order[0].name == customer.name]


class OrderSearch:
    def __init__(self, name: str, order_book: OrderBook):
        self.name = name
        self.order_book = [
            order for order in order_book.orders if order[0].name == name
        ]
