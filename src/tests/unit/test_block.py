import pytest
import datetime
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestBlock:
    """Test cases for the Block """
    
    def test_block_creation(self):
        """Test creating a block with valid parameters"""
        timestamp = "2025-07-15T12:00:00"
        transactions = []
        previous_hash = "0"
        hash_value = "abc123"
        
        block = Block(1, timestamp, transactions, previous_hash, hash_value)
        
        assert block.index == 1
        assert block.timestamp == timestamp
        assert block.transactions == transactions
        assert block.previous_hash == previous_hash
        assert block.hash == hash_value
    
    def test_block_creation_with_transactions(self):
        """Test creating a block with transactions"""
        token = Token("Bitcoin", "BTC", 1.0)
        transaction = Transaction("Alice", "Bob", token, 10.0, "2025-07-15T12:00:00")
        transactions = [transaction]
        
        block = Block(1, "2025-07-15T12:00:00", transactions, "0", "abc123")
        
        assert len(block.transactions) == 1
        assert block.transactions[0] == transaction
    
    def test_block_string_representation(self):
        """Test the string representation of a block"""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        
        expected = "Block(index=1, timestamp=2025-07-15T12:00:00, transactions=[], previous_hash=0, hash=abc123)"
        assert str(block) == expected
    
    def test_block_equality(self):
        """Test block equality."""
        block1 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        block2 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        block3 = Block(2, "2025-07-15T12:00:00", [], "0", "abc123")
        
        assert block1 == block2
        assert block1 != block3
    
    def test_block_hash(self):
        """Test that blocks can be used as dictionary keys"""
        block1 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        block2 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        
        block_dict = {block1: "value1"}
        assert block_dict[block2] == "value1"
    
    def test_block_immutability(self):
        """Test that block attributes cannot be modified after creation"""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        
        with pytest.raises(AttributeError):
            block.index = 2
        
        with pytest.raises(AttributeError):
            block.timestamp = "2025-07-15T13:00:00"
        
        with pytest.raises(AttributeError):
            block.previous_hash = "def456"
        
        with pytest.raises(AttributeError):
            block.hash = "ghi789"
    
    def test_block_with_empty_transactions(self):
        """Test creating a block with empty transactions list"""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        assert len(block.transactions) == 0
    
    def test_block_with_multiple_transactions(self):
        """Test creating a block with multiple transactions"""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Ethereum", "ETH", 2.0)
        
        transaction1 = Transaction("Alice", "Bob", token1, 10.0, "2025-07-15T12:00:00")
        transaction2 = Transaction("Bob", "Charlie", token2, 5.0, "2025-07-15T12:05:00")
        
        transactions = [transaction1, transaction2]
        block = Block(1, "2025-07-15T12:00:00", transactions, "0", "abc123")
        
        assert len(block.transactions) == 2
        assert block.transactions[0] == transaction1
        assert block.transactions[1] == transaction2
    
    def test_block_with_zero_index(self):
        """Test creating a block with zero index (genesis block)"""
        block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        assert block.index == 0
    
    def test_block_with_negative_index(self):
        """Test creating a block with negative index"""
        # Should not raise an exception for negative index
        block = Block(-1, "2025-07-15T12:00:00", [], "0", "abc123")
        assert block.index == -1
    
    def test_block_with_empty_hash(self):
        """Test creating a block with empty hash"""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "")
        assert block.hash == ""
    
    def test_block_with_long_hash(self):
        """Test creating a block with a long hash value"""
        long_hash = "a" * 64  # 64 character hash
        block = Block(1, "2025-07-15T12:00:00", [], "0", long_hash)
        assert block.hash == long_hash 