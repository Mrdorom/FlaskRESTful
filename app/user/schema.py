from app import ma


class UserSchema(ma.Schema):
    # 需要返回的模型对应得列
    class Meta:
        fields = ("ID", "UserName", "NickName")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
