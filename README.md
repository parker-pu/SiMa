# SiMa

数据字典。以史为录，提供快速查询的功能，故叫司马迁的司马

### 使用技术说明

- 前端
  - Vue 3
- 后端
  - Python 3.10
  - FastAPI
  - Elasticsearch

### 安装

- [本地安装](https://github.com/parker-pu/SiMa/blob/main/docs/LocalInstall.md)
- [Nginx 模式安装]()
- [Docker 模式安装]()
- [开发模式]()

### 使用手册
- 管理员模块（用户管理及数据库管理）
- 搜索模块
- 评论模块

### 展望
- 表结构通过 binlog 同步
- 增加类似 navicat 的数据查询功能（RDBMS及Hive）
- 增加相关钩子函数，解析SQL,构建元数据
