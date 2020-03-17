from celery import Celery
from celery.schedules import crontab

from app import create_app
from app import db
from app.user.models import User


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL']
    )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


app = create_app()
celery = make_celery(app)


@celery.task
def test():
    check_user = db.session.query(User).first()
    print(f"--{check_user}--用户名:{check_user.UserName}")
    return "这是测试的task!!!"


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), test.s(), name="测试")
