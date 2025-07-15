[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=bugs&token=d7be540c8103597de4b21fa888b5daad459600e4)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_BlockChain)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=code_smells&token=d7be540c8103597de4b21fa888b5daad459600e4)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_BlockChain)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_BlockChain&metric=coverage&token=d7be540c8103597de4b21fa888b5daad459600e4)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_BlockChain)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/cap92/blockchainspython)

# Token, block & blockchain learning

Understanding basic cryptographics through this Python project.

I learned how to :

- Create my own token (Tekra)
- Create blocks of this token (or transactions with any other tokens/currency)
- Create block-chains for these blocks
- Create result files and logs dated
- Setup properly Sonarqube, Python & Pytest/Tox

# CI/CD

Each commit is analyzed by Sonarqube and Pytest/Tox wich then is pushed to the dockerhub official image `https://hub.docker.com/repository/docker/cap92/blockchainspython/general`

## Usefull docs

https://www.coinbase.com/fr-fr/learn/crypto-basics/what-is-a-token

# Config

- Python 3.x
- Docker

# Usage

- [Optionnal]: Remove the tests files in `/src/transactions/` and `/src/results`
- Add your transactions in `/src/transactions` based of **template.json**
- Run `cd /src` --> `python main.py`
- You can then access logs in `/src/logs/blocks.txt` and results in `/src/today-date/blockchain-today-date.json`

# Installation

You can either clone this repository with `git clone https://github.com/MathieuAudibert/BlockChain.git`

or pull its public image using Docker `docker image pull cap92/blockchainspython` or Podman `podman image pull cap92/blockchainspython`
