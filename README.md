# SiMa

数据字典。以史为录，提供快速查询的功能，故叫司马迁的司马

### 使用技术说明

- 前端
  - Vue 3
  - Ant UI
- 后端
  - Python 3.11
  - FastAPI
  - Elasticsearch

### 安装

- [本地安装](https://github.com/parker-pu/SiMa/blob/main/docs/LocalInstall.md)
- [Nginx 模式安装]()
- [Docker 模式安装]()
- [开发模式]()

### 使用手册

- [管理员模块（用户管理及数据库管理）](https://github.com/parker-pu/SiMa/blob/main/docs/AdminManage.md)
- [搜索模块](https://github.com/parker-pu/SiMa/blob/main/docs/SearchModel.md)
- [评论模块](https://github.com/parker-pu/SiMa/blob/main/docs/CommentModel.md)
- [普通模块](https://github.com/parker-pu/SiMa/blob/main/docs/OrdinaryModel.md)

### 展望

- 分页，目前后端分页完成，前端还未添加
- 表结构通过 binlog 同步
- 增加评论信息的搜索
- 增加日志功能
- 增加类似 navicat 的数据查询功能（RDBMS 及 Hive）
- 增加相关钩子函数，解析 SQL,构建元数据

### API

- Swagger UI

```shell
http://127.0.0.1:80/docs
```

- ReDoc

```shell
http://127.0.0.1:80/redoc
```

### 版本历程
- v1: (2020-12-29) 数据字典功能
- 2023.12 计划增加自动生成接口的功能