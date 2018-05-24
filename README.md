# blockchain-poc

# Usage

## Starting a node

You can start as many nodes as you want with the following steps:

1 - Change the port in blockchain_api.py and save the file
2 - Run in a new terminal: `python blockchain_api.py`
3 - Repeat

## Endpoints


### Requesting the Blockchain of a node

* `GET localhost:5000/chain`

### Mining a new block

* `GET localhost:5000/mine`

### Adding a new transaction

* `POST localhost:5000/transactions/new`

* __Body__: A transaction to be added

  ```json
  {
  	 "sender": "74ca08f91d364e1f950d0713814b6700",
  	 "recipient": "someone else's address",
  	 "amount": 5
  }
  ```

### Register a new node in the network
Currently you must add each new node to each running node.

* `POST localhost:5000/nodes/register`

* __Body__: A list of nodes to add

  ```json
  {
     "nodes": ["http://localhost:5001", <any-others>]
  }
  ```

### Resolving Blockchain differences in each node

* `GET localhost:5000/nodes/resolve`
