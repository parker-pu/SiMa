# 本地安装

### 注意事项

- 本地安装仅需关注 FastApi 这个文件夹即可
- 第一次安装，如果 “SiMa\FastApi\sima” 目录下有 conn.json 这个文件需要删掉，这个文件是记录初始化的相关数据

### 安装步骤

- 安装 Python（注意版本需要最新版，3.8 及其之后）
- 安装相关包（pip 或者 pipevn 任选）
  - pip
  ```shell
  pip install -r requirements.txt
  ```
  - pipenv
  ```
  pipenv install
  ```
- 启动使用即可（在目录 SiMa\FastApi\sima 下）

```shell
python3 manage.py
```

### 启动之后需要在 web 界面输入初始化信息

- 第一次会跳出初始化页面，输出所需信息
  - ES 地址
  - ES 端口
  - 超级用户账号
  - 超级用户密码
 ![初始化](https://github.com/parker-pu/SiMa/blob/main/docs/imgs/%E5%88%9D%E5%A7%8B%E5%8C%96.png)
