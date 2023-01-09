import hashlib
import datetime

class Block:
    def __init__(self, timestamp, transactions, previous_hash):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(datetime.datetime.now(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address):
        block = Block(datetime.datetime.now(), self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        print(f"Block mined: {block.hash}")
        self.chain.append(block)
        self.pending_transactions = [{"from": "mining reward", "to": mining_reward_address, "amount": 1}]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["from"] == address:
                    balance -= transaction["amount"]
                if transaction["to"] == address:
                    balance += transaction["amount"]
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def check_halving(self):
        if self.block_counter % 52000 == 0:
            self.mining_reward /= 2
            print(f"Halving occurred, mining reward is now {self.mining_reward}")

blockchain = Blockchain()

print("Mining block 1...")
blockchain.create_transaction("a", "b", 100)
blockchain.create_transaction("c", "d", 10)
blockchain.mine_pending_transactions("x")

print("Mining block 2...")
blockchain.create_transaction("a", "b", 50)
blockchain.create_transaction("c", "d", 5)
blockchain.mine_pending_transactions("x")

print("Mining block 3...")
blockchain.create_transaction("a", "b", 25)
blockchain.create_transaction("c", "d", 2.5)
blockchain.mine_pending_transactions("x")

print(f"Blockchain is valid: {blockchain.is_chain_valid()}")
