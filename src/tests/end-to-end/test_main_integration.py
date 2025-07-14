import pytest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from crypto.block_chain import BlockChain
from crypto.block import Block
from crypto.transactions import Transaction
from crypto.tokens import Token


class TestMainIntegration:
    """Integration tests for the main function and complete workflow."""
    
    @patch('builtins.print')
    def test_main_function_complete_workflow(self, mock_print):
        """Test the complete main function workflow."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Create test transaction files
            test_files = [
                {
                    "filename": "transactions1.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Alice",
                                "receiver": "Bob",
                                "token": {"name": "Bitcoin", "symbol": "BTC", "value": 1.0},
                                "amount": 10.0,
                                "timestamp": "2025-07-15T12:00:00"
                            }
                        ]
                    }
                },
                {
                    "filename": "transactions2.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Bob",
                                "receiver": "Charlie",
                                "token": {"name": "Ethereum", "symbol": "ETH", "value": 2.0},
                                "amount": 5.0,
                                "timestamp": "2025-07-15T12:05:00"
                            }
                        ]
                    }
                }
            ]
            
            # Write test files
            for test_file in test_files:
                file_path = os.path.join(transactions_dir, test_file["filename"])
                with open(file_path, 'w') as f:
                    json.dump(test_file["data"], f)
            
            # Mock the datetime to have a consistent date
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "15-07-2025"
                
                # Import and run main function
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                # Mock the os.path.dirname to return our temp directory
                with patch('os.path.dirname', return_value=temp_dir):
                    from main import main
                    main()
                
                # Verify that the results directory was created
                results_dir = os.path.join(temp_dir, "results", "15-07-2025")
                assert os.path.exists(results_dir)
                
                # Verify that the blockchain JSON file was created
                blockchain_file = os.path.join(results_dir, "blockchain-15-07-2025.json")
                assert os.path.exists(blockchain_file)
                
                # Verify the JSON content
                with open(blockchain_file, 'r') as f:
                    blockchain_data = json.load(f)
                
                assert "genesis" in blockchain_data
                assert "blocks" in blockchain_data
                assert blockchain_data["genesis"]["index"] == 0
                assert len(blockchain_data["blocks"]) == 3  # genesis + 2 blocks
                
                # Verify the blocks
                assert blockchain_data["blocks"][1]["index"] == 1
                assert blockchain_data["blocks"][2]["index"] == 2
                assert len(blockchain_data["blocks"][1]["transactions"]) == 1
                assert len(blockchain_data["blocks"][2]["transactions"]) == 1
    
    def test_main_function_ignores_template_json(self):
        """Test that main function ignores template.json files."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Create test files including template.json
            test_files = [
                {
                    "filename": "template.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Template",
                                "receiver": "User",
                                "token": {"name": "Template", "symbol": "TPL", "value": 0.0},
                                "amount": 0.0,
                                "timestamp": "2025-07-15T12:00:00"
                            }
                        ]
                    }
                },
                {
                    "filename": "transactions1.json",
                    "data": {
                        "transactions": [
                            {
                                "sender": "Alice",
                                "receiver": "Bob",
                                "token": {"name": "Bitcoin", "symbol": "BTC", "value": 1.0},
                                "amount": 10.0,
                                "timestamp": "2025-07-15T12:00:00"
                            }
                        ]
                    }
                }
            ]
            
            # Write test files
            for test_file in test_files:
                file_path = os.path.join(transactions_dir, test_file["filename"])
                with open(file_path, 'w') as f:
                    json.dump(test_file["data"], f)
            
            # Mock the datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "15-07-2025"
                
                # Import and run main function
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                with patch('os.path.dirname', return_value=temp_dir):
                    from main import main
                    main()
                
                # Verify that only the non-template file was processed
                results_dir = os.path.join(temp_dir, "results", "15-07-2025")
                blockchain_file = os.path.join(results_dir, "blockchain-15-07-2025.json")
                
                with open(blockchain_file, 'r') as f:
                    blockchain_data = json.load(f)
                
                # Should have 2 blocks: genesis + 1 transaction block (template ignored)
                assert len(blockchain_data["blocks"]) == 2
                
                # Verify that template transaction is not in the blockchain
                genesis_transactions = blockchain_data["genesis"]["transactions"]
                block1_transactions = blockchain_data["blocks"][1]["transactions"]
                
                # Check that no transaction has "Template" as sender
                all_transactions = genesis_transactions + block1_transactions
                template_senders = [tx["sender"] for tx in all_transactions if tx.get("sender") == "Template"]
                assert len(template_senders) == 0
    
    def test_main_function_creates_directories(self):
        """Test that main function creates necessary directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Create a simple test file
            test_file = {
                "filename": "transactions1.json",
                "data": {
                    "transactions": [
                        {
                            "sender": "Alice",
                            "receiver": "Bob",
                            "token": {"name": "Bitcoin", "symbol": "BTC", "value": 1.0},
                            "amount": 10.0,
                            "timestamp": "2025-07-15T12:00:00"
                        }
                    ]
                }
            }
            
            file_path = os.path.join(transactions_dir, test_file["filename"])
            with open(file_path, 'w') as f:
                json.dump(test_file["data"], f)
            
            # Mock the datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "15-07-2025"
                
                # Import and run main function
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                with patch('os.path.dirname', return_value=temp_dir):
                    from main import main
                    main()
                
                # Verify that results directory was created
                results_dir = os.path.join(temp_dir, "results", "15-07-2025")
                assert os.path.exists(results_dir)
                assert os.path.isdir(results_dir)
                
                # Verify that logs directory was created (if it doesn't exist)
                logs_dir = os.path.join(temp_dir, "logs")
                if os.path.exists(logs_dir):
                    assert os.path.isdir(logs_dir)
    
    def test_main_function_logs_blockchain(self):
        """Test that main function logs blockchain information."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Create logs directory
            logs_dir = os.path.join(temp_dir, "logs")
            os.makedirs(logs_dir)
            
            # Create a test file
            test_file = {
                "filename": "transactions1.json",
                "data": {
                    "transactions": [
                        {
                            "sender": "Alice",
                            "receiver": "Bob",
                            "token": {"name": "Bitcoin", "symbol": "BTC", "value": 1.0},
                            "amount": 10.0,
                            "timestamp": "2025-07-15T12:00:00"
                        }
                    ]
                }
            }
            
            file_path = os.path.join(transactions_dir, test_file["filename"])
            with open(file_path, 'w') as f:
                json.dump(test_file["data"], f)
            
            # Mock the datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "15-07-2025"
                
                # Import and run main function
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                with patch('os.path.dirname', return_value=temp_dir):
                    from main import main
                    main()
                
                # Verify that log file was created
                log_file = os.path.join(logs_dir, "blocks.txt")
                assert os.path.exists(log_file)
                
                # Verify log content
                with open(log_file, 'r') as f:
                    log_content = f.read()
                    assert "Blockchain created with genesis block" in log_content
                    assert "Blocks in the blockchain" in log_content
                    assert "=" * 70 in log_content  # Separator line
    
    def test_main_function_handles_empty_transactions_directory(self):
        """Test that main function handles empty transactions directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create empty transactions directory
            transactions_dir = os.path.join(temp_dir, "transactions")
            os.makedirs(transactions_dir)
            
            # Mock the datetime
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "15-07-2025"
                
                # Import and run main function
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                with patch('os.path.dirname', return_value=temp_dir):
                    from main import main
                    main()
                
                # Verify that results directory was created
                results_dir = os.path.join(temp_dir, "results", "15-07-2025")
                assert os.path.exists(results_dir)
                
                # Verify that blockchain JSON file was created with only genesis block
                blockchain_file = os.path.join(results_dir, "blockchain-15-07-2025.json")
                assert os.path.exists(blockchain_file)
                
                with open(blockchain_file, 'r') as f:
                    blockchain_data = json.load(f)
                
                # Should have only genesis block
                assert len(blockchain_data["blocks"]) == 1
                assert blockchain_data["genesis"]["index"] == 0 