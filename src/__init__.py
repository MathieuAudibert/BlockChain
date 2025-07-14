"""
BlockChain-1: A Python blockchain implementation

This package contains a simple blockchain implementation with:
- Block creation and management
- Transaction handling
- Token system
- Blockchain validation

Author: @MathieuAudibert
"""

__version__ = "1.0.0"
__author__ = "@MathieuAudibert"

# Import main classes for easy access
from .crypto.block_chain import BlockChain
from .crypto.block import Block
from .crypto.transactions import Transaction
from .crypto.tokens import Token

__all__ = [
    'BlockChain',
    'Block', 
    'Transaction',
    'Token'
] 