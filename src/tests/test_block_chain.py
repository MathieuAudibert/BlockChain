import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blockchain.block_chain import BlockChain
from main import creer_block_chain


class TestBlockChainCreation(unittest.TestCase):
    def test_blockchain_creation(self):
        transactions = [
            "Alice envoie 50 EUR à Bob",
            "Bob envoie 25 EUR à Charlie",
            "Charlie envoie 10 EUR à Alice",
            "Alice envoie 5 EUR à Bob",
        ]
        blockchain = creer_block_chain(transactions, transa_par_block=2)
        self.assertEqual(len(blockchain), 2)

        for i in range(1, len(blockchain)):
            current_block = blockchain[i]
            previous_block = blockchain[i - 1]
            self.assertEqual(current_block.get_block_precedant(), previous_block.get_hash())

    def test_hash_modification(self):
        transactions = [
            "Alice envoie 50 EUR à Bob",
            "Bob envoie 25 EUR à Charlie",
            "Charlie envoie 10 EUR à Alice",
            "Alice envoie 5 EUR à Bob",
        ]

        blockchain = creer_block_chain(transactions)
        original_hash = blockchain[0].get_hash()

        transactions[0] = "Alice envoie 100 EUR à Bob"
        modified_blockchain = creer_block_chain(transactions)
        modified_hash = modified_blockchain[0].get_hash()

        self.assertNotEqual(original_hash, modified_hash)

if __name__ == "__main__":
    unittest.main()