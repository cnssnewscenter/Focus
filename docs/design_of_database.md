# 数据库设计

使用mongodb 作为后端

1. meta collection 存储元数据
2. 每个项目有一个独立的 hmac 编号，通过这个编号对不同的项目进行区分
3. 每个项目占据独立的一个collection，名字为 hmac 
