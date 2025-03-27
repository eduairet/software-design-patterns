from hashlib import sha256


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class Block:
    def __init__(
        self,
        timestamp: int,
        transactions: list[Transaction],
        previous_hash: str,
        nonce: int = 0,
    ):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        return sha256(
            str(self.timestamp).encode()
            + str(self.transactions).encode()
            + str(self.previous_hash).encode()
            + str(self.nonce).encode()
        ).hexdigest()


@singleton
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nonce = 1

    def create_genesis_block(self) -> Block:
        return Block(0, [], "0", 0)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        new_block.nonce = self.nonce
        self.chain.append(new_block)
        self.nonce += 1
