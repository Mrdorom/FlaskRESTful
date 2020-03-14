from app import ma


class ArticleSchema(ma.Schema):
    # 需要返回的模型对应得列
    class Meta:
        fields = ("ID", "Title", "Text", "UserID")


user_schema = ArticleSchema()
users_schema = ArticleSchema(many=True)
