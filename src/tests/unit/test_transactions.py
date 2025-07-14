import pytest
import datetime
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestTransaction:
    """Test cases for the Transaction """
    
    def test_transaction_creation(self):
        """Test creating a transaction with valid parameters"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        assert transaction.sender == "Alice"
        assert transaction.receiver == "Bob"
        assert transaction.token == token
        assert transaction.amount == 10.0
        assert transaction.timestamp == timestamp
    
    def test_transaction_creation_with_different_amount_types(self):
        """Test creating transactions with different amount types"""
        token = Token("Ethereum", "ETH", 2.0)
        timestamp = "2025-07-15T12:00:00"
        
        # Integer amount
        transaction1 = Transaction("Alice", "Bob", token, 10, timestamp)
        assert transaction1.amount == 10
        
        # Float amount
        transaction2 = Transaction("Bob", "Charlie", token, 5.5, timestamp)
        assert transaction2.amount == 5.5
    
    def test_transaction_string_representation(self):
        """Test the string representation of a transaction"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        transaction = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        expected = f"Transaction(sender=Alice, receiver=Bob, token={token}, amount=10.0, timestamp={timestamp})"
        assert str(transaction) == expected
    
    def test_transaction_equality(self):
        """Test transaction equality"""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Ethereum", "ETH", 2.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction1 = Transaction("Alice", "Bob", token1, 10.0, timestamp)
        transaction2 = Transaction("Alice", "Bob", token1, 10.0, timestamp)
        transaction3 = Transaction("Bob", "Charlie", token2, 5.0, timestamp)
        
        assert transaction1 == transaction2
        assert transaction1 != transaction3
    
    def test_transaction_hash(self):
        """Test that transactions can be used as dictionary keys"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction1 = Transaction("Alice", "Bob", token, 10.0, timestamp)
        transaction2 = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        transaction_dict = {transaction1: "value1"}
        assert transaction_dict[transaction2] == "value1"
    
    def test_transaction_immutability(self):
        """Test that transaction attributes cannot be modified after creation"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        transaction = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        with pytest.raises(AttributeError):
            transaction.sender = "Charlie"
        
        with pytest.raises(AttributeError):
            transaction.receiver = "David"
        
        with pytest.raises(AttributeError):
            transaction.amount = 20.0
        
        with pytest.raises(AttributeError):
            transaction.timestamp = "2025-07-15T13:00:00"
    
    def test_transaction_with_zero_amount(self):
        """Test creating a transaction with zero amount"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction = Transaction("Alice", "Bob", token, 0.0, timestamp)
        assert transaction.amount == 0.0
    
    def test_transaction_with_negative_amount(self):
        """Test creating a transaction with negative amount"""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        # Should not raise an exception for negative amounts
        transaction = Transaction("Alice", "Bob", token, -5.0, timestamp)
        assert transaction.amount == -5.0 