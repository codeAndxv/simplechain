#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 18:10
import json
from uuid import uuid4 #签名
import requests
from flask import Flask, jsonify, request   #flask网络框架

from PiCoin.PiCoinBlock import picoinblock2dict
from PiCoin.PiCoinBlockChain import PiCoinBlockChain
from PiCoin.PiCoinWrapTransaction import picoinwraptransaction2dict


class PiCoinBlockNode:
    def __init__(self):
        self.picoin = PiCoinBlockChain()     #创建一条链
        self.node_id = str(uuid4()).replace("-", "")     #生成节点密钥 即钱包地址
        print("当前节点钱包地址：" , self.node_id)

        self.app = Flask(__name__)  #初始化flask框架


        @self.app.route("/")
        def index_page():
            return "welcome to PiCoin..."

        @self.app.route("/chain")  #查看所有区块链
        def index_chain():
            response = {
                "chain":json.dumps(self.picoin.chain, default=picoinblock2dict),  #区块链
                "length":len(self.picoin.chain)  #区块链长度
            }
            return jsonify(response), 200

        @self.app.route("/mine")     #挖矿
        def index_mine():
            last_block = self.picoin.last_block
            proof = self.picoin.proof_of_work(last_block)

            #系统奖励挖矿币
            self.picoin.add_transaction(
                sender="0",
                recipient = self.node_id,
                amount = 12.5
            )

            block = self.picoin.new_block(proof, self.picoin.hash(last_block))

            response = {
                "message" : "new block created.....",
                "index" : block.index,
                "transactions" : json.dumps(block.transactionlist, default=picoinwraptransaction2dict),
                "proof" : block.proof,
                "hash" : block.hash,
                "prev_hash" : block.prev_hash
            }

            return jsonify(response), 200

        #新增交易记录
        @self.app.route("/add_transaction", methods=["POST"])
        def index_add_transaction():
            values  = request.get_json()
            wraptransaction = self.picoin.add_transaction(
                sender=values.get("sender"),
                recipient = values.get("recipient"),
                amount = values.get("amount")
            )

            response = {
                "message": "new transaction created.....",
                "hash": wraptransaction.hash,
                "prev_hash": wraptransaction.prev_hash,
                "timestamp": wraptransaction.timestamp,
                "data": wraptransaction.data
            }

            return jsonify(response), 200


        @self.app.route("/new_node", methods=["POST"])       #新增节点
        def index_new_node():
            values = request.get_json()
            nodes = values.get("nodes")     #获取所有节点

            if nodes is None:
                return "怎么是空节点"

            for node in nodes:
                self.picoin.register_node(node)

            response = {
                "message": "网络节点加入到区块",
                "nodes":list(self.picoin.nodes)
            }

            return jsonify(response), 200

        @self.app.route("/node_refresh")  #刷新节点
        def index_node_refresh():
            replaced = self.picoin.resolve_conflicts()  #一致性算法进行最长链选择

            print(replaced)

            if replaced:
                response = {
                "message": "区块链被替换为最长有效链",
                "new chain": self.picoin.chain
                }
            else:
                response = {
                    "message": "当前区块链为最长无需替换",
                    "chain": self.picoin.chain
                }
            return jsonify(response), 200

if __name__ == '__main__':
    node = PiCoinBlockNode()
    node.app.run()