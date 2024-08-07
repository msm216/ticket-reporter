import sqlite3
import os
import sys
import pandas as pd

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到 sys.path
project_root = 'd:\\Projects\\Py-Projects\\Flask-Projects\\ticket-reporter'
sys.path.append(project_root)

from app import create_app, db
from app.models import *


# 创建 Flask 应用实例
app = create_app()

# 提取数据库路径
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
if db_uri.startswith('sqlite:///'):
    db_path = db_uri[len('sqlite:///'):]
elif db_uri.startswith('sqlite://'):
    db_path = db_uri[len('sqlite://'):]
else:
    raise ValueError("Unsupported database URI scheme")

# 在 Jupyter Notebook 中手动指定路径
db_path = os.path.join(os.getcwd(), 'instance', 'report.db')

# 检查数据库文件是否存在
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found: {db_path}")

# 打印数据库路径以进行调试
print(f"Database path: {db_path}")

def read_table_to_dataframe(table_name, model):
    try:
        query = session.query(model).statement
        df = pd.read_sql(query, session.bind)
        return df
    except Exception as e:
        print(f"Failed to read table {table_name}: {e}")
        return None


# 使用 SQLAlchemy 的连接引擎
engine = create_engine(f'sqlite:///{db_path}', echo=True)

with app.app_context():

    # 测试数据库连接和会话创建
    try:
        # 创建会话
        Session = sessionmaker(bind=engine)
        session = Session()

        # 列出数据库中实际存在的表
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print("Existing tables in the database:")
        print(existing_tables)

        # 使用 pandas 读取 SQL 数据
        model_to_table_map = {
            'client_table': Client,
            'device_table': Device,
            'site_table': Site,
            'ticket_table': Ticket,
            'task_table': Task,
            'issue_table': Issue,
            'resolution_table': Resolution
        }
        # 读取每个表的数据并打印
        for table_name, model in model_to_table_map.items():
            if table_name in existing_tables:
                df = read_table_to_dataframe(table_name, model)
                if df is not None:
                    print(f"{table_name.capitalize()} DataFrame:")
                    print(df.head())
                    print()
            else:
                print(f"Table {table_name} does not exist in the database.")

        # 关闭会话
        session.close()
    except SQLAlchemyError as e:
        print(f"Failed to connect to the database: {e}")