#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 19:24
import json
import time
import hashlib

from PiCoinTransaction import picointransaction2dict, PiCoinTransaction


class PiCoinWrapTransaction: #交易纪录类
    def __init__(self, data , prev_hash = "0"):
        self.data = data    #交易信息
        self.hash = None  #自身哈希
        self.prev_hash = None   #上一个交易记录的哈希
        self.timestamp = time.time()
        self.payload_hash = self._hash_payload()    #负载哈希，data和时间戳的hash

    def _hash_payload(self): #交易哈希
        return hashlib.sha256((str(self.timestamp)+ str(self.data)).encode("utf-8")).hexdigest()

    def _hash_message(self):  #交易记录哈希，锁定交易(哈希在哈希)
        return hashlib.sha256((str(self.prev_hash) + str(self.payload_hash)).encode("utf-8")).hexdigest()


    # 密封，相当于将交易信息封装为一个带哈希验证值的数据结构 使得交易信息(包括交易数据和时间，交易链接的顺序)不能被修改
    def seal(self):
        self.hash = self._hash_message()        #对应数据锁定

    def validate(self):     #验证交易记录是否合法
        if self.payload_hash!=self._hash_payload():
            raise InvalidMessage("交易数据与时间被修改" + str(self))

        if self.hash != self._hash_message():  #判断消息链
            raise InvalidMessage("交易的哈希链接被修改" + str(self))

        return "data ok"+str(self)

    def __repr__(self):  #返回对象基本信息
        mystr = "hash:{}, prev_hash:{},data:{}".format(self.hash, self.prev_hash, self.data)
        return mystr
    def link(self, message):  #链接
        self.prev_hash = message.hash

class InvalidMessage(Exception):   #异常处理类
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


#用来解决Object of type 'XXX' is not JSON serializable问题
def picoinwraptransaction2dict(wraptransaction):
    return {
        'data':json.dumps(wraptransaction.data, default=picointransaction2dict),
        'prev_hash': wraptransaction.prev_hash,
        'hash':wraptransaction.hash,
        'timestamp':wraptransaction.timestamp
    }

if __name__ == '__main__':

    transaction = PiCoinTransaction(451648979651165654896789, 9898656413489714887, 100)


    wraptransaction = PiCoinWrapTransaction(transaction)
    wraptransaction.seal()
    print(json.dumps(wraptransaction, default=picoinwraptransaction2dict))