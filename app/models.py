from . import db



class Task(db.Model):
    id = db.Column(db.String, primary_key=True)
    execute_on = db.Column(db.DateTime, nullable=False)
    ticket_id = db.Column(db.String, db.ForeignKey('ticket.id'), nullable=False)
    description = db.Column(db.Text)
    effort_hour = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 构造对象时根据日期生成 id
        if not self.id:
            self.id = self.generate_id(self.execute_on)

    @staticmethod
    def generate_id(execute_on):
        date_str = execute_on.strftime('%Y%m%d')
        like_pattern = f"Task-{date_str}%"
        last_task = Task.query.filter(Task.id.like(like_pattern)).order_by(Task.id.desc()).first()
        if last_task:
            last_id_num = int(last_task.id.split('-')[-1])
            new_id_num = last_id_num + 1
        else:
            new_id_num = 1
        return f"Task-{date_str}-{new_id_num:02d}"


class Ticket(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True)
    report_on = db.Column(db.DateTime, nullable=False)
    project_id = db.Column(db.String, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    update_on = db.Column(db.DateTime)
    # 反向关系
    tasks = db.relationship('Task', backref='ticket', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = self.generate_id(self.report_on)

    @staticmethod
    def generate_id(report_on):
        date_str = report_on.strftime('%Y%m%d')
        like_pattern = f"Ticket-{date_str}%"
        last_ticket = Ticket.query.filter(Ticket.id.like(like_pattern)).order_by(Ticket.id.desc()).first()
        if last_ticket:
            last_id_num = int(last_ticket.id.split('-')[-1])
            new_id_num = last_id_num + 1
        else:
            new_id_num = 1
        return f"Ticket-{date_str}-{new_id_num:02d}"
    
    # 根据最新的task确定更新时间
    def update_update_on(self):
        latest_task = max(self.tasks, key=lambda task: task.execute_on, default=None)
        if latest_task:
            self.update_on = latest_task.execute_on


class Project(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, unique=True)
    create_on = db.Column(db.DateTime)
    charger_amount = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # 反向关系
    tickets = db.relationship('Ticket', backref='project', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = self.generate_id(self.create_on)

    @staticmethod
    def generate_id(create_on):
        date_str = create_on.strftime('%Y%m%d')
        like_pattern = f"Project-{date_str}%"
        last_project = Project.query.filter(Project.id.like(like_pattern)).order_by(Project.id.desc()).first()
        if last_project:
            last_id_num = int(last_project.id.split('-')[-1])
            new_id_num = last_id_num + 1
        else:
            new_id_num = 1
        return f"Project-{date_str}-{new_id_num:02d}"