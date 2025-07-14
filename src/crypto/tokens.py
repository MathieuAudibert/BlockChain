from dataclasses import dataclass

@dataclass
class Token:
    """
    Handle tokens 
    
    Attributes:
    name (str): the name of the token
    symbol (str): the symbol of the token
    value (float): the price of 1 token
    """
    _name: str 
    _symbol: str
    _value: float


    # Forcing symbol and name to be strings and value to be a float
    def __post_init__(self):
        self.name = self._name
        self.symbol = self._symbol
        self.value = self._value
    
    @property
    def name(self):
        return self._name
    
    @property
    def symbol(self):
        return self._symbol

    @property
    def value(self):
        return self._value
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Token name must be a string")
        self._name = value
    
    @symbol.setter
    def symbol(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Token symbol must be a string")
        self._symbol = value

    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Token value must be a number")
        self._value = float(value)

