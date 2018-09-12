#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 17:34
import hashlib  #信息安全加密
import json  #网络数据传递格式
import time  #时间
from typing import Optional, Dict, Any, List  #必要数据类型
from urllib.parse import urlparse  #url编码解码
from uuid import uuid4  #签名
import requests  #网络请求
from flask import Flask, jsonify, request  #flask网络框架

from PiCoin.PiCoinBlock import PiCoinBlock, picoinblock2dict
from PiCoin.PiCoinTransaction import PiCoinTransaction
from PiCoin.PiCoinWrapTransaction import PiCoinWrapTransaction


class PiCoinBlockChain:

    def __init__(self):
        self.chain = []    #区块列表
        self.current_transactions = []      #交易列表  wraptransaction
        self.nodes = set()  #节点
        self.new_block(proof = 100, prev_hash = "0")      #创建创世区块

    #新增区块
    def new_block(self,
                      proof:int,  #指定工作量类型
                      prev_hash  #默认是字符串
                      )->PiCoinBlock:  #指定返回值类型为字典

            prevhash = prev_hash or self.hash(self.chain[-1])
            block = PiCoinBlock(len(self.chain)  ,       #新增区块，原有区块索引加1,创世区块从0开始
                                     time.time(),       #时间戳
                                     self.current_transactions,         #交易
                                     proof,     #工作量证明
                                     prevhash ) #上个区块的哈希

            #把block字段都进行赋值
            block.assign_self()

            self.current_transactions = []  #开辟新的区块，即交易记录加入区块，当前交易需要被清空！！！
            self.chain.append(block)  #将区块追加到区块链表中

            return block

    def add_transaction(self, sender:str, recipient:str, amount:float)->PiCoinWrapTransaction:

        # 生成交易信息
        transaction = PiCoinTransaction(sender,     # 付款方
                                        recipient,      # 收款方
                                        amount      # 交易数额
                                        )
        #使用PiCoinWrapTransaction来包装PiCpinTransaction

        if len(self.current_transactions) ==0 :
            wrap_transaction = PiCoinWrapTransaction(transaction)
        else:
            wrap_transaction = PiCoinWrapTransaction(transaction,           #交易记录
                                 self.current_transactions[-1].hash       #前面一个记录的hash
                                 )
        wrap_transaction.seal()         #生成本次交易的hash并赋值到hash字段上

        self.current_transactions.append(wrap_transaction)

        return wrap_transaction


    @staticmethod
    def hash(block:PiCoinBlock)->str:        #传入一个PiCoinBlock，返回本区块的hash值

        return block.hash    #返回哈希值

    @property
    def last_block(self)->PiCoinBlock:
        return self.chain[-1]

    #挖矿依赖于上一个模块
    def proof_of_work(self, last_block)->int:   #挖矿获取工作证明
        last_proof = last_block.proof
        last_hash = self.hash(last_block)

        proof = 0   #循环求解符合条件的合法哈希
        #valid_proof:用于验证工作量证明是否符合条件
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof:int, proof:int)->bool:    #验证工作量证明
        guess = f'{last_proof}{proof}'.encode("utf-8")
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] == "000"   #计算难度

    def register_node(self, addr:str)->None: #加入网络中的其他节点，用于更新
        parsed_url = urlparse(addr) #url解析
        if parsed_url.netloc:  # 可以连接网络
            self.nodes.add(parsed_url.netloc)  # 增加网络节点
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("url无效")

    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:  # 区块链校验
        last_block = chain[0]  # 从第一块开始校验
        current_index = 1

        while current_index < len(chain):  # 循环校验
            block = chain[current_index]
            if block["prev_hash"] != self.hash(last_block):  # 区块校哈希验
                return False

            if not self.valid_proof(last_block["proof"],
                                    block["proof"]):  # 工作量校验
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self)->bool:  #冲突，一致性算法的一种
        #取得互联网中最长的链来替换当前的链
        neighbours = self.nodes  #备份节点  eg:127.0.0.1是一个节点，另一个不同的节点192.168.1.
        new_chain = None  #更新后的最长区块链
        max_length = len(self.chain)  #先保存当前节点的长度

        for node in neighbours:  #刷新每个网络节点，获取最长跟新
            response = requests.get(f'http://{node}/chain')  #取得其他节点的区块链
            if response.status_code == 200:  #网络请求成功
                length = response.json()["length"]  #取得邻节点区块链长度
                chain = response.json()["chain"]    #取得邻节点区块链

                #如果找到区块链长度大于当前节点区块链长度并且区块链校验合法，刷新并保存最长区块链
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain


        if new_chain:  #判断是否更新成功
            return True
        else:
            return  False
