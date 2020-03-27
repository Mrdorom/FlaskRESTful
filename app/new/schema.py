from app import ma


class NewSchema(ma.Schema):
    # 需要返回的模型对应得列
    class Meta:
        fields = ("ID", "Title", "Url")


new_schema = NewSchema()
news_schema = NewSchema(many=True)
