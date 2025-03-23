import unittest
import os
import json
import tempfile
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blockchain.block_chain import BlockChain
from main import recup_transactions, creer_block_chain, blockchaine_dict, sauvegarder_en_json

# Test de toutes les fonctions du module main.py... tests sur le format du json etc... 

class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.transactions_dir = os.path.join(self.temp_dir, "transactions")
        self.results_dir = os.path.join(self.temp_dir, "results")
        os.makedirs(self.transactions_dir, exist_ok=True)
        
        self.test_transactions = [
            "Alice envoie 50 EUR à Bob",
            "Bob envoie 25 EUR à Charlie",
            "Charlie envoie 10 EUR à Alice",
            "Alice envoie 5 EUR à Bob",
        ]
        
        self.transaction_file = os.path.join(self.transactions_dir, "test_transactions.json")
        with open(self.transaction_file, 'w') as f:
            json.dump(self.test_transactions, f)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_recup_transactions_list(self):
        transactions = recup_transactions(self.transaction_file)
        self.assertEqual(len(transactions), 4)
        self.assertEqual(transactions[0], "Alice envoie 50 EUR à Bob")
    
    def test_recup_transactions_dict(self):
        dict_transaction_file = os.path.join(self.transactions_dir, "dict_transactions.json")
        with open(dict_transaction_file, 'w') as f:
            json.dump({"transactions": self.test_transactions}, f)
        
        transactions = recup_transactions(dict_transaction_file)
        self.assertEqual(len(transactions), 4)
        self.assertEqual(transactions[2], "Charlie envoie 10 EUR à Alice")
    
    def test_recup_transactions_file_not_found(self):
        transactions = recup_transactions("non_existent_file.json")
        self.assertEqual(transactions, [])
    
    def test_recup_transactions_invalid_json(self):
        invalid_file = os.path.join(self.transactions_dir, "invalid.json")
        with open(invalid_file, 'w') as f:
            f.write("This is not valid JSON")
        
        transactions = recup_transactions(invalid_file)
        self.assertEqual(transactions, [])
    
    def test_creer_block_chain(self):
        blockchain = creer_block_chain(self.test_transactions, transa_par_block=2)
        
        self.assertEqual(len(blockchain), 2)
        self.assertEqual(len(blockchain[0].get_list_transactions()), 2)
        self.assertEqual(len(blockchain[1].get_list_transactions()), 2)
        
        self.assertEqual(blockchain[0].get_block_precedant(), "Initial")
        
        self.assertEqual(blockchain[1].get_block_precedant(), blockchain[0].get_hash())
    
    def test_blockchaine_dict(self):
        blockchain = creer_block_chain(self.test_transactions, transa_par_block=2)
        blockchain_dict = blockchaine_dict(blockchain)
        
        self.assertEqual(len(blockchain_dict), 2)
        self.assertEqual(blockchain_dict[0]["index"], 0)
        self.assertEqual(blockchain_dict[1]["index"], 1)
        self.assertEqual(blockchain_dict[0]["previous_hash"], "Initial")
        self.assertEqual(blockchain_dict[1]["previous_hash"], blockchain_dict[0]["hash"])
        self.assertEqual(len(blockchain_dict[0]["transactions"]), 2)
    
    def test_sauvegarder_en_json(self):
        blockchain = creer_block_chain(self.test_transactions)
        file_path = sauvegarder_en_json(blockchain, "test_transactions", path=self.results_dir)
        
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(len(saved_data), 1)  
        self.assertEqual(saved_data[0]["index"], 0)
        self.assertEqual(len(saved_data[0]["transactions"]), 4)

if __name__ == "__main__":
    unittest.main()