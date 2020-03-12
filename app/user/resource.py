from flask_restful import Resource, reqparse
from app import db
from app.system_config import SysConfig
from app.auth import token_required
from .models import User
from .schema import UserSchema


parser = reqparse.RequestParser()
parser.add_argument("UserName", help="用户名")


class UserResource(Resource):
    def get(self):
        parser.add_argument("ID", help="用户ID")
        args = parser.parse_args()
        print("============", args, args["ID"])
        user = User.query.first()
        user_schema = UserSchema()
        return user_schema.dump(user)

    def post(self):
        return {"test": "User Post success"}


class LoginResource(Resource):
    def post(self):
        parser.add_argument("Password", help="用户密码")
        args = parser.parse_args()
        print("请求的参数", args)
        check_user = User.query.filter_by(UserName=args["UserName"]).first()
        if not check_user:
            return SysConfig.ReturnCode("USER_NOT_EXIST")
        if not check_user.verify_password(args["Password"]):
            return SysConfig.ReturnCode("USER_PASSWORD_ERROR")
        token = check_user.generate_auth_token()
        print("登录成功！放回token等信息", token, type(token))
        return {"code": 200, "Token": token.decode('ascii'), "UserID": check_user.ID}


class CheckToken(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, *args, **kwargs):
        print("校验token通过")
        return {"code": 200, "Status": True}
