import pytest
import datetime
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestTransaction:
    """Test cases for the Transaction class."""
    
    def test_transaction_creation(self):
        """Test creating a transaction with valid parameters."""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        assert transaction.sender == "Alice"
        assert transaction.receiver == "Bob"
        assert transaction.token == token
        assert transaction.amount == 10.0
        assert transaction.timestamp == timestamp
    
    def test_transaction_creation_with_different_amount_types(self):
        """Test creating transactions with different amount types."""
        token = Token("Ethereum", "ETH", 2.0)
        timestamp = "2025-07-15T12:00:00"
        
        # Integer amount
        transaction1 = Transaction("Alice", "Bob", token, 10, timestamp)
        assert transaction1.amount == 10
        
        # Float amount
        transaction2 = Transaction("Bob", "Charlie", token, 5.5, timestamp)
        assert transaction2.amount == 5.5
    
    def test_transaction_string_representation(self):
        """Test the string representation of a transaction."""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        transaction = Transaction("Alice", "Bob", token, 10.0, timestamp)
        
        # The string representation should contain the class name and field names
        assert "Transaction" in str(transaction)
        assert "_sender" in str(transaction) or "sender" in str(transaction)
        assert "_receiver" in str(transaction) or "receiver" in str(transaction)
        assert "_token" in str(transaction) or "token" in str(transaction)
        assert "_amount" in str(transaction) or "amount" in str(transaction)
        assert "_timestamp" in str(transaction) or "timestamp" in str(transaction)
    
    def test_transaction_equality(self):
        """Test transaction equality."""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Ethereum", "ETH", 2.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction1 = Transaction("Alice", "Bob", token1, 10.0, timestamp)
        transaction2 = Transaction("Alice", "Bob", token1, 10.0, timestamp)
        transaction3 = Transaction("Bob", "Charlie", token2, 5.0, timestamp)
        
        assert transaction1 == transaction2
        assert transaction1 != transaction3
    
    def test_transaction_type_validation(self):
        """Test that transaction validates input types."""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        # Test sender validation
        with pytest.raises(TypeError, match="Sender must be a string"):
            Transaction(123, "Bob", token, 10.0, timestamp)
        
        # Test receiver validation
        with pytest.raises(TypeError, match="Receiver must be a string"):
            Transaction("Alice", 123, token, 10.0, timestamp)
        
        # Test token validation
        with pytest.raises(TypeError, match="Token must be an instance of Token class"):
            Transaction("Alice", "Bob", "not a token", 10.0, timestamp)
        
        # Test amount validation
        with pytest.raises(TypeError, match="Amount must be a number"):
            Transaction("Alice", "Bob", token, "not a number", timestamp)
        
        # Test timestamp validation
        with pytest.raises(TypeError, match="Timestamp must be a string"):
            Transaction("Alice", "Bob", token, 10.0, 123)
    
    def test_transaction_with_zero_amount(self):
        """Test creating a transaction with zero amount."""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        transaction = Transaction("Alice", "Bob", token, 0.0, timestamp)
        assert transaction.amount == 0.0
    
    def test_transaction_with_negative_amount(self):
        """Test creating a transaction with negative amount."""
        token = Token("Bitcoin", "BTC", 1.0)
        timestamp = "2025-07-15T12:00:00"
        
        # Should not raise an exception for negative amounts
        transaction = Transaction("Alice", "Bob", token, -5.0, timestamp)
        assert transaction.amount == -5.0 