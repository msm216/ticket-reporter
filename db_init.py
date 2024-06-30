import os
import random

from flask import current_app

from app import create_app, db
from app.models import Task, Ticket, Project
from datetime import datetime, timezone, timedelta

from app.utilities import date_to_id, generate_random_coordinates, generate_random_string, generate_random_date


app = create_app()


with app.app_context() as app_ctx:
    
    # 手动创建应用上下文，确保正常使用 Flask 应用的全局变量和扩展
    app_ctx.push()
    print(f"Current app: {current_app.name}")
    

    # 重置数据库
    db.drop_all()
    db.create_all()

    # Create initial projects
    projects = []
    for _ in range(3):
        # 今天减去随机时间差（90天内）
        create_on_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        # 获取随机经纬度
        latitude, longitude = generate_random_coordinates()
        project = Project(
            title=f"Project-{generate_random_string(10)}",
            charger_amount=random.randint(1, 10),
            latitude=latitude,
            longitude=longitude,
            create_on=create_on_date
        )
        project.id = Project.generate_id(create_on_date)
        projects.append(project)
        db.session.add(project)
    db.session.commit()

    # Create initial tickets
    tickets = []
    for _ in range(10):
        # 今天减去随机时间差（60天内）
        report_on_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
        ticket = Ticket(
            title=f"Ticket-{generate_random_string(10)}",
            report_on=report_on_date,
            # 随机绑定 project
            project_id=random.choice(projects).id if random.random() > 0.5 else None,
            description=f"This happend: {generate_random_string(50)}"
        )
        ticket.id = Ticket.generate_id(report_on_date)
        tickets.append(ticket)
        db.session.add(ticket)
    db.session.commit()

    # Create initial tasks
    for _ in range(50):
        # 今天减去随机时间差（30天内）
        execute_on_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
        task = Task(
            execute_on=execute_on_date,
            ticket_id=random.choice(tickets).id,
            description=f"This has been done: {generate_random_string(50)}",
            effort_hour=random.randint(1, 8)
        )
        task.id = Task.generate_id(execute_on_date)
        db.session.add(task)
    db.session.commit()

    # Update update_on for tickets
    for ticket in tickets:
        ticket.update_update_on()
        db.session.add(ticket)
    db.session.commit()

    # 销毁当前的应用上下文
    app_ctx.pop()





if __name__ == '__main__':

    app = create_app()

    with app.app_context():

        # 关闭当前会话
        db.session.remove()



        # 销毁当前的应用上下文
        app_ctx.pop()
    