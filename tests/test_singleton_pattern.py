from software_design_patterns.creational.singleton_pattern import *

GENESIS_BLOCK_HASH = "ec596eea922c4f9b003eb27d2ea8744d2d43e09401cb17f597906abea72a89ca"


def test_singleton_blockchain():
    blockchain = Blockchain()

    assert len(blockchain.chain) == 1
    assert blockchain.get_latest_block().hash == GENESIS_BLOCK_HASH

    transaction1 = Transaction("Alice", "Bob", 10)
    block1 = Block(1, [transaction1], GENESIS_BLOCK_HASH)
    blockchain.add_block(block1)

    assert len(blockchain.chain) == 2
    assert blockchain.get_latest_block().hash != GENESIS_BLOCK_HASH
    assert blockchain.get_latest_block().previous_hash == GENESIS_BLOCK_HASH
    assert blockchain.get_latest_block().transactions == [transaction1]
    assert blockchain.get_latest_block().nonce == 1

    blockchain_2 = Blockchain()

    assert blockchain is blockchain_2 is Blockchain()
    assert (
        len(blockchain.chain) == len(blockchain_2.chain) == len(Blockchain().chain) == 2
    )
