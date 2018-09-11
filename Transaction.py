#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 14:39

import datetime


class Transaction:#交易类
    def __init__(self,
                payer,  #付款方
                recer,  #收款方
                count): #金额
        self.payer = payer
        self.recer = recer
        self.count = count
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return str(self.payer) + "  pay  "+ str(self.recer)+ "   "+str(self.count) + "  in  " + str(self.timestamp)

c