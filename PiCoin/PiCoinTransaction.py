#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 19:22
import time
import json

class PiCoinTransaction:#交易类
    def __init__(self,
                payer,  #付款方
                recer,  #收款方
                count): #金额

        self.payer = str(payer)
        self.recer = str(recer)
        self.count = count
        self.timestamp = time.time()

    def __repr__(self):
        return str(self.payer) + "  pay  "+ str(self.recer)+ "   "+str(self.count) + "  in  " + str(self.timestamp)



#用来解决Object of type 'XXXXX' is not JSON serializable问题
def picointransaction2dict(transaction):
    return {
        'payer':transaction.payer,
        'recer':transaction.recer,
        'count':transaction.count,
        'timestamp':transaction.timestamp
    }

if __name__ == '__main__':
    transaction = PiCoinTransaction(451648979651165654896789, 9898656413489714887, 100)

    print(json.dumps(transaction, default=picointransaction2dict))