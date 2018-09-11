#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 15:19


# block = {
#     'index': 1,
#     'timestamp': 1506057125.900785,
#     'transactions': [
#         {
#             'sender': "8527147fe1f5426f9dd545de4b27ee00",
#             'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
#             'amount': 5,
#         }
#     ],
#     'proof': 324984774000,
#     'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
# }

import datetime
import hashlib
from Message import ChaorsMessage
from Message import InvalidMessage
from Transaction import Transaction


class Block:
    def __init__(self, *args):
        self.messagelist = []       #存储多个交易记录
        self.timestamp = None       #当前时间戳
        self.hash = None
        self.prev_hash = None

        #把所有的交易都加入到交易列表中
        if args:
            for arg in args:
                self.add_message(arg)

    def add_message(self, msg):  #增加交易信息
        #判断是否已经有第一条交易信息
        if len(self.messagelist) > 0 :
            msg.link(self.messagelist[-1])
        msg.seal()
        msg.validate()
        self.messagelist.append(msg)

    def link(self, block):   #链接
        #当前区块的上个哈希值为上个区块哈希值
        block.hash = self.prev_hash

    def seal(self):  #区块封装，带有时间戳和哈希值的数据结构
       self.timestamp = datetime.datetime.now()
       self.hash = self._hash_block()

     #求区块的哈希值
    def _hash_block(self):
        sum = ""
        for message in self.messagelist:
           sum = sum + str(message.hash)
        return hashlib.sha256((str(self.prev_hash) +
                              str(self.timestamp) +
                              sum).encode("utf-8")).hexdigest()

    def validate(self):  #区块合法性验证
        for i, msg in enumerate(self.messagelist):
           msg.validate()
           if i > 0 and msg.prev_hash != self.messagelist[i-1].hash:
               raise InvalidBlock("无效block，第{}条交易记录被修改".format(i)+ str(self))

        return str(self) + "block ok..."

class InvalidBlock(Exception):  #异常处理类

   def __init__(self, *args, **kwargs):
       Exception.__init__(self, *args, **kwargs)


if __name__ == '__main__':

   try:
       t1 = Transaction("chaors", "yajun", 999999999)
       t2 = Transaction("chaors2", "yajun2", 999999999)
       t3 = Transaction("chaors4", "yajun4", 999999999)

       m1 = ChaorsMessage(t1)
       m2 = ChaorsMessage(t2)
       m3 = ChaorsMessage(t3)

       block = Block(m1, m2, m3)
       block.seal()
       print(block)
       # m1.data = "kkkk"
       block.messagelist[1] = m3
       block.validate()

   except InvalidMessage as e:
       print(e)

   except InvalidBlock as e:
       print(e)