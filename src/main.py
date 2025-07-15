#!/usr/bin/env python 
import datetime
import json
import os
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token
from time import sleep

def load_transactions(file_path):
    """
    Load transactions from a JSON 

    Args:
    file_path (str): the path to the JSON 

    Returns:
    list: list of transactions objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transactions = []
    for tx in data['transactions']:
        token = Token(tx['token']['name'], tx['token']['symbol'], tx['token']['value'])
        transaction = Transaction(tx['sender'], tx['receiver'], token, tx['amount'], tx['timestamp'])
        transactions.append(transaction)
    
    return transactions

def create_blockchain(transactions):
    """
    Create a blockchain 

    Args:
    transactions (list): list of transactions objects

    Returns:
    BlockChain: a BlockChain object containing the genesis block and the blocks with transactions
    """
    genesis_block = Block(0, datetime.datetime.now().isoformat(), [], "0", "Genesis")
    blockchain = BlockChain([genesis_block], genesis_block)
    
    for i, tx in enumerate(transactions):
        previous_hash = blockchain.get_last().hash
        block = Block(i + 1, datetime.datetime.now().isoformat(), [tx], previous_hash, "")
        blockchain.blocks.append(block)
    
    return blockchain

def pretty_print_blockchain(blockchain):
    """
    Pretty print the blockchain information

    Args:
    blockchain (BlockChain): the blockchain to print

    Returns:
    None
    """
    print("\n=== Blockchain Overview ===")
    print(f"Genesis Block: (index={blockchain.genesis.index}, hash={blockchain.genesis.hash})")
    print("\nBlocks:")
    for block in blockchain.blocks:
        print(f"\n  Block #{block.index}")
        print(f"    Timestamp: {block.timestamp}")
        print(f"    Previous Hash: {block.previous_hash}")
        print(f"    Hash: {block.hash}")
        print(f"    Transactions:")
        if not block.transactions:
            print("      (No transactions)")
        for tx in block.transactions:
            print(f"      - {tx.sender} -> {tx.receiver} | {tx.amount} {tx.token.symbol} ({tx.token.name}) at {tx.timestamp}")


def log_blockchain(blockchain, file_path):
    """
    Log blockchain informations into a file

    Args:
    blockchain (BlockChain): the blockchain to log
    file_path (str): the path to the log file

    Returns:
    None
    """
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write("Blockchain created with genesis block:\n")
        f.write(str(blockchain.genesis) + "\n")
        f.write("Blocks in the blockchain:\n")
        for block in blockchain.blocks:
            f.write(str(block) + "\n")
        f.write("=" * 70 + "\n")


def main():
    # useful variables
    today_str = datetime.datetime.now().strftime('%d-%m-%Y')
    transactions_dir = os.path.join(os.path.dirname(__file__), 'transactions')
    results_dir = os.path.join(os.path.dirname(__file__), 'results', today_str)
    os.makedirs(results_dir, exist_ok=True)

    # get all transactions files (except template)
    files = [f for f in os.listdir(transactions_dir) if f.endswith('.json') and f != 'template.json']
    print(f"[{today_str}]: Blockchain simulation by @MathieuAudibert")
    print(f"[{today_str}]: Creating blockchain from all transaction files...")
    
    # create the genesis block and the blockchain
    genesis_block = Block(0, datetime.datetime.now().isoformat(), [], "0", "Genesis")
    blockchain = BlockChain([genesis_block], genesis_block)
    
    # process each transaction file
    for i, filename in enumerate(files):
        print(f"[{today_str}]: Processing {filename}...")
        file_path = os.path.join(transactions_dir, filename)
        transactions = load_transactions(file_path)
        
        previous_hash = blockchain.get_last().hash
        block = Block(i + 1, datetime.datetime.now().isoformat(), transactions, previous_hash, "")
        blockchain.blocks.append(block)
        print(f"[{today_str}]: Added block {i + 1} with {len(transactions)} transactions")

    #FIXME: a l'exterieur de la fonction main ? / outside main function ? 
    def block_to_dict(block):
        """
        Convert a Block object to a dictionary for JSON 
        
        Args:
        block (Block): the block to convert

        Returns:
        dict: a dictionary representation of the block
        """
        return {
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': [
                {
                    'sender': tx.sender,
                    'receiver': tx.receiver,
                    'token': {
                        'name': tx.token.name,
                        'symbol': tx.token.symbol,
                        'value': tx.token.value
                    },
                    'amount': tx.amount,
                    'timestamp': tx.timestamp
                } for tx in block.transactions
            ],
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }
    blockchain_data = {
        'genesis': block_to_dict(blockchain.genesis),
        'blocks': [block_to_dict(b) for b in blockchain.blocks]
    }
    result_file = os.path.join(results_dir, f'blockchain-{today_str}.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(blockchain_data, f, indent=2)

    # useful infos
    print(f"[{today_str}]: Blockchain created successfully!")
    print(f"[{today_str}]: done and saved in {result_file}")
    print(f"[{today_str}]: Total blocks: {len(blockchain.blocks)} (including genesis)")
    print(f"[{today_str}]: Total transactions: {sum(len(block.transactions) for block in blockchain.blocks)}")
    
    # log blockchain information
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_blockchain(blockchain, os.path.join(logs_dir, 'blocks.txt'))

if __name__ == "__main__":
    main()