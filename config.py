import os


# d:\Projects\Py-Projects\ticket-reporter
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BASE_DIR, 'app', 'data', 'sqlite', 'report.db')
    # 追踪每个对象的变化并发出相应的信号，影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 不在每次请求结束后都自动提交数据库的变动 db.session.commit()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SECRET_KEY = 'HardToGuessStringAsDefaulKey'

