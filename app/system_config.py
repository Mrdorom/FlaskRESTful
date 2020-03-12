class SysConfig():
    RETURNCODE = {
        "USER_NOT_EXIST": {"code": 204, "message":"该用户不存在！"},
        "USER_PASSWORD_ERROR": {"code":204, "message":"用户密码错误！"},
        "TOKEN_ERROR": {"code":2000, "message":"TOKEN不正确！"},
        "TOKEN_EXPIRED": {"code":2001, "message":"TOKEN过期！"},
        "TOKEN_NEED": {"code":2002, "message":"请携带Token进行访问！"}
    }
    SECRETKEY = "awdJKawd12121"

    @staticmethod
    def ReturnCode(status):
        return SysConfig.RETURNCODE.get(status, {"code": 404, "message": "该状态不存在！"})
    
    @staticmethod
    def SecretKey():
        return SysConfig.SECRETKEY