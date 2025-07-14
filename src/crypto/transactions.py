from dataclasses import dataclass
from .tokens import Token

@dataclass
class Transaction:
    """
    Class representing a transaction in the blockchain.

    Attributes:
    sender (str): the sender
    receiver (str): the receiver
    token (Token): the token used in the transaction
    amount (float): the amount sent (in tokens)
    timestamp (datetime): datetime of the transaction
    """
    _sender: str
    _receiver: str
    _token: Token
    _amount: float
    _timestamp: str
    
    # Forcing good types
    def __post_init__(self):
        self.sender = self._sender
        self.receiver = self._receiver
        self.token = self._token
        self.amount = self._amount
        self.timestamp = self._timestamp
    
    @property
    def sender(self):
        return self._sender
    
    @property
    def receiver(self):
        return self._receiver
    
    @property
    def token(self):
        return self._token
    
    @property
    def amount(self):
        return self._amount

    @property
    def timestamp(self):
        return self._timestamp
    
    @sender.setter
    def sender(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Sender must be a string")
        self._sender = value
    
    @receiver.setter
    def receiver(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Receiver must be a string")
        self._receiver = value

    @token.setter
    def token(self, value: Token):
        if not isinstance(value, Token):
            raise TypeError("Token must be an instance of Token class")
        self._token = value

    @amount.setter
    def amount(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Amount must be a number (float or int)")
        self._amount = value

    @timestamp.setter
    def timestamp(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Timestamp must be a string")
        self._timestamp = value
