import hashlib
import datetime

class BlockChain:
  """
  Classe definissant le block
  """

  def __init__(self, liste_transactions, block_precedant):
    self.liste_transactions = liste_transactions
    self.block_precedant = block_precedant
    self.block_timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    self.block_raw_data = " - ".join(liste_transactions) + " - " + block_precedant
    self.hash = hashlib.sha256(self.block_raw_data.encode()).hexdigest()
    self.block_data = " Hash: " + self.hash + " BlockP Hash: " + self.block_precedant + " Transactions: " + str(self.liste_transactions) + " Timestamp: " + self.block_timestamp

  # Getters 
  def get_list_transactions(self):
    return self.liste_transactions

  def get_block_precedant(self):
    return self.block_precedant

  def get_block_raw_data(self):
    return self.block_raw_data

  def get_hash(self):
    return self.hash

  def get_block_data(self):
    return self.block_data
  
  def get_block_timestamp(self):
    return self.block_timestamp
  
  # Setters
  def set_list_transactions(self, liste_transactions):
    self.liste_transactions = liste_transactions

  def set_block_precedant(self, block_precedant):
    self.block_precedant = block_precedant

"""
t1 = "Clément envoie 2EUR a Paul"
t2 = "Paul envoie 3EUR a Mathieu"
t3 = "Mathieu envoie 1EUR a Clément"

b1 = BlockChain([t1], "Initial")
print(b1.get_block_data())

b2 = BlockChain([t2, t3], b1.get_hash())
print(b2.get_block_data())
"""



