import os
from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

RPC = os.environ.get("RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC))

MERCHANT = "0xdXXXX".lower()  # GANTI DENGAN WALLET KAMU
USDT = "0xdBE9Dd24BE7ad52f5b6bda078662080e4c408a4A".lower()

TRANSFER_EVENT_SIG = w3.keccak(text="Transfer(address,address,uint256)").hex()

@app.route("/")
def home():
    return "AI AGENT CRYPTO ENGINE LIVE"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    tx_hash = data.get("tx_hash")
    expected_amount = int(data.get("amount"))

    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        if receipt.status != 1:
            return jsonify({"status": "failed"})

        for log in receipt.logs:
            if log.address.lower() == USDT and log.topics[0].hex() == TRANSFER_EVENT_SIG:
                to_address = "0x" + log.topics[2].hex()[-40:]
                value = int(log.data, 16)

                if to_address.lower() == MERCHANT and value >= expected_amount:
                    return jsonify({"status": "success"})

    except:
        pass

    return jsonify({"status": "failed"})
