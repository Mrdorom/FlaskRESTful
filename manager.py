from flask_script import Manager, Shell
from app import create_app, db

app = create_app()
manager = Manager(app)

# Shell模式下无需导入可执行的对象，属性与方法


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
