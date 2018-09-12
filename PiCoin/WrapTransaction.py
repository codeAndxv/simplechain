#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 14:47

import time
import hashlib
from PiCoin.Transaction import Transaction

class WrapTransaction: #交易纪录类
    def __init__(self, data):
        self.data = data    #交易信息
        self.hash = None  #自身哈希
        self.prev_hash = None   #上一个交易记录的哈希
        self.timestamp = time.time()
        self.payload_hash = self._hash_payload()    #锁定哈希

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

if __name__ == '__main__': #单独模块测试
    try:
        t1 = Transaction("chaors", "yajun", 999999999)
        t2 = Transaction("chaors2", "yajun2", 999999999)

        m1 = WrapTransaction(t1)
        m2 = WrapTransaction(t2)

        #交易密封
        m1.seal()
        #交易哈希只有密封之后才能link
        m2.link(m1)
        m2.seal()

        m1.validate()
        m2.validate()
        # 篡改数据 篡改数据后会捕获到异常
        # m2.data = "hahahaha"
        # m2.validate()
        #
        m2.prev_hash = "kkkkk"
        # print(m2)
        m2.validate()
    except InvalidMessage as e:
        print(e)