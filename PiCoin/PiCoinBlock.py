#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 19:21

import json
import hashlib
import time
import array

from PiCoin.PiCoinWrapTransaction import picoinwraptransaction2dict

class PiCoinBlock:
    def __init__(self, index, timestamp, transactions, proof, prev_hash):
        self.index = index                  #本区块的序号
        self.mount = 0                      #本区块的交易记录的数量
        self.transactionlist = transactions       #存储多个交易记录
        self.timestamp = timestamp          #当前时间戳
        self.proof = proof                  #工作量证明
        self.hash = None                    #本区块的hash
        self.prev_hash = prev_hash          #前一个区块的hash


    def assign_self(self):
        self.mount = len(self.transactionlist)
        self._hash_()

    #生成hash并复制到hash字段上
    def _hash_(self):
        sum = ""
        for transaction in self.transactionlist:
            sum  = sum + str(transaction.hash)

        self.hash =  hashlib.sha256((str(self.index)
                              +str(self.mount)
                              +sum
                              + str(self.timestamp)
                              + str(self.proof)
                              + str(self.prev_hash)).encode("utf-8")).hexdigest()



#用来解决Object of type 'PiCoinBlock' is not JSON serializable问题
def picoinblock2dict(block):
    return {
        'index':block.index,
        'mount':block.mount,
        'timestamp':block.timestamp,
        'proof':block.proof,
        'prev_hash':block.prev_hash,
        'hash':block.hash,
        'transactionlist':json.dumps(block.transactionlist, default=picoinwraptransaction2dict)
    }

if __name__ == '__main__':
    picoin = PiCoinBlock(1, time.time(), [], 100, "4546168798646")
    picoin.assign_self()
    print(json.dumps(picoin, default=picoinblock2dict))