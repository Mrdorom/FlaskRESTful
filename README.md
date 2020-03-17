# 这是一个符合RESTful规范的Flask项目

刚刚开始学习前后端分离的开发模式，鉴于之前没有经验，特地用这个项目来锻炼一下自己，里面的代码可能不规范，希望大神们看到后及时提出这样我好改正，这个项目的目的就是为了学习，并且希望也能帮助到其他正在使用Flask构建RESTful规范后端的同学。

这个项目使用了`Flask+Sqlalchemy+flask_restful+flask_marshmallow+Celery+Mysql`来构建项目，后面可能会加上`scrapy`，但是现在暂时不使用。

认证机制使用Token，用户登录后获得一个临时的Token，每次请求通过这个Token进行认证。至于怎么保存啥的是前端要管的，后面我也把vue的前端学习项目也传到github



前端项目是：Vue.js开发的，通过Vue-cli脚手架进行创建项目，前端模板使用了BootstrapVue框架。地址在[这里](https://github.com/WRAllen/MyVue)



PS：要稍微了解Flask的同学会容易看懂，对Flask不熟悉的同学建议先看一下Flask的官网教程，当前Celery只是通过了测试可以和sqlalchemy一起结合使用，后期打算加上scrapy框架通过Celery来执行(后期要使用这个Celery还要结合supervisor)

# 需要环境

环境需求在`requirement.txt` 安装的方法很简单（推荐在虚拟环境下）

```shell
pip install -r requirement.txt
```

当然你的电脑或者服务器必须有Mysql，对于Mysql的安装这里不介绍。

由于Celery的使用要依赖Redis，这里也默认安装了Redis(没有使用RabbitMQ,broker和backend都使用了Redis)

# 修改配置

**记得把项目里面的Mysql配置啥的改成自己的，配置在`app/__init__.py`里面**

并且根据你的配置去把数据库建立起来，这里也不介绍了

# 如何使用

## 创建表

首先进入你的虚拟环境，通过下面的代码进行创建表

```shell
项目根文件夹下：python manager.py shell
>>> db.create_all()
```

这样两个基础表就建立好了，一个是user一个是article



## 运行项目

```shell
项目根文件夹下：python manager.py runserver --host 0.0.0.0 --port 5000
```

如果是阿里的服务器记得把对应的端口打开（5000添加到安全组的入站规则），这里也不做介绍

运行有如下的输出就是正常的

```shell
(venv) [root@iZbp117p51ll3pasv31s6fZ FlaskRestful]# python manager.py runserver --host 0.0.0.0 --port 5000
/home/work/FlaskRestful/venv/lib/python3.8/site-packages/flask_marshmallow/__init__.py:26: UserWarning: Flask-SQLAlchemy integration requires marshmallow-sqlalchemy to be installed.
  warnings.warn(
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## 后面就可以用Postman进行测试了

话说Postman是真的好用O(∩_∩)O

## 注册用户

用户通过ip+/user的POST请求添加用户

```json
{
	"UserName": "allen",
	"Password": "123"
}
```

返回结果

```json
{
    "code": 200,
    "message": "注册成功！"
}
```

# 项目结构

```
├── app
│   ├── article
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── resource.py
│   │   └── schema.py
│   ├── auth.py
│   ├── __init__.py
│   ├── system_config.py
│   └── user
│       ├── __init__.py
│       ├── models.py
│       ├── resource.py
│       └── schema.py
├── celery_task ------这个是celery的独立文件夹-后期要加上scrapy
│   └── __init__.py---当前celery的配置也写在这里
├── manager.py
└── requirement.txt

```

下面稍微介绍一下（由于在测试阶段，所以里面可以看到有一些没用print函数）

## requirement.txt

需要安装的包

## manager.py

用manage管理的Flask项目

## app文件

整个app就是我们最重要的内容了

> auth.py:这个是用于验证Token的
>
> `__init__.py`:这个里面是项目的主要配置
>
> system_config.py:这个里面是通用的一些提示啥的
>
> user用户模块文件夹
>
> >`__init__.py`:用户的蓝图声明
> >
> >models.py:用户模型
> >
> >resource.py:RESTful规范接口写在这里面
> >
> >schema.py: 把模型映射成Json格式的文件 
>
> article文章模块文件夹：与user用户模块相同不进行介绍

## celery_task文件

里面的`__init__.py`写了主要的Celery的配置和任务，不过暂时Celery没有实质性的使用，只是通过了测试可以和sqlalchemy一起使用了，后期要使用这个Celery还要结合supervisor