import datetime
from dataclasses import dataclass
from .block import Block
from .tokens import Token
from .transactions import Transaction

@dataclass
class BlockChain:
  """
  Class representing a blockchain.

  Attributes:
  blocks (list[Block]): list of blocks in the blockchain
  genesis (Block): the first block of the blockchain
  """
  _blocks: list[Block]
  _genesis: Block

  # Forcing good types
  def __post_init__(self):
    self.blocks = self._blocks
    self.genesis = self._genesis

  @property
  def blocks(self):
    return self._blocks
  
  @property
  def genesis(self):
    return self._genesis
  
  @blocks.setter
  def blocks(self, value: list[Block]):
    if not isinstance(value, list):
      raise TypeError("Blocks must be a list")
    for block in value:
      if not isinstance(block, Block):
        raise TypeError("All items in blocks must be Block instances")
    self._blocks = value

  @genesis.setter
  def genesis(self, value: Block): 
    if not isinstance(value, Block):
      raise TypeError("Genesis must be a Block instance")
    self._genesis = value

  def genesis_creation(self):
    """
    Create the genesis block and add it to the blockchain.
    """
    block = Block(index=0, timestamp=datetime.datetime.now().isoformat(), transactions=[], previous_hash="0", hash="Genesis")
    self.blocks.append(block)
  
  def get_last(self):
    """
    Get the last block in the blockchain.
    
    Returns:
    Block: the last block in the blockchain
    """
    if not self.blocks:
      raise ValueError("Blockchain is empty")
    return self.blocks[-1]
  
  def add_block(self, block: Block):
    """
    Add a new block to the blockchain.
    
    Args:
    block (Block): the block to add
    """
    if not isinstance(block, Block):
      raise TypeError("Block must be an instance of Block class")
    if self.blocks:
      last = self.get_last()
      if block.previous_hash != last.hash:
        raise ValueError("Block's previous hash does not match the last block's hash")
      new = Block(index=last.index + 1, timestamp=datetime.datetime.now().isoformat(), transactions=block.transactions, previous_hash=last.hash, hash=block.hash)
      self.blocks.append(new)

