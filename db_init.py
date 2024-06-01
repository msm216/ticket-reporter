import random
import string

from app import create_app, db
from app.models import Task, Ticket, Project
from datetime import datetime, timezone, timedelta


app = create_app()


# 生成特定长度随机字符串
def generate_random_string(length):
    # string.punctuation 特殊字符
    characters = string.ascii_letters + string.digits
    random_string = ''.join(
        random.choice(characters) for i in range(length))
    return random_string

def generate_random_coordinates():
    # 欧洲大陆大致范围的经纬度
    min_latitude = 35.0   # 南部边界：约为地中海区域
    max_latitude = 71.0   # 北部边界：约为北极圈附近
    min_longitude = -10.0  # 西部边界：约为葡萄牙
    max_longitude = 40.0   # 东部边界：约为乌拉尔山脉
    # 生成随机的纬度和经度
    latitude = random.uniform(min_latitude, max_latitude)
    longitude = random.uniform(min_longitude, max_longitude)

    return latitude, longitude


with app.app_context():
    
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