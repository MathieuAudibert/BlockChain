import pytest
from crypto.tokens import Token


class TestToken:
    """Test cases for the Token"""
    
    def test_token_creation(self):
        """Test creating a token with valid parameters"""
        token = Token("Bitcoin", "BTC", 1.0)
        assert token.name == "Bitcoin"
        assert token.symbol == "BTC"
        assert token.value == 1.0
    
    def test_token_creation_with_different_types(self):
        """Test creating tokens with different value types"""
        # Integer value
        token1 = Token("Ethereum", "ETH", 2)
        assert token1.value == 2
        
        # Float value
        token2 = Token("Litecoin", "LTC", 3.5)
        assert token2.value == 3.5
    
    def test_token_string_representation(self):
        """Test the string representation of a token"""
        token = Token("Bitcoin", "BTC", 1.0)
        expected = "Token(name=Bitcoin, symbol=BTC, value=1.0)"
        assert str(token) == expected
    
    def test_token_equality(self):
        """Test token equality."""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Bitcoin", "BTC", 1.0)
        token3 = Token("Ethereum", "ETH", 1.0)
        
        assert token1 == token2
        assert token1 != token3
    
    def test_token_hash(self):
        """Test that tokens can be used as dictionary keys"""
        token1 = Token("Bitcoin", "BTC", 1.0)
        token2 = Token("Bitcoin", "BTC", 1.0)
        
        token_dict = {token1: "value1"}
        assert token_dict[token2] == "value1"
    
    def test_token_immutability(self):
        """Test that token attributes cannot be modified after creation"""
        token = Token("Bitcoin", "BTC", 1.0)
        
        with pytest.raises(AttributeError):
            token.name = "Ethereum"
        
        with pytest.raises(AttributeError):
            token.symbol = "ETH"
        
        with pytest.raises(AttributeError):
            token.value = 2.0 