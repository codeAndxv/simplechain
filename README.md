# PiCoinBlock
使用python构造一个简单的公链

文件作用：

- PiCoinTransaction: 
四个字段，付款人payer; 收款人recer; 金额count; 时间戳timestamp

- PiCoinWrapTransaction:
包装PiCoinTransaction, 增加hash，prev_hash字段

- PiCoinBlock：区块类，
区块序号 index；交易记录数量 mount； 生成区块的时间戳timestamp；工作量证明 proof；前一个区块的hash prev_hash；本区块的哈希 hash； 交易记录列表 transactionlist 

- PiCoinBlockChain:链类
区块列表  chain；交易列表 current_transactions用来暂时存储交易记录，一旦打块的时候，把这个列表放到新的区块中并且清空该列表；本条链的节点们  nodes；

- PiCoinBlockNode:使用flask框架来作为与链交互
