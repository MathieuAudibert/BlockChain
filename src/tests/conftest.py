"""
Pytest configuration and common fixtures for BlockChain-1 tests.
"""

import pytest
import tempfile
import os
import json
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


@pytest.fixture
def sample_token():
    """Create a sample token for testing"""
    return Token("Bitcoin", "BTC", 1.0)


@pytest.fixture
def sample_transaction(sample_token):
    """Create a sample transaction for testing"""
    return Transaction("Alice", "Bob", sample_token, 10.0, "2025-07-15T12:00:00")


@pytest.fixture
def sample_block(sample_transaction):
    """Create a sample block for testing"""
    return Block(1, "2025-07-15T12:00:00", [sample_transaction], "0", "abc123")


@pytest.fixture
def sample_blockchain(sample_block):
    """Create a sample blockchain for testing"""
    genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
    return BlockChain([genesis_block, sample_block], genesis_block)


@pytest.fixture
def temp_transactions_file():
    """Create a temporary transactions JSON file for testing"""
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
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_datetime():
    """Mock datetime to return consistent values"""
    import datetime
    from unittest.mock import patch
    
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value.strftime.return_value = "15-07-2025"
        mock_dt.now.return_value.isoformat.return_value = "2025-07-15T12:00:00"
        yield mock_dt 