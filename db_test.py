import pandas as pd

from app import create_app, db
from app.models import Task, Ticket, Project

####################################################

# 通过 __init__.py 中的 create_app() 函数创建app
app = create_app()
# sqlite:///d:\\Projects\\Py-Projects\\ticket-reporter\\data\\sqlite\\app.db
db_path = app.config['SQLALCHEMY_DATABASE_URI']
print(db_path)

with app.app_context():

    # 读取表格内容为 list，其中的元素都为各自对应模型的实例
    tasks_list = Task.query.all()
    tickets_list = Ticket.query.all()
    projects_list = Project.query.all()

    # 读取表格内容为 DataFrame
    tasks_df = pd.read_sql(Task.query.statement, db.session.bind)
    tickets_df = pd.read_sql(Ticket.query.statement, db.session.bind)
    projects_df = pd.read_sql(Project.query.statement, db.session.bind)