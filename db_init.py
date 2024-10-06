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


        # JSON 数据路径
        json_path = os.path.join('data', 'samples', 'sites.json')
        # 读取和解析 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 空列表用于记录创建的实例
        client_inst = []
        device_inst = []
        site_inst = []

        # 创建 Client 实例
        for client_name, sites in data.items():
            # | id | name | (sites) |
            new_client = Client(
                name=client_name
            )
            client_inst.append(new_client)
            db.session.add(new_client)
            try:
                db.session.commit()
                print(f"New client: {new_client} committed")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing {new_client}")

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
                try:
                    db.session.commit()
                    print(f"New site: {new_site} committed")
                except IntegrityError as e:
                    db.session.rollback()
                    print(f"Error '{e}' occurred while committing {new_site}")
                
                # 创建 Device 实例
                for device_id, info in details['devices'].items():
                    # | id | model | install_on | site_id |
                    new_device = Device(
                        id=device_id,
                        model=info['model'],
                        material=info['material'],
                        install_on=datetime.strptime(info['install_on'], '%Y/%m/%d'),
                        site_id=new_site.id
                    )
                    device_inst.append(new_device)
                    db.session.add(new_device)
                    try:
                        db.session.commit()
                        print(f"New device: {new_device} committed")
                    except IntegrityError as e:
                        db.session.rollback()
                        print(f"Error '{e}' occurred while committing {new_device}")
                       
        print(f"\n{len(client_inst)} clients \
                \n{len(site_inst)} sites \
                \n{len(device_inst)} devices \
                \n...added to the database\n")
        
        #############
        # 5 clients
        # 10 sites
        # 25 devices
        #############

        # 空列表用于记录创建的实例
        ticket_inst = []
        task_inst = []

        # 创建10个随机 Ticket
        for i in range(10):
            new_ticket = Ticket(
                id=random_ticket_id(),
                title=random_string(20),
                create_on=random_date(90),
                ticket_type=random.choice(list(Type)),
                description=f"This occured on site: {random_string(40)}",
                status=random.choice(list(Status))
            )
            ticket_inst.append(new_ticket)
            db.session.add(new_ticket)
            try:
                db.session.commit()
                print(f"New ticket: {new_ticket} committed")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing {new_ticket}")

        # 创建15个随机 Task
        for i in range(15):
            # 随机分配给一个 Ticket 实例
            random_ticket = random.choice(ticket_inst)
            new_task = Task(
                execute_on=random_date(60),
                action=random.choice(list(Action)),
                description=f"This action has been taken: {random_string(20)}",
                on_site=random.choice([True, False]),
                result=random.choice(list(Result)),
                ticket_id=random_ticket.id
            )
            task_inst.append(new_task)
            db.session.add(new_task)
            try:
                db.session.commit()
                print(f"New tast: {new_task} committed")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing {new_task}")


        # 空列表用于记录创建的实例
        issue_inst = []
        resolution_inst = []

        # 创建8个随机 Issue
        for i in range(8):
            new_issue = Issue(
                title=random_string(20),
                report_on=random_date(90),
                report_by=random.choice(list(Reporter)),
                category=random.choice(list(Category)),
                description=f"This was the issue: {random_string(40)}",
                severity=random.choice(list(Severity)),
                progress=random.choice(list(Progress)),
            )
            issue_inst.append(new_issue)
            db.session.add(new_issue)
            try:
                db.session.commit()
                print(f"New issue: {new_issue} committed")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing {new_issue}")

        # 创建20个随机 Resolution
        for i in range(20):
            # 随机分配给一个 Ticket 实例
            random_issue = random.choice(issue_inst)
            new_resolution = Resolution(
                update_on=random_date(60),
                description=f"This can solve the issue: {random_string(20)}",
                issue_id=random_issue.id
            )
            resolution_inst.append(new_resolution)
            db.session.add(new_resolution)
            try:
                db.session.commit()
                print(f"New resolution: {new_resolution} committed")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing {new_resolution}")

        print(f"\n{len(ticket_inst)} tickets \
                \n{len(task_inst)} tasks \
                \n{len(issue_inst)} issues \
                \n{len(resolution_inst)} resolutions \
                \n...added to the database\n")
        
        #############
        # 10 tickets
        # 15 tasks
        # 8 issues
        # 20 resolutions
        #############

        # 随机创建多对多关系
        # Ticket <-> Issue
        for ticket in ticket_inst:
            related_issues = random.sample(issue_inst, random.randint(1, 2))
            for issue in related_issues:
                ticket.issues.append(issue)
            try:
                db.session.commit()
                print(f"Ticket {ticket.id} linked to issues: {[issue.id for issue in related_issues]}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing ticket-issue relationships")

        # Ticket <-> Device
        for ticket in ticket_inst:
            related_devices = random.sample(device_inst, random.randint(1, 3))
            for device in related_devices:
                ticket.devices.append(device)
            try:
                db.session.commit()
                print(f"Ticket {ticket.id} linked to devices: {[device.id for device in related_devices]}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error '{e}' occurred while committing ticket-device relationships")