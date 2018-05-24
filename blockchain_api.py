from flask import Flask, jsonify, request
from textwrap import dedent
from uuid import uuid4

from blockchain import Blockchain


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


# Tells the server to mine a new block.
@app.route('/mine', methods=['GET'])
def mine():
    """
    Steps:

    - Calculate the Proof of Work
    - Reward the miner by adding a transaction granting us 1 coin
    - Forge the new Block by adding it to the chain
    """

    # Run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    # The recipient of the mined block is the address of the node
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Example Post Request:

    {
     "sender": "my address",
     "recipient": "someone else's address",
     "amount": 100
    }
    """

    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


# Returns the full Blockchain.
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# Adds neighbouring nodes
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    Accepts a list of new nodes in the form of URLs

    Example Post Request:

    {
    	 "nodes" : ["http://localhost:5001"]
    }
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# Implement the Consensus Algorithm, which resolves any conflicts
# to ensure a node has the correct chain.
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Old chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Current chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
