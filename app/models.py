import enum

from datetime import datetime, timezone
from sqlalchemy import event, Enum
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
    abnormality = "abnormality"
    connectivity = "connectivity"
    platform = "platform"

# 事件状态
class Status(enum.Enum):
    analyzing = "analyzing"
    pending = "pending"
    verifying = "verifying"
    closed = "closed"


# 客户
class Client(db.Model):

    __tablename__ = 'client_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    # 反向关联 Site
    resolutions = db.relationship('Site', backref='client_ref', lazy=True)

    def __repr__(self):
        return f'<Client: {self.id}>'


# 站点 --> 客户
class Site(db.Model):

    __tablename__ = 'site_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    # 场站设备数量
    amount = db.Column(db.Integer, default=0, nullable=False)
    # 可调用对象 lambda 确保每次实例化时都会重新获得当前日期时间，而不是服务器启动时的日期时间
    opened_on = db.Column(db.Datetime, default=lambda: datetime.now(timezone.utc).date())
    city = db.Column(db.String(20), default='Test')
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    # 外键指向一个 Client 实例
    owner = db.Column(db.String(20), db.ForeignKey('client_table.id'), default=None)

    def __repr__(self):
        return f'<Site: {self.name}>'


# 事件 <--> 站点
class Issue(db.Model):

    __tablename__ = 'issue_table'

    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(40), nullable=False, unique=True)
    titel_cn = db.Column(db.String(40), nullable=True, unique=True)
    # 外键指向一个 Client 实例
    site_ids = 
    # 可调用对象 lambda 确保每次实例化时都会重新获得当前日期时间，而不是服务器启动时的日期时间
    reported_on = db.Column(db.Datetime, default=lambda: datetime.now(timezone.utc).date())
    category = db.Column(Enum(Category), nullable=True)
    details = db.Column(db.String(80), nullable=False)
    severity = db.Column(Enum(Severity), nullable=True)
    first_resolution_on = db.Column(db.Datetime, nullable=True)
    first_resolution = db.Column(db.String(80), nullable=True)
    last_resolution_on = db.Column(db.Datetime, nullable=True)
    last_resolution = db.Column(db.String(80), nullable=True)
    status = db.Column(Enum(Status), default=Status.analyzing, nullable=False)
    # 反向关联 Resolution，lazy='dynamic' 使得反向关系被访问时返回一个对象而不是列表
    resolutions = db.relationship('Resolution', backref='issue_ref', lazy=True)

    def __repr__(self):
        return f'<Issue: {self.titel}>'


# 解决方案 --> 事件
class Resolution(db.Model):

    __tablename__ = 'user_table'

    id = db.Column(db.String(20), primary_key=True)
    updated_on = db.Column(db.Datetime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = db.Column(db.String(20), db.ForeignKey('issue_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'
    

# 任务单 <--> 事件，任务单 --> 站点
class Ticket(db.Model):

    __tablename__ = 'ticket_table'

    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(40), nullable=False, unique=True)
    # 可调用对象 lambda 确保每次实例化时都会重新获得当前日期时间，而不是服务器启动时的日期时间
    created_on = db.Column(db.Datetime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Site 实例
    site_id = db.Column(db.String(20), db.ForeignKey('site_table.id'), default=None)

    def __repr__(self):
        return f'<Ticket: {self.titel}>'
    

# 工作 --> 任务单
class Task(db.Model):

    __tablename__ = 'task_table'

    id = db.Column(db.String(20), primary_key=True)
    titel = db.Column(db.String(40), nullable=False, unique=True)
    updated_on = db.Column(db.Datetime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = db.Column(db.String(20), db.ForeignKey('ticket_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'