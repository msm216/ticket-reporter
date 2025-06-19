import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 配置日志级别
logging.getLogger('weasyprint').setLevel(logging.ERROR)  # 设置 WeasyPrint 日志级别
logging.getLogger('fontTools').setLevel(logging.ERROR)   # 设置 fontTools 日志级别

# 初始化数据库
db = SQLAlchemy()

def create_app(test_config=None):
    # 创建并配置app
    app = Flask(__name__, instance_relative_config=True)
    
    # 设置默认配置
    app.config.from_object(Config)

    # 添加额外的配置以减少警告
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # 如果提供了测试配置，则覆盖默认配置
    if test_config is not None:
        app.config.update(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    from app.views import bp
    app.register_blueprint(bp)

    return app