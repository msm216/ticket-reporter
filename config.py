import os


# d:\Projects\Py-Projects\ticket-reporter
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'HardToGuessStringAsDefaulKey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'report.db')
    # 追踪每个对象的变化并发出相应的信号，影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 不在每次请求结束后都自动提交数据库的变动 db.session.commit()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

