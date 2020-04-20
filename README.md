# 这是一个符合RESTful规范的Flask的项目(可打包成docker的image)
**适用对象：稍微了解docker，刚刚接触RestFul规范，好奇如何使用docker打包web项目的同学们**

**该项目默认使用了mysql的容器，如不需要使用下面有教程**

这个项目使用了`Flask+Sqlalchemy+flask_restful+flask_marshmallow`来构建基础项目，

> 其中后端的mysql是使用了docker的image创建的NAME为flask-mysql的容器（这也是为什么我配置里面localhost是flask-mysql的原因，因为把我该项目和mysql的容器放到了一个network里面，所以可以识别mysql的container的name）

还有一点，本来项目里整合了celery，但是发现不知道怎么在一个容器里面运行两种项目（flask项目和celery项目），于是决定把celery的项目也打包成docker的image(其实这有一个问题，celery的项目我想用flask项目里面的model和mysql连接的，当是分开后我只能二者都设置成一样先，后面看看有没有办法解决这个问题，或者有大神知道解决方法可以在issue里面提出帮助一下我谢谢！)
# 项目结构

```
├── app
│   ├── article
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── resource.py
│   │   └── schema.py
│   ├── auth.py
│   ├── gbcomment
│   │   ├── __init__.py
│   │   └── resource.py
│   ├── __init__.py
│   ├── new
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── resource.py
│   │   └── schema.py
│   ├── system_config.py
│   └── user
│       ├── __init__.py
│       ├── models.py
│       ├── resource.py
│       └── schema.py
├── dockerfile
├── manager.py
├── README.md
└── requirement.txt

```

下面稍微介绍一下（由于在测试阶段，所以里面可以看到有一些没用print函数）

## requirement.txt

需要安装的包

## manager.py

用manage管理的Flask项目

## app文件

整个app就是我们最重要的内容了

> `auth.py`:这个是用于验证Token的
>
> `__init__.py`:这个里面是项目的主要配置
>
> `system_config.py`:这个里面是通用的一些提示啥的
>
> user用户模块文件夹
>
> >`__init__.py`:用户的蓝图声明
> >
> >`models.py`:用户模型
> >
> >`resource.py`:RESTful规范接口写在这里面
> >
> >`schema.py`: 把模型映射成Json格式的文件 
>
> article文章模块文件夹：与user用户模块相同不进行介绍

## 认证机制

认证机制使用Token，用户登录后获得一个临时的Token，每次请求通过这个Token进行认证。至于怎么保存啥的是前端的事情这里不管。

