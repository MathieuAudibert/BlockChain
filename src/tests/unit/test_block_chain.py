import pytest
import datetime
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestBlockChain:
    """Test cases for the BlockChain class."""
    
    def test_blockchain_creation(self):
        """Test creating a blockchain with valid parameters."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        assert len(blockchain.blocks) == 1
        assert blockchain.genesis == genesis_block
        assert blockchain.blocks[0] == genesis_block
    
    def test_blockchain_creation_with_empty_blocks(self):
        """Test creating a blockchain with empty blocks list."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([], genesis_block)
        
        assert len(blockchain.blocks) == 0
        assert blockchain.genesis == genesis_block
    
    def test_blockchain_get_last_with_single_block(self):
        """Test getting the last block when there's only the genesis block."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        last_block = blockchain.get_last()
        assert last_block == genesis_block
    
    def test_blockchain_get_last_with_multiple_blocks(self):
        """Test getting the last block when there are multiple blocks."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        block1 = Block(1, "2025-07-15T12:01:00", [], "Genesis", "")
        block2 = Block(2, "2025-07-15T12:02:00", [], block1.hash, "")
        
        blockchain = BlockChain([genesis_block, block1, block2], genesis_block)
        
        last_block = blockchain.get_last()
        assert last_block == block2
    
    def test_blockchain_get_last_empty(self):
        """Test getting the last block when blockchain is empty."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([], genesis_block)
        
        with pytest.raises(ValueError, match="Blockchain is empty"):
            blockchain.get_last()
    
    def test_blockchain_blocks_setter_wrong_type(self):
        """Test setting blocks with wrong type."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        with pytest.raises(TypeError, match="Blocks must be a list"):
            blockchain.blocks = "not a list"
    
    def test_blockchain_blocks_setter_wrong_element_type(self):
        """Test setting blocks with wrong element type."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        with pytest.raises(TypeError, match="All items in blocks must be Block instances"):
            blockchain.blocks = [genesis_block, "not a block"]
    
    def test_blockchain_genesis_setter_wrong_type(self):
        """Test setting genesis with wrong type."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        with pytest.raises(TypeError, match="Genesis must be a Block instance"):
            blockchain.genesis = "not a block"
    
    def test_blockchain_string_representation(self):
        """Test the string representation of a blockchain."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        # The string representation should contain the class name
        assert "BlockChain" in str(blockchain)
    
    def test_blockchain_with_multiple_blocks(self):
        """Test blockchain with multiple blocks."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        block1 = Block(1, "2025-07-15T12:01:00", [], "Genesis", "")
        block2 = Block(2, "2025-07-15T12:02:00", [], block1.hash, "")
        
        blockchain = BlockChain([genesis_block, block1, block2], genesis_block)
        
        assert len(blockchain.blocks) == 3
        assert blockchain.blocks[0] == genesis_block
        assert blockchain.blocks[1] == block1
        assert blockchain.blocks[2] == block2
    
    def test_blockchain_add_block_wrong_type(self):
        """Test adding a non-Block object to the blockchain."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        with pytest.raises(TypeError, match="Block must be an instance of Block class"):
            blockchain.add_block("not a block")
    
    def test_blockchain_add_block_wrong_previous_hash(self):
        """Test adding a block with wrong previous hash."""
        genesis_block = Block(0, "2025-07-15T12:00:00", [], "0", "Genesis")
        blockchain = BlockChain([genesis_block], genesis_block)
        
        # Block with wrong previous hash
        new_block = Block(1, "2025-07-15T12:01:00", [], "WrongHash", "")
        
        with pytest.raises(ValueError, match="Block's previous hash does not match the last block's hash"):
            blockchain.add_block(new_block) 