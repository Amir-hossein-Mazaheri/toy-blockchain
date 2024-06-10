import json
import os
import glob
import re
from hashlib import sha256

genesis_block = None

ledgers = []

blocks = []


def initial_load():
    with open('GenesisBlock/GenesisBlock.json', 'r') as file:
        global genesis_block
        genesis_block = json.load(file)

    ledgers_path = 'Ledgers'
    ledgers_files_path = glob.glob(os.path.join(ledgers_path, '*'))

    for ledger in ledgers_files_path:
        if os.path.isfile(ledger):
            with open(ledger, 'r') as file:
                ledgers.append(json.load(file))

    ledgers.sort(key=lambda block: block["blockNumber"])

    problems_path = 'Math_Problems'
    problems_files_path = glob.glob(os.path.join(problems_path, '*'))

    # sort based on math problem number, so I can add problem to ledger based on their indexes
    problems_files_path.sort(key=lambda p: int(re.search(r'Math_Problem_Number(\d+)', p).group(1)))

    for i, problem in enumerate(problems_files_path):
        if os.path.isfile(problem):
            with open(problem, 'r') as file:
                ledgers[i]["mathProblem"] = json.load(file)["mathProblem"]


def add_block(prev_block, ledger):
    math_problem = ledger["mathProblem"]

    block = {
        k: v for k, v in ledger.items() if k != "mathProblem"
    }
    # previous block hash value which is stored on it should not be in the
    # prev_hash because I just added hash to print it later and in bitcoin
    # it's not part of the hash
    block["prev_hash"] = sha256(json.dumps({
        k: v for k, v in prev_block.items() if k != "hash"
    }).encode()).hexdigest()
    block["nonce"] = 0

    while True:
        hash = sha256(json.dumps(block).encode()).hexdigest()

        if hash[:len(math_problem)] == math_problem:
            block["hash"] = hash
            return block

        block["nonce"] += 1


def fill_blocks():
    blocks.append(genesis_block)

    for i, ledger in enumerate(ledgers):
        block = add_block(blocks[i], ledger)

        print(f"Block Number: {block['blockNumber']}")
        print(f"Block Hash: {block['hash']}")
        print(f"Previous Block Hash: {block['prev_hash']}")
        print(f"Nonce: {block['nonce']}")
        print("-" * 100)

        blocks.append(block)


if __name__ == '__main__':
    initial_load()

    fill_blocks()
