class SysConfig():
    RETURNCODE = {
        "SIGN_UP_SUCCESS": {"code": 200, "message": "注册成功！"},
        "CHANGE_SUCCESS": {"code": 200, "message": "修改成功！"},
        "DELETE_SUCCESS": {"code": 200, "message": "删除成功！"},
        "USER_NOT_EXIST": {"code": 204, "message": "该用户不存在！"},
        "USER_EXIST": {"code": 204, "message": "该用户已存在！"},
        "USER_PASSWORD_ERROR": {"code": 204, "message": "用户密码错误！"},
        "USER_NAME_EMPTY": {"code": 204, "message": "用户名不可为空！"},
        "USER_PASSWORD_EMPTY": {"code": 204, "message": "用户密码不可为空！"},
        "ARTICLE_NOT_EXIST": {"code": 204, "message": "该文章不存在！"},
        "TOKEN_ERROR": {"code": 2000, "message": "TOKEN不正确！"},
        "TOKEN_EXPIRED": {"code": 2001, "message": "TOKEN过期！"},
        "TOKEN_NEED": {"code": 2002, "message": "请携带Token进行访问！"}
    }
    SECRETKEY = "awdJKawd12121"

    @staticmethod
    def ReturnCode(status):
        return SysConfig.RETURNCODE.get(status, {"code": 404, "message": "该状态不存在！"})

    @staticmethod
    def SecretKey():
        return SysConfig.SECRETKEY
