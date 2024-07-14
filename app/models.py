import enum

from datetime import datetime, timezone
from sqlalchemy import event, Enum, Table, Column, Integer, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .utilities import *



# 严重程度
class Severity(enum.Enum):
    vital = "vital"
    critical = "critical"
    grave = "grave"
    normal = "normal"
    minor = "minor"

# 事件分类
class Category(enum.Enum):
    feature = "feature"
    quality = "quality"
    abnormality = "firmware"
    connectivity = "connectivity"
    platform = "platform"

# 事件状态
class Status(enum.Enum):
    analyzing = "analyzing"
    pending = "pending"
    verifying = "verifying"
    closed = "closed"

# Ticket <--> Issue 关联表
ticket_issue_association = Table('ticket_issue', db.Model.metadata,
    Column('ticket_id', Integer, ForeignKey('ticket_table.id')),
    Column('issue_id', Integer, ForeignKey('issue_table.id'))
)


# | id | name |
# Client <-- Site
class Client(db.Model):

    __tablename__ = 'client_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    # 反向关联 Site
    sites = db.relationship('Site', backref='client_ref', lazy=True)

    def __repr__(self):
        return f'<Client: {self.id}>'


# | id | name | amount | open_on | city | latitude | longitude | owner |
# Site --> Client
# Site <-- Ticket
class Site(db.Model):

    __tablename__ = 'site_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    # 场站设备数量
    amount = db.Column(db.Integer, default=0, nullable=False)
    open_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    city = db.Column(db.String(20), default='Test')
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    # 外键指向一个 Client 实例
    owner = db.Column(db.String(20), db.ForeignKey('client_table.id'), default=None)
    # 反向关联 Ticket
    tickets = db.relationship('Ticket', backref='site_ref', lazy=True)

    def __repr__(self):
        return f'<Site: {self.name}>'


# | id | title | title_cn | report_on | category | latitude | longitude | owner |
# Issue <-- Resolution
# Issue <-> Ticket
class Issue(db.Model):

    __tablename__ = 'issue_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    title_cn = db.Column(db.String(40), nullable=True, unique=True)
    report_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    category = db.Column(Enum(Category), nullable=True)
    details = db.Column(db.String(80), nullable=False)
    severity = db.Column(Enum(Severity), nullable=True)
    first_resolution_on = db.Column(db.DateTime, nullable=True)
    first_resolution = db.Column(db.String(80), nullable=True)
    last_resolution_on = db.Column(db.DateTime, nullable=True)
    final_resolution = db.Column(db.String(80), nullable=True)
    status = db.Column(Enum(Status), default=Status.analyzing, nullable=False)
    # 反向关联 Resolution，lazy='dynamic' 使得反向关系被访问时返回一个对象而不是列表
    resolutions = db.relationship('Resolution', backref='issue_ref', lazy=True)
    # 与 Ticket 的多对多关系
    tickets = db.relationship('Ticket', secondary=ticket_issue_association, back_populates='issues')

    def __repr__(self):
        return f'<Issue: {self.title}>'


# Resolution --> Issue
class Resolution(db.Model):

    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    updated_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = db.Column(db.String(20), db.ForeignKey('issue_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'
    

# Ticket --> Site
# Ticket <-> Issue
class Ticket(db.Model):

    __tablename__ = 'ticket_table'

    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    # 可调用对象 lambda 确保每次实例化时都会重新获得当前日期时间，而不是服务器启动时的日期时间
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Site 实例
    site_id = db.Column(db.String(20), db.ForeignKey('site_table.id'), default=None)
    # 与 Issue 的多对多关系
    issues = db.relationship('Issue', secondary=ticket_issue_association, back_populates='tickets')

    def __repr__(self):
        return f'<Ticket: {self.title}>'


# Task --> Ticket
class Task(db.Model):

    __tablename__ = 'task_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    executed_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = db.Column(db.String(20), db.ForeignKey('ticket_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'