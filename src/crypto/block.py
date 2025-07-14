import hashlib
from dataclasses import dataclass

@dataclass
class Block:
    """
    Class representing a block in the blockchain

    Attributes:
    index (int): the index of the block in the chain
    timestamp (str): datetime of the block creation
    transactions (list): list of transactions in the block
    previous_hash (str): the hash of the previous block
    hash (str): the hash of the current block
    """
    #FIXME: ajouter un nonce ? / add a nonce ?

    _index: int
    _timestamp: str
    _transactions: list
    _previous_hash: str
    _hash: str
 
    # Forcing good types
    def __post_init__(self):
        self.index = self._index
        self.timestamp = self._timestamp
        self.transactions = self._transactions
        self.previous_hash = self._previous_hash
        # except for the genesis, each block has a computed hash
        if self._index == 0 and (self._previous_hash == '0' or self._hash == 'Genesis'):
            self.hash = self._hash
        else:
            self.hash = self.compute_hash()
    
    @property
    def index(self):
        return self._index
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def transactions(self):
        return self._transactions
    
    @property
    def previous_hash(self):
        return self._previous_hash
    
    @property
    def hash(self):
        return self._hash
    
    @index.setter
    def index(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Block index must be an integer")
        self._index = value

    @timestamp.setter
    def timestamp(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Block timestamp must be a string")
        self._timestamp = value

    @transactions.setter
    def transactions(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Block transactions must be a list")
        self._transactions = value

    @previous_hash.setter
    def previous_hash(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Block previous hash must be a string")
        self._previous_hash = value
    
    @hash.setter
    def hash(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Block hash must be a string")
        self._hash = value

    def compute_hash(self):
        """
        Compute the hash of the block using SHA-256
        """
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()
    
