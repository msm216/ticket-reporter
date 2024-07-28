import os
import random
import json

from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import *
from app.utilities import *

#from config import Config


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
        # 重新创建表格
        db.drop_all()
        print("Tables dropped.")
        db.create_all()
        print("Tables created.")


        # 空列表用于记录创建的实例
        client_inst = []
        device_inst = []
        site_inst = []
        ticket_inst = []
        task_inst = []
        issue_inst = []
        resolution_inst = []

        # JSON 数据路径
        json_path = os.path.join('data', 'samples', 'sites.json')
        # 读取和解析 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # 创建 Client 实例
        for client_name, sites in data.items():
            # | id | name | (sites) |
            new_client = Client(
                name=client_name
            )
            client_inst.append(new_client)
            db.session.add(new_client)
            db.session.commit()
            print(f"New client: {new_client} committed")
            # 创建 Site 实例
            for site_name, details in sites.items():
                # | id | name | address | zip | latitude | longitude | owner_id | (devices) | (tickets) |
                new_site = Site(
                    name=site_name,
                    address=details['address'],
                    zip_code=details['zip'],
                    country=details['country'],
                    latitude=details['latitude'],
                    longitude=details['longitude'],
                    owner_id=new_client.id
                )
                site_inst.append(new_site)
                db.session.add(new_site)
                db.session.commit()
                print(f"New site: {new_site} committed")
                # 创建 Site 实例
                for device_sn, info in details['devices'].items():
                    # | sn | model | install_on | site_id |
                    new_device = Device(
                        sn=device_sn,
                        model=info['model'],
                        material=info['material'],
                        install_on=datetime.strptime(info['install_on'], '%Y/%m/%d'),
                        site_id=new_site.id
                    )
                    device_inst.append(new_device)
                    db.session.add(new_device)
                    db.session.commit()
                    print(f"New device: {new_device} committed")
        
        print(f"Committed:\n{len(client_inst)} clients\n{len(site_inst)} sites\n{len(device_inst)} devices to the database.")




        '''


        # 创建 Client 实例
        # | id | name | (sites) |
        # Client <-- Site
        for i in range(5):
            new_client = Site(
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


        # 创建 Client 实例
        for name, _ in clients.items():
            new_client = Client(name=name)
            client_instances.append(new_client)
            db.session.add(new_client)
        try:
            # 提交组实例到数据库
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while committing clients: {e}")


        # | id | name | amount | open_on | city | latitude | longitude | owner_id | (tickets) |
        # Site --> Client
        # Site <-- Ticket
 
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
        '''