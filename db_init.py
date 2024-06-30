import os
import random
from datetime import datetime, timezone, timedelta

from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import *
from app.utilities import *

#from config import Config


# 一些数据实例信息
clients = {
    'EVN': {}, 
    'Energie360': {}, 
    'Transtema': {}
}


if __name__ == '__main__':

    app = create_app()

    with app.app_context():

        # 关闭当前会话
        db.session.remove()
        # 'instance\\report.db'
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        # 删除db文件
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f'Database file removed: {db_path}')
        else:
            print(f'Database file {db_path} not found.')
        # 删除表格
        db.drop_all()
        print("Tables dropped.")
        # 创建表格
        db.create_all()
        print("Tables created.")
      

        # 记录 Client 实例用于随机分配给 Site 实例
        client_instances = []
        # 创建 Client 实例
        for key, value in clients.items():
            new_client = Client(name=key)
            client_instances.append(new_client)
            db.session.add(new_client)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing clients: {e}")


        # 记录 Site 实例用于随机分配给 Ticket 实例
        site_instances = []
        # 创建 Site 实例
        for i in range(10):
            random_client = random.choice(client_instances)
            random_city = f'City_{i}'
            lati, long = generate_random_coordinates()
            new_site = Site(
                owner=random_client.id,
                city=random_city,
                name=f'{random_client.name}-{random_city}',
                opened_on = generate_random_date(90, 120),
                amount=random.randint(1, 20),
                latitude=lati,
                longitude=long,
            )
            site_instances.append(new_site)
            db.session.add(new_site)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing site: {e}")


        # 记录 Issue 实例用于随机分配给 Update，Ticket 实例
        issue_instances = []
        # 创建 Issue 实例
        for i in range(15):
            new_issue = Issue(
                title=f'Issue_{i}',
                title_cn=f'问题_{i}',
                reported_on=generate_random_date(90),
                category=random.choice(list(Category)),
                details=f"It was the case that: {generate_random_string(40)}",
                severity=random.choice(list(Severity)),
            )
            site_instances.append(new_issue)
            db.session.add(new_issue)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing issue: {e}")


        # 记录 Ticket 实例用于随机分配给 Task 实例
        ticket_instances = []
        # 创建 Ticket 实例，并关联到 Site 和 Issue
        for i in range(20):
            random_id_head = random.choices(string.ascii_uppercase, k=2)
            random_site = random.choice(site_instances)
            ticket = Ticket(
                id=f"{random_id_head}{generate_random_string(10)}",
                title=f'{random_site.name}-Ticket_{i}',
                created_on=generate_random_date(90),
                details=f"It was reported that: {generate_random_string(40)}",
                site_id=random_site.id
            )
            ticket_instances.append(ticket)
            db.session.add(ticket)
            # 随机关联 Issue
            related_issues = random.sample(issue_instances, random.randint(1, 3))
            for issue in related_issues:
                ticket.issues.append(issue)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing ticket: {e}")


        # 创建 Task 实例
        for i in range(60):
            random_ticket = random.choice(ticket_instances)
            new_task = Task(
                title=f'Task_{i}',
                executed_on=generate_random_date(90),
                details=f'We did {generate_random_string(40)}',
                issue_id=random_ticket.id
            )
            db.session.add(new_task)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing task: {e}")


         # 创建 Resolution 实例
        for i in range(60):
            random_issue = random.choice(issue_instances)
            new_resolution = Resolution(
                updated_on=generate_random_date(90),
                details=f'We can do this: {generate_random_string(40)}',
                issue_id=random_ticket.id
            )
            db.session.add(new_resolution)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing resolution: {e}")