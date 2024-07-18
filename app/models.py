import enum

from datetime import datetime, timezone
from sqlalchemy import event, Enum, Table, Column, Integer, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .utilities import *



# Model of Device
class Model(enum.Enum):
    IDC30 = "IDC30"
    IDC180 = "IDC180"
    IDC480 = "IDC480"

# Severity of Issue
class Severity(enum.Enum):
    vital = "vital"
    critical = "critical"
    grave = "grave"
    normal = "normal"
    minor = "minor"

# Category of Issue
class Category(enum.Enum):
    rnd = "R&D"
    quality = "quality"
    connectivity = "connectivity"
    platform = "platform"

# Progress of Issue
class Progress(enum.Enum):
    analyzing = "analyzing"
    pending = "pending"
    verify = "verify"
    closed = "closed"

# Type of Ticket
class Type(enum.Enum):
    abnormal = "abnormal"
    commission = "commission"
    connectivity = "connectivity"
    platform = "platform"

# Status of Ticket
class Status(enum.Enum):
    open = "open"
    processing = "processing"
    closed = "closed"

# Action taken in Task
class Action(enum.Enum):
    consult = "consult"
    remote_debug = "remote_debug"
    onsite_debug = "onsite_debug"
    inhouse_repair = "inhouse_repair"
    onsite_repair = "onsite_repair"
    spare_delivery = "spare_delivery"
    callback = "callback"

# Result of Task
class Result(enum.Enum):
    observation = "observation"
    solved = "solved"
    failed = "failed"


# Ticket <--> Issue 关联表
ticket_issue_association = Table('ticket_issue', db.Model.metadata,
    Column('ticket_id', Integer, ForeignKey('ticket_table.id')),
    Column('issue_id', Integer, ForeignKey('issue_table.id'))
)

# Ticket <--> Device 关联表
ticket_device_association = Table('ticket_device', db.Model.metadata,
    Column('ticket_id', Integer, ForeignKey('ticket_table.id')),
    Column('device_id', Integer, ForeignKey('device_table.id'))
)


# | id | name | (sites) |
# Client <-- Site
class Client(db.Model):

    __tablename__ = 'client_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    # 反向关联 Site
    sites = db.relationship('Site', backref='client_ref', lazy=True)

    def __repr__(self):
        return f'<Client: {self.id}>'


# | id | model | install_on | site_id |
# Device --> Site
# Device <-> Ticket
class Device(db.Model):

    __tablename__ = 'divice_table'

    sn = db.Column(db.String(20), primary_key=True)
    model = db.Column(Enum(Model), nullable=True)
    install_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    # 外键指向一个 Client 实例
    site_id = db.Column(db.String(20), db.ForeignKey('site_table.id'), default=None)
    # 与 Ticket 的多对多关系
    tickets = db.relationship('Ticket', secondary=ticket_device_association, back_populates='devices')

    def __repr__(self):
        return f'<Site: {self.name}>'
    

# | id | name | address | zip | latitude | longitude | owner_id | (devices) | (tickets) |
# Site --> Client
# Site <-- Ticket
# Site <-- Device
class Site(db.Model):

    __tablename__ = 'site_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    address = db.Column(db.String(30), nullable=True)
    zip = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    # 外键指向一个 Client 实例
    owner_id = db.Column(db.String(20), db.ForeignKey('client_table.id'), default=None)
    # 反向关联 Device
    devices = db.relationship('Device', backref='site_ref', lazy=True)
    # 反向关联 Ticket
    tickets = db.relationship('Ticket', backref='site_ref', lazy=True)

    def __repr__(self):
        return f'<Site: {self.name}>'


# | id | title | title_cn | creat_on | type | details | status | first_response | first_response_on |
# | final_resolution | close_on | (issues) |
# Ticket --> Site
# Ticket <-> Issue
class Ticket(db.Model):

    __tablename__ = 'ticket_table'

    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    title_cn = db.Column(db.String(40), nullable=False, unique=True)
    creat_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    # 外键指向一个 Site 实例
    site_id = db.Column(db.String(20), db.ForeignKey('site_table.id'), default=None)
    type = db.Column(Enum(Type), nullable=True)
    details = db.Column(db.String(80), nullable=False)
    status = db.Column(Enum(Status), default=Status.open, nullable=False)
    first_response = db.Column(db.String(80), nullable=True)
    first_response_on = db.Column(db.DateTime, nullable=True)
    final_resolution = db.Column(db.String(80), nullable=True)
    close_on = db.Column(db.DateTime, nullable=True)
    # 与 Issue 的多对多关系
    issues = db.relationship('Issue', secondary=ticket_issue_association, back_populates='tickets')

    def __repr__(self):
        return f'<Ticket: {self.title}>'


# | id | execute_on | action | detail | result | first_response | ticket_id |
# Task --> Ticket
class Task(db.Model):

    __tablename__ = 'task_table'

    id = db.Column(db.Integer, primary_key=True)
    execute_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    action = db.Column(Enum(Action), nullable=True)
    detail = db.Column(db.String(80), nullable=False)
    result = db.Column(Enum(Result), nullable=True)
    # 外键指向一个 Ticket 实例
    ticket_id = db.Column(db.String(20), db.ForeignKey('ticket_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'
    

# | id | title | title_cn | report_on | category | details | severity | progress |
# | final_resolution | close_on | (resolutions) | (tickets) |
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
    progress = db.Column(Enum(Progress), default=Progress.analyzing, nullable=False)
    final_resolution = db.Column(db.String(80), nullable=True)
    close_on = db.Column(db.DateTime, nullable=True)
    # 反向关联 Resolution，lazy='dynamic' 使得反向关系被访问时返回一个对象而不是列表
    resolutions = db.relationship('Resolution', backref='issue_ref', lazy=True)
    # 与 Ticket 的多对多关系
    tickets = db.relationship('Ticket', secondary=ticket_issue_association, back_populates='issues')

    def __repr__(self):
        return f'<Issue: {self.title}>'


# | id | update_on | details | issue_id |
# Resolution --> Issue
class Resolution(db.Model):

    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    update_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    details = db.Column(db.String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = db.Column(db.String(20), db.ForeignKey('issue_table.id'), default=None)

    def __repr__(self):
        return f'<Resolution: {self.id}>'