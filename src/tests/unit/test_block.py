import pytest
import datetime
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestBlock:
    """Test cases for the Block class."""
    
    def test_block_creation(self):
        """Test creating a block with valid parameters."""
        timestamp = "2025-07-15T12:00:00"
        transactions = []
        previous_hash = "0"
        hash_value = "abc123"
        
        block = Block(1, timestamp, transactions, previous_hash, hash_value)
        
        assert block.index == 1
        assert block.timestamp == timestamp
        assert block.transactions == transactions
        assert block.previous_hash == previous_hash
        # Hash is auto-computed for non-genesis blocks
        assert block.hash != hash_value  # Should be computed hash
        assert len(block.hash) == 64  # SHA-256 hash length
    
    def test_genesis_block_creation(self):
        """Test creating a genesis block (index 0)."""
        timestamp = "2025-07-15T12:00:00"
        transactions = []
        previous_hash = "0"
        hash_value = "Genesis"
        
        block = Block(0, timestamp, transactions, previous_hash, hash_value)
        
        assert block.index == 0
        assert block.timestamp == timestamp
        assert block.transactions == transactions
        assert block.previous_hash == previous_hash
        assert block.hash == "Genesis"  # Genesis hash should be preserved
    
    def test_block_creation_with_transactions(self):
        """Test creating a block with transactions."""
        token = Token("Bitcoin", "BTC", 1.0)
        transaction = Transaction("Alice", "Bob", token, 10.0, "2025-07-15T12:00:00")
        transactions = [transaction]
        
        block = Block(1, "2025-07-15T12:00:00", transactions, "0", "")
        
        assert len(block.transactions) == 1
        assert block.transactions[0] == transaction
        assert len(block.hash) == 64  # Should have computed hash
    
    def test_block_string_representation(self):
        """Test the string representation of a block."""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        
        # The string representation should contain the class name and field names
        assert "Block" in str(block)
        assert "_index" in str(block) or "index" in str(block)
        assert "_timestamp" in str(block) or "timestamp" in str(block)
    
    def test_block_equality(self):
        """Test block equality."""
        block1 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        block2 = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        block3 = Block(2, "2025-07-15T12:00:00", [], "0", "abc123")
        
        assert block1 == block2
        assert block1 != block3
    
    def test_block_with_empty_transactions(self):
        """Test creating a block with empty transactions list."""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "abc123")
        assert len(block.transactions) == 0
    
    def test_block_with_multiple_transactions(self):
        """Test creating a block with multiple transactions."""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Ethereum", "ETH", 2.0)
        
        transaction1 = Transaction("Alice", "Bob", token1, 10.0, "2025-07-15T12:00:00")
        transaction2 = Transaction("Bob", "Charlie", token2, 5.0, "2025-07-15T12:05:00")
        
        transactions = [transaction1, transaction2]
        block = Block(1, "2025-07-15T12:00:00", transactions, "0", "")
        
        assert len(block.transactions) == 2
        assert block.transactions[0] == transaction1
        assert block.transactions[1] == transaction2
    
    def test_block_with_zero_index(self):
        """Test creating a block with zero index (genesis block)."""
        block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        assert block.index == 0
    
    def test_block_with_negative_index(self):
        """Test creating a block with negative index."""
        # Should not raise an exception for negative index
        block = Block(-1, "2025-07-15T12:00:00", [], "0", "abc123")
        assert block.index == -1
    
    def test_block_compute_hash(self):
        """Test that block hash is computed correctly."""
        block = Block(1, "2025-07-15T12:00:00", [], "0", "")
        
        # Hash should be computed automatically
        assert len(block.hash) == 64  # SHA-256 hash length
        assert block.hash != ""  # Should not be empty
    
    def test_block_hash_consistency(self):
        """Test that same block data produces same hash."""
        block1 = Block(1, "2025-07-15T12:00:00", [], "0", "")
        block2 = Block(1, "2025-07-15T12:00:00", [], "0", "")
        
        # Same data should produce same hash
        assert block1.hash == block2.hash
    
    def test_block_hash_uniqueness(self):
        """Test that different block data produces different hashes."""
        block1 = Block(1, "2025-07-15T12:00:00", [], "0", "")
        block2 = Block(2, "2025-07-15T12:00:00", [], "0", "")
        
        # Different data should produce different hashes
        assert block1.hash != block2.hash
    
    def test_block_type_validation(self):
        """Test that block validates input types."""
        # Test index validation
        with pytest.raises(TypeError, match="Block index must be an integer"):
            Block("not an int", "2025-07-15T12:00:00", [], "0", "abc123")
        
        # Test timestamp validation
        with pytest.raises(TypeError, match="Block timestamp must be a string"):
            Block(1, 123, [], "0", "abc123")
        
        # Test transactions validation
        with pytest.raises(TypeError, match="Block transactions must be a list"):
            Block(1, "2025-07-15T12:00:00", "not a list", "0", "abc123")
        
        # Test previous_hash validation
        with pytest.raises(TypeError, match="Block previous hash must be a string"):
            Block(1, "2025-07-15T12:00:00", [], 123, "abc123")
        
        # Test hash validation
        with pytest.raises(TypeError, match="Block hash must be a string"):
            Block(1, "2025-07-15T12:00:00", [], "0", 123) 