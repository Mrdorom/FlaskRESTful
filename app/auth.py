from flask_restful import reqparse
from functools import wraps

from app.system_config import SysConfig
from app.user.models import User

parser = reqparse.RequestParser()
parser.add_argument('Token', location='headers')

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("===开始校验Token===")
        args = parser.parse_args()
        print("token", args["Token"])
        if not args["Token"]: return SysConfig.ReturnCode("TOKEN_NEED")
        check_user = User.verify_auth_token(args["Token"])
        if type(check_user) == type({}): return check_user
        return func(*args, **kwargs)
    return wrapper