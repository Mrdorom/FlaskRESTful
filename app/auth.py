from flask_restful import reqparse
from functools import wraps

from app.system_config import SysConfig
from app.user.models import User

parser = reqparse.RequestParser()


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser.add_argument('Token', location='headers')
        args = parser.parse_args()
        print("token认证：", {args["Token"]})
        if not args["Token"]:
            return SysConfig.ReturnCode("TOKEN_NEED")
        check_user = User.verify_auth_token(args["Token"])
        if type(check_user) == type({}):
            return check_user
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser.add_argument('UserID', location='headers')
        args = parser.parse_args()
        print("UserID认证：", {args["UserID"]})
        if not args["UserID"]:
            return SysConfig.ReturnCode("USERID_NEED")
        check_user = User.query.get(args["UserID"])
        if not check_user:
            return SysConfig.ReturnCode("USER_NOT_EXIST")
        if check_user.RoleID != 1:
            return SysConfig.ReturnCode("USER_NOT_PERMISSION")
        return func(*args, **kwargs)
    return wrapper
