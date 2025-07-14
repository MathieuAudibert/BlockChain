import datetime
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token
from time import sleep

tekra = Token("Tekra", "TEK", 100.0)

transaction1 = Transaction("Mathieu", "Franck", tekra, 10.0, datetime.datetime.now().isoformat())
transaction2 = Transaction("Mathieu", "Franck", tekra, 5, datetime.datetime.now().isoformat())
sleep(2)
transaction3 = Transaction("Franck", "Roman", tekra, 8, datetime.datetime.now().isoformat())
sleep(2)
transaction4 = Transaction("Roman", "Elisa", tekra, 4, datetime.datetime.now().isoformat())
transaction5 = Transaction("Roman", "Juliette", tekra, 4, datetime.datetime.now().isoformat())

block1 = Block(0, datetime.datetime.now().isoformat(), [transaction1, transaction2], "0", "hash1")
block2 = Block(1, datetime.datetime.now().isoformat(), [transaction3], block1.hash, "")
block3 = Block(2, datetime.datetime.now().isoformat(), [transaction4, transaction5], block2.hash, "")

blockchain = BlockChain([block1, block2, block3], block1)

print("Blockchain created with genesis block:")
print(blockchain.genesis)
print("Blocks in the blockchain:")
for block in blockchain.blocks:
    print(block)

def pretty_print_blockchain(blockchain):
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


def main():
    print(f"[{datetime.datetime.now().strftime("%d-%m-%Y")}]: Blockchain simulation by @MathieuAudibert")
    print(f"[{datetime.datetime.now().strftime("%d-%m-%Y")}]: Select the transaction file to add to the blockchain :")
    print(f"[{datetime.datetime.now().strftime("%d-%m-%Y")}]: ")
    pretty_print_blockchain(blockchain)

if __name__ == "__main__":
    main()