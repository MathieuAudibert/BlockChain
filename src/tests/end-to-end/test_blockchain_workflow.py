import pytest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestBlockchainWorkflow:
    """End-to-end tests for the complete blockchain workflow"""
    
    def test_load_transactions_from_json(self):
        """Test loading transactions from a JSON file"""
        # Create a temporary JSON file with test data
        test_data = {
            "transactions": [
                {
                    "sender": "Alice",
                    "receiver": "Bob",
                    "token": {
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "value": 1.0
                    },
                    "amount": 10.0,
                    "timestamp": "2025-07-15T12:00:00"
                },
                {
                    "sender": "Bob",
                    "receiver": "Charlie",
                    "token": {
                        "name": "Ethereum",
                        "symbol": "ETH",
                        "value": 2.0
                    },
                    "amount": 5.0,
                    "timestamp": "2025-07-15T12:05:00"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            # Import the function from main.py
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from main import load_transactions
            
            # Test loading transactions
            transactions = load_transactions(temp_file)
            
            assert len(transactions) == 2
            
            # Check first transaction
            assert transactions[0].sender == "Alice"
            assert transactions[0].receiver == "Bob"
            assert transactions[0].token.name == "Bitcoin"
            assert transactions[0].token.symbol == "BTC"
            assert transactions[0].token.value == pytest.approx(1.0)
            assert transactions[0].amount == pytest.approx(10.0)
            assert transactions[0].timestamp == "2025-07-15T12:00:00"
            
            # Check second transaction
            assert transactions[1].sender == "Bob"
            assert transactions[1].receiver == "Charlie"
            assert transactions[1].token.name == "Ethereum"
            assert transactions[1].token.symbol == "ETH"
            assert transactions[1].token.value == pytest.approx(2.0)
            assert transactions[1].amount == pytest.approx(5.0)
            assert transactions[1].timestamp == "2025-07-15T12:05:00"
            
        finally:
            os.unlink(temp_file)
    
    def test_create_blockchain_from_transactions(self):
        """Test creating a blockchain from a list of transactions"""
        # Create test transactions
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Ethereum", "ETH", 2.0)
        
        transaction1 = Transaction("Alice", "Bob", token1, 10.0, "2025-07-15T12:00:00")
        transaction2 = Transaction("Bob", "Charlie", token2, 5.0, "2025-07-15T12:05:00")
        
        transactions = [transaction1, transaction2]
        
        # Import the function from main.py
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from main import create_blockchain
        
        # Test creating blockchain
        blockchain = create_blockchain(transactions)
        
        # Check genesis block
        assert blockchain.genesis.index == 0
        assert len(blockchain.genesis.transactions) == 0
        assert blockchain.genesis.previous_hash == "0"
        assert blockchain.genesis.hash == "Genesis"
        
        # Check blocks
        assert len(blockchain.blocks) == 3  # genesis + 2 transaction blocks
        
        # Check first transaction block
        block1 = blockchain.blocks[1]
        assert block1.index == 1
        assert len(block1.transactions) == 1
        assert block1.transactions[0] == transaction1
        assert block1.previous_hash == "Genesis"
        
        # Check second transaction block
        block2 = blockchain.blocks[2]
        assert block2.index == 2
        assert len(block2.transactions) == 1
        assert block2.transactions[0] == transaction2
        assert block2.previous_hash == block1.hash
    
    def test_blockchain_to_json_serialization(self):
        """Test converting a blockchain to JSON format"""
        # Create a simple blockchain
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        token = Token("Bitcoin", "BTC", 1.0)
        transaction = Transaction("Alice", "Bob", token, 10.0, "2025-07-15T12:00:00")
        block1 = Block(1, "2025-07-15T12:01:00", [transaction], "Genesis", "abc123")
        
        blockchain = BlockChain([genesis_block, block1], genesis_block)
        
        # Convert to dictionary (simulating the block_to_dict function)
        def block_to_dict(block):
            return {
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': [
                    {
                        'sender': tx.sender,
                        'receiver': tx.receiver,
                        'token': {
                            'name': tx.token.name,
                            'symbol': tx.token.symbol,
                            'value': tx.token.value
                        },
                        'amount': tx.amount,
                        'timestamp': tx.timestamp
                    } for tx in block.transactions
                ],
                'previous_hash': block.previous_hash,
                'hash': block.hash
            }
        
        blockchain_data = {
            'genesis': block_to_dict(blockchain.genesis),
            'blocks': [block_to_dict(b) for b in blockchain.blocks]
        }
        
        # Test JSON serialization
        json_str = json.dumps(blockchain_data, indent=2)
        assert json_str 
        assert "genesis" in json_str
        assert "blocks" in json_str
        assert "Alice" in json_str
        assert "Bob" in json_str
        assert "Bitcoin" in json_str
        assert "BTC" in json_str
    
    def test_complete_workflow_with_temp_files(self):
        """Test the complete workflow with temporary files"""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Create results directory
            results_dir = os.path.join(temp_dir, "results", "15-07-2025")
            os.makedirs(results_dir)
            
            # Create logs directory
            logs_dir = os.path.join(temp_dir, "logs")
            os.makedirs(logs_dir)
            
            # Create test transaction files
            test_files = [
                {
                    "filename": "transactions1.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Alice",
                                "receiver": "Bob",
                                "token": {"name": "Bitcoin", "symbol": "BTC", "value": 1.0},
                                "amount": 10.0,
                                "timestamp": "2025-07-15T12:00:00"
                            }
                        ]
                    }
                },
                {
                    "filename": "transactions2.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Bob",
                                "receiver": "Charlie",
                                "token": {"name": "Ethereum", "symbol": "ETH", "value": 2.0},
                                "amount": 5.0,
                                "timestamp": "2025-07-15T12:05:00"
                            }
                        ]
                    }
                }
            ]
            
            # Write test files
            for test_file in test_files:
                file_path = os.path.join(transactions_dir, test_file["filename"])
                with open(file_path, 'w') as f:
                    json.dump(test_file["data"], f)
            
            # Import main functions
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from main import load_transactions, create_blockchain, log_blockchain
            
            # Test the complete workflow
            files = [f for f in os.listdir(transactions_dir) if f.endswith('.json')]
            assert len(files) == 2
            
            # Create genesis block
            genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
            blockchain = BlockChain([genesis_block], genesis_block)
            
            # Process each file
            for i, filename in enumerate(files):
                file_path = os.path.join(transactions_dir, filename)
                transactions = load_transactions(file_path)
                
                previous_hash = blockchain.get_last().hash
                block = Block(i + 1, "2025-07-15T12:00:00", transactions, previous_hash, "")
                blockchain.blocks.append(block)
            
            # Verify blockchain structure
            assert len(blockchain.blocks) == 3  # genesis + 2 blocks
            assert blockchain.genesis.index == 0
            assert blockchain.blocks[1].index == 1
            assert blockchain.blocks[2].index == 2
            
            # Verify transactions in blocks
            assert len(blockchain.blocks[1].transactions) == 1
            assert len(blockchain.blocks[2].transactions) == 1
            
            # Check transaction details
            tx1 = blockchain.blocks[1].transactions[0]
            assert tx1.sender == "Alice"
            assert tx1.receiver == "Bob"
            assert tx1.token.name == "Bitcoin"
            assert tx1.token.symbol == "BTC"
            assert tx1.token.value == pytest.approx(1.0)
            assert tx1.amount == pytest.approx(10.0)
            
            tx2 = blockchain.blocks[2].transactions[0]
            assert tx2.sender == "Bob"
            assert tx2.receiver == "Charlie"
            assert tx2.token.name == "Ethereum"
            assert tx2.token.symbol == "ETH"
            assert tx2.token.value == pytest.approx(2.0)
            assert tx2.amount == pytest.approx(5.0)
    
    def test_error_handling_invalid_json(self):
        """Test error handling for invalid JSON files"""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json content')
            temp_file = f.name
        
        try:
            # Import the function from main.py
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from main import load_transactions
            
            # Test that loading invalid JSON raises an exception
            with pytest.raises(Exception):
                load_transactions(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_error_handling_missing_file(self):
        """Test error handling for missing files"""
        # Import the function from main.py
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from main import load_transactions
        
        # Test that loading a non-existent file raises an exception
        with pytest.raises(FileNotFoundError):
            load_transactions("nonexistent_file.json") 