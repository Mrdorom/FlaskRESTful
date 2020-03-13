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
        user = User.query.first()
        user_schema = UserSchema()
        return user_schema.dump(user)

    def post(self):
        print("开始添加用户")
        parser.add_argument("Password", help="密码")
        args = parser.parse_args()
        if args["UserName"] == None or args["UserName"] == "":
            return SysConfig.ReturnCode("USER_NAME_EMPTY")
        if args["Password"] == None or args["Password"] == "":
            return SysConfig.ReturnCode("USER_PASSWORD_EMPTY")
        check_user = User.query.filter_by(UserName=args["UserName"]).first()
        if check_user:
            return SysConfig.ReturnCode("USER_EXIST")
        check_user = User()
        check_user.UserName = args["UserName"]
        check_user.password = args["Password"]
        db.session.add(check_user)
        db.session.commit()
        return SysConfig.ReturnCode("SIGN_UP_SUCCESS")


class LoginResource(Resource):
    def post(self):
        parser.add_argument("Password", help="用户密码")
        args = parser.parse_args()
        check_user = User.query.filter_by(UserName=args["UserName"]).first()
        if not check_user:
            return SysConfig.ReturnCode("USER_NOT_EXIST")
        if not check_user.verify_password(args["Password"]):
            return SysConfig.ReturnCode("USER_PASSWORD_ERROR")
        token = check_user.generate_auth_token()
        return {"code": 200, "Token": token.decode('ascii'), "UserID": check_user.ID}


class CheckToken(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, *args, **kwargs):
        return {"code": 200, "Status": True}
