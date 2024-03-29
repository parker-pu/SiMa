# -*- encoding: utf-8 -*-
"""
@Contact :   i54605@outlook.com
@License :   (C)Copyright 2023-2025

处理错误
"""
from pydantic import BaseModel


class ErrorBase(BaseModel):
    code: int
    msg: str = ""


# 找不到路径
ERROR_NOT_FOUND = ErrorBase(code=404, msg="api 路径错误,或者没有数据")
# 参数错误
ERROR_PARAMETER_ERROR = ErrorBase(code=400, msg="参数错误")

# 用户相关
ERROR_USER_TOKEN_FAILURE = ErrorBase(code=5004, msg="未登录或登录过期")
ERROR_USER_NOT_FOUND = ErrorBase(code=5004, msg="用户不存在")
ERROR_USER_PASSWORD_ERROR = ErrorBase(code=5005, msg="密码错误")
ERROR_USER_NOT_ACTIVATE = ErrorBase(code=5006, msg="用户账号尚未")
ERROR_USER_ACCOUNT_EXISTS = ErrorBase(code=5007, msg="账号已存在")
ERROR_USER_EMAIL_NOT_EXISTS = ErrorBase(code=5008, msg="邮箱不存在")
ERROR_FORGET_PWD_TOKEN_ERROR = ErrorBase(code=5009, msg="重置密码链接错误或已过期")
ERROR_USER_REGISTER_TOKEN_ERROR = ErrorBase(code=5031, msg="注册验证链接已过期或不存在")
ERROR_USER_REGISTER_EXISTS = ErrorBase(code=5032, msg="注册失败，可能账号已存在。")
ERROR_USER_REGISTER_ERROR = ErrorBase(code=5033, msg="注册失败，请重试。")
ERROR_USER_REGISTER_TO_OFTEN = ErrorBase(code=5034, msg="提交注册太频繁，请稍后重试")
ERROR_USER_EMAIL_EXISTS = ErrorBase(code=5011, msg="邮箱不可用")
ERROR_USER_PHONE_EXISTS = ErrorBase(code=5012, msg="手机号码不可用")
ERROR_USER_USERNAME_EXISTS = ErrorBase(code=5013, msg="用户名不可用")
ERROR_USER_CAPTCHA_CODE_ERROR = ErrorBase(code=5021, msg="验证码错误")
ERROR_USER_CAPTCHA_CODE_INVALID = ErrorBase(code=5022, msg="验证码已失效，请重试。")
ERROR_USER_PREM_ADD_ERROR = ErrorBase(code=5031, msg="权限标识添加失败")
ERROR_USER_PREM_ERROR = ErrorBase(code=5403, msg="权限不足")

# 接口验证相关
ERROR_FILE_NOT_EXISTS_ERROR = ErrorBase(code=5010, msg="文件不存在")
ERROR_NO_MAP_DATA_ERROR = ErrorBase(code=5011, msg="地图接口调用失败")
SORT_COLUMN_NOT_EXISTS_ERROR = ErrorBase(code=5012, msg="排序字段不存在或者错误")

# 数据相关
DATA_EXISTS_ERROR = ErrorBase(code=5013, msg="数据已存在,检查主键或唯一键存在")
DATA_NOT_EXISTS_ERROR = ErrorBase(code=5014, msg="数据不存在,检查主键或唯一键是否存在")