搭配前端项目可以完整的运行起来
前端项目是：Vue.js开发的，通过Vue-cli脚手架进行创建项目，前端模板使用了BootstrapVue框架。地址在[这里](https://github.com/WRAllen/MyVue)


PS：要稍微了解Flask的同学会容易看懂，对Flask不熟悉的同学建议先看一下Flask的官网教程。暂时没有把这个项目传到docker hub(还在优化，传太浪费时间)，如果想看效果可以通过dockerfile打包成image来运行，直接运行的话记得把mysql的连接地址改成你的数据库ip地址，例如flask-mysql改成localhost。


# 如果你用docker下面是使用教程
## 在项目根目录打包成image
打包时间有点久，可以先开始创建桥接网络(包含)后面的教程
```shell
# docker build -t image的名字/tag 具体需要被打包成iamge的位置
# 下面就是把当前文件夹FlaskRestful下的内容打包成flask_restful/1.0
[root@XXX FlaskRestful]# docker build -t flask_restful/1.0 ./
巴拉巴拉一堆东西，最后看到下面
Successfully built 847928942db6
Successfully tagged flask_restful/1.0:latest
```
## 查看生成的image
```shell
[root@iZbp117p51ll3pasv31s6fZ FlaskRestful]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
flask_restful/1.0   latest              847928942db6        About a minute ago   1.02GB
```

## 创建桥接网络
目的是使mysql和flask项目在一个网络下
```shell
docker network create 网络名称
[root@XXX ~]# docker network create flask_network
191b267bd27356f06c69e48046d552e301a1c8d5ff19886bcda90eced6266d0f
```

## 获取mysql的image
```shell
[root@iZbp117p51ll3pasv31s6fZ ~]# docker pull mysql
Using default tag: latest
latest: Pulling from library/mysql
巴拉巴拉一堆东西，最后看到下面
1811572b5ea5: Pull complete 
Digest: sha256:b69d0b62d02ee1eba8c7aeb32eba1bb678b6cfa4ccfb211a5d7931c7755dc4a8
Status: Downloaded newer image for mysql:latest
docker.io/library/mysql:latest
```
## mysql的image创建相关container并且连接到network
```shell
docker run --network 刚刚创建的network --name mysql容器的名称 -p 物理机端口:3306 -e MYSQL_ROOT_PASSWORD=你的数据库密码 -d mysql:latest
[root@iZbp117p51ll3pasv31s6fZ FlaskRestful]# docker run --network flask_network --name flask-mysql -p 4306:3306 -e MYSQL_ROOT_PASSWORD=XXXX -d mysql:latest
c869affa8013c7b8aceeee972423dd420707908c12b8c82ebe1bb0f220e65eef
```
## 查看network当前的连接情况
```shell
巴拉巴拉
"Containers": {
  "d3d55d3ed501def858d36843c9db41195d82c5b214e3184d2db5daefe53224c4": {
      "Name": "flask-mysql",
      "EndpointID": "50ae10c43c32190b73703b30d6bb08015b0bf28b2cd4f7dfb4dfc006bd51df8b",
      "MacAddress": "02:42:ac:15:00:02",
      "IPv4Address": "172.21.0.2/16",
      "IPv6Address": ""
  }
},
巴拉巴拉
```
可以发现flask-mysql连接上了
## 运行flask的image生成container-临时用于测试
这个时候差不多也打包好了， 这里的--rm退出后就会删除该容器用于测试 -it用于显示交互式查看是否成功
现在用这个临时的容器看一下是否正常连接network
```shell
docker run --name 容器名称 -it --rm --network flask_network -p 8888:8888 flask_restful/1.0 python manager.py shell
```

## 查看network的情况
```shell
docker network ls
docker network inspect flask_network
"Containers": {
  "3b868d46dc9f7f9f663f8381d6bfb7da42bb6b691fdc9b094b4ea7746fe39408": {
      "Name": "flask_app",
      "EndpointID": "ea5ce2a56101a2f7319085589f47a2450796fbc3b1bd2d03f47f0f147355e8e6",
      "MacAddress": "02:42:ac:15:00:03",
      "IPv4Address": "172.21.0.3/16",
      "IPv6Address": ""
  },
  "d3d55d3ed501def858d36843c9db41195d82c5b214e3184d2db5daefe53224c4": {
      "Name": "flask-mysql",
      "EndpointID": "50ae10c43c32190b73703b30d6bb08015b0bf28b2cd4f7dfb4dfc006bd51df8b",
      "MacAddress": "02:42:ac:15:00:02",
      "IPv4Address": "172.21.0.2/16",
      "IPv6Address": ""
  }
},
```
可以发现都连上了
## 然后进入mysql的容器创建对应的数据库
```shell
[root@iZbp117p51ll3pasv31s6fZ ~]# docker exec -it flask-mysql bash
root@0f7e82571cd9:/# mysql -u root -pAliCentOSMysql123456
# 进入之后
mysql> create schema `FlaskRESTFul` default character set utf8 ;
Query OK, 1 row affected, 1 warning (0.02 sec)
```
## 然后再次用临时的flask容器创建表
```shell
docker run --name flask_app -it --rm --network flask_network -p 8888:8888 flask_restful/1.0 python manager.py shell
[root@iZbp117p51ll3pasv31s6fZ FlaskRestful]# docker run --name flask_app -it --rm --network flask_network -p 5000:8888 flask_restful/1.0 python manager.py shell
/usr/local/lib/python3.6/site-packages/flask_marshmallow/__init__.py:27: UserWarning: Flask-SQLAlchemy integration requires marshmallow-sqlalchemy to be installed.
  "Flask-SQLAlchemy integration requires "
>>> db
<SQLAlchemy engine=mysql+pymysql://root:***@flask-mysql:3306/FlaskRESTFul?charset=utf8>
>>> db.create_all()
/usr/local/lib/python3.6/site-packages/pymysql/cursors.py:170: Warning: (3719, "'utf8' is currently an alias for the character set UTF8MB3, but will be an alias for UTF8MB4 in a future release. Please consider using UTF8MB4 in order to be unambiguous.")
  result = self._query(query)
>>> 
```
这样表也创建好了
## 创建永久的flask容器
下面是正常的语句
```shell
docker run --name flask_app --network flask_network -p 5000:8888 flask_restful/1.0
```
## 查看docker容器的情况
```shell
docker ps
可以发现二者都在运行，这样就搞定了
如果退出后发现容器没有在运行直接
docker start flask_app 即可
```

# 如果你用venv这种方式下面是使用教程

## 安装需要环境(前提是已经在虚拟环境下了)

环境需求在`requirement.txt` 安装的方法很简单（推荐在虚拟环境下）

```shell
pip install -r requirement.txt
```

## 配置mysql
当然你的电脑或者服务器必须有Mysql，对于Mysql的安装这里不介绍。
修改`app/__init__.py`
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:你的mysql密码@mysql的ip地址:端口号/数据库名称'
```
这里的数据库要记得去创建，如果以及有了记得数据库里面表的名字是否和该项目重复(因为重复sqlalchemy创建表是会默认跳过的)

## 创建表

首先进入你的虚拟环境，通过下面的代码进行创建表

```shell
项目根文件夹下：python manager.py shell
>>> db.create_all()
```

这样基础表就建立好了



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
