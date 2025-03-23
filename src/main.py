import os
import sys
import json
import datetime  
from blockchain.block_chain import BlockChain

def recup_transactions(path):
    """
    Recupere les transactions json
    
    Args:
        path (str): chemin du fichier json

    Returns:
        list: liste des transactions
    """

    try: 
        with open(path, 'r') as file:
            data = json.load(file)
            
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'transactions' in data:
            return data['transactions']
        else:
            print(f"Erreur: Format de transactions invalide pour {path}")
            return []
        
    except FileNotFoundError:
        print(f"Erreur: Fichier {path} introuvable")
        return []
    
    except json.JSONDecodeError:
        print(f"Erreur: Fichier {path} a un json invalide")
        return []
    
def creer_block_chain(transactions, transa_par_block=4):
    """
    Cree la chaine de blocks
    
    Args:
        transactions (list): liste des transactions
        transa_par_block (int): nombre de transactions par block

    Returns:
        list: liste des blocks
    """
    
    blockchaine = []

    for i in range(0, len(transactions), transa_par_block):
        lot = transactions[i:i+transa_par_block]

        if not blockchaine:
            block = BlockChain(lot, "Initial")
        else :
            block = BlockChain(lot, blockchaine[-1].get_hash())

        blockchaine.append(block)
    
    return blockchaine

def blockchaine_dict(blockchaine):
    """
    Convertit la chaine de blocks en dictionnaire
    
    Args:
        blockchaine (list): liste des blocks

    Returns:
        dict: dictionnaire des blocks
    """
    
    result = []
    
    for i, block in enumerate(blockchaine):
        block_dict = {
            "index": i,
            "date": block.get_block_timestamp(),
            "hash": block.get_hash(),
            "previous_hash": block.get_block_precedant(),
            "transactions": block.get_list_transactions(),
            "raw_data": block.get_block_raw_data()
        }
        result.append(block_dict)
    
    return result

def sauvegarder_en_json(blockchaine, transaction_file_name, path="results"):
    """
    Sauvegarde la chaine de blocks en json
    
    Args:
        blockchaine (list): liste des blocks
        transaction_file_name (str): nom du fichier de transactions
        path (str): chemin du fichier json
    """

    os.makedirs(path, exist_ok=True)
    date = datetime.datetime.now().strftime("%d-%m-%Y")  
    nomf = f"result_{transaction_file_name}_{date}.json"
    chemin = os.path.join(path, nomf)

    blockchaine_data = blockchaine_dict(blockchaine)

    with open(chemin, 'w') as file:
        json.dump(blockchaine_data, file, indent=4)
    
    return chemin

def main():
    
    fichier = input("Rentrez le nom du fichier de transactions: ").strip()
    transactionsf = os.path.join("transactions", fichier)  
    transactions = recup_transactions(transactionsf)

    if not transactions:
        print("Erreur: Aucune transaction")
        sys.exit(1)
    
    print(f"Nombre de transactions chargées: {len(transactions)}")

    blockchaine = creer_block_chain(transactions)
    
    fichier = sauvegarder_en_json(blockchaine, os.path.splitext(fichier)[0])
    print(f"Chaine de blocks sauvegardée dans {fichier}")

    return blockchaine

if __name__ == "__main__":
    main()