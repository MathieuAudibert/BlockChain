import pytest
from crypto.tokens import Token


class TestToken:
    """Test cases for the Token class."""
    
    def test_token_creation(self):
        """Test creating a token with valid parameters."""
        token = Token("Bitcoin", "BTC", 1.0)
        assert token.name == "Bitcoin"
        assert token.symbol == "BTC"
        assert token.value == 1.0
    
    def test_token_creation_with_different_types(self):
        """Test creating tokens with different value types."""
        # Integer value
        token1 = Token("Ethereum", "ETH", 2)
        assert token1.value == 2
        
        # Float value
        token2 = Token("Litecoin", "LTC", 3.5)
        assert token2.value == 3.5
    
    def test_token_string_representation(self):
        """Test the string representation of a token."""
        token = Token("Bitcoin", "BTC", 1.0)
        
        # The string representation should contain the class name and field names
        assert "Token" in str(token)
        assert "_name" in str(token) or "name" in str(token)
        assert "_symbol" in str(token) or "symbol" in str(token)
        assert "_value" in str(token) or "value" in str(token)
    
    def test_token_equality(self):
        """Test token equality."""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Bitcoin", "BTC", 1.0)
        token3 = Token("Ethereum", "ETH", 1.0)
        
        assert token1 == token2
        assert token1 != token3
    
    def test_token_type_validation(self):
        """Test that token validates input types."""
        # Test name validation
        with pytest.raises(TypeError, match="Token name must be a string"):
            Token(123, "BTC", 1.0)
        
        # Test symbol validation
        with pytest.raises(TypeError, match="Token symbol must be a string"):
            Token("Bitcoin", 123, 1.0)
        
        # Test value validation
        with pytest.raises(TypeError, match="Token value must be a number"):
            Token("Bitcoin", "BTC", "not a number")
    
    def test_token_with_zero_value(self):
        """Test creating a token with zero value."""
        token = Token("Test", "TST", 0.0)
        assert token.value == 0.0
    
    def test_token_with_negative_value(self):
        """Test creating a token with negative value."""
        token = Token("Test", "TST", -5.0)
        assert token.value == -5.0 