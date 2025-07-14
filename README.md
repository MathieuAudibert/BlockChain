![Bugs](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=bugs)
![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=code_smells)
![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=coverage)

# Token, block & blockchain learning

Understanding basic cryptographics through this Python project.

I learned how to :

- Create my own token (Tekra)
- Create blocks of this token (or transactions with any other tokens/currency)
- Create block-chains for these blocks
- Create result files and logs dated

## Usefull docs

https://www.coinbase.com/fr-fr/learn/crypto-basics/what-is-a-token

# Config

- Python 3.x

# Usage

- [Optionnal]: Remove the tests files in `/src/transactions/` and `/src/results`
- Install dependecies `cd /src` --> `pip install -r requirements.txt`
- Add your transactions in `/src/transactions` based of **template.json**
- Run `cd /src` --> `python main.py`
- You can then access logs in `/src/logs/blocks.txt` and results in `/src/today-date/blockchain-today-date.json`
