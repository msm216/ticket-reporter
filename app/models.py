import enum

from datetime import datetime, timezone
from sqlalchemy import event, Enum, Table, Column, ForeignKey, String, Integer, Float, DateTime, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from . import db
from .utilities import random_serial_number, random_ticket_id, date_based_id



# Model of Device
class Country(enum.Enum):
    AT = "AT"
    BE = "BE"
    CZ = "CZ"
    DK = "DK"
    FI = "FI"
    FR = "FR"
    DE = "DE"
    IE = "IE"
    IT = "IT"
    NL = "NL"
    NO = "NO"
    PL = "PL"
    PT = "PT"
    SK = "SK"
    ES = "ES"
    SE = "SE"
    CH = "CH"
    GB = "GB"

# Model of Device
class Model(enum.Enum):
    IDC30 = "IDC30"
    IDC180 = "IDC180"
    IDC480 = "IDC480"

# Severity of Issue
class Severity(enum.Enum):
    vital = "Vital"
    critical = "Critical"
    grave = "Grave"
    normal = "Normal"
    minor = "Minor"

# Category of Issue
class Category(enum.Enum):
    development = "R&D"
    quality = "Quality"
    connectivity = "Connectivity"
    platform = "Platform"

# Reporter of Issue
class Member(enum.Enum):
    colleg_01 = "Peter"
    colleg_02 = "Louis"
    colleg_03 = "Chris"

# Progress of Issue
class Progress(enum.Enum):
    analyzing = "Analyzing"
    pending = "Pending"
    verify = "Verify"
    closed = "Closed"

# Type of Ticket
class Type(enum.Enum):
    abnormal = "Abnormal"
    commission = "Commission"
    connectivity = "Connectivity"
    platform = "Platform"

# Status of Ticket
class Status(enum.Enum):
    open = "Open"
    processing = "Processing"
    closed = "Closed"

# Action taken in Task
class Action(enum.Enum):
    consult = "Consult"
    debug = "Debug"
    repair = "Repair"
    commission = "Commission"
    spare_delivery = "Spare_delivery"
    callback = "Callback"

# Result of Task
class Result(enum.Enum):
    pending = "Pending"
    observation = "Observation"
    solved = "Solved"
    failed = "Failed"


# Ticket <--> Issue 关联表
ticket_issue_association = Table(
    'ticket_issue', db.Model.metadata,
    Column('ticket_id', String(20), ForeignKey('ticket_table.id')),
    Column('issue_id', String(20), ForeignKey('issue_table.id'))
)

# Ticket <--> Device 关联表
ticket_device_association = Table(
    'ticket_device', db.Model.metadata,
    Column('ticket_id', String(20), ForeignKey('ticket_table.id')),
    Column('device_id', String(20), ForeignKey('device_table.id'))
)



# | id | name | (sites) |
# Client <-- Site
class Client(db.Model):

    __tablename__ = 'client_table'

    id = Column(String(20), primary_key=True)
    name = Column(String(40), nullable=False, unique=True)
    # 反向关联 Site
    sites = relationship('Site', backref='client_ref', lazy=True)

    def __repr__(self):
        return f'<Client: {self.name}>'
    
    @staticmethod
    def generate_client_id(mapper, connection, target):
        max_id = db.session.query(db.func.max(Client.id)).scalar()
        new_id_num = int(max_id.split('-')[1]) + 1 if max_id else 1
        target.id = f'CLIENT-{new_id_num:03d}'
        return

# 将事件监听器绑定到 Client 类的 before_insert 事件上
event.listen(Client, 'before_insert', Client.generate_client_id)



# | id | model | install_on | site_id |
# Device --> Site
# Device <-> Ticket
class Device(db.Model):

    __tablename__ = 'device_table'

    id = Column(String(20), primary_key=True)
    model = Column(Enum(Model), nullable=False)
    material = Column(String(20), nullable=False)
    install_on = Column(DateTime, default=lambda: datetime.now(timezone.utc).date())
    # 外键指向一个 Client 实例
    site_id = Column(String(20), ForeignKey('site_table.id'), nullable=True)
    # 与 Ticket 的多对多关系
    tickets = relationship('Ticket', secondary=ticket_device_association, back_populates='devices')

    def __repr__(self):
        return f'<Site: {self.id}>'
    
    @staticmethod
    def generate_device_sn(mapper, connection, target):
        target.id = random_serial_number()
        return

# 将事件监听器绑定到 Device 类的 before_insert 事件上
event.listen(Device, 'before_insert', Device.generate_device_sn)



# | id | name | address | zip | latitude | longitude | owner_id | (devices) | (tickets) |
# Site --> Client
# Site <-- Device
class Site(db.Model):

    __tablename__ = 'site_table'

    id = Column(String(20), primary_key=True)
    name = Column(String(40), nullable=False, unique=True)
    address = Column(String(30), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(Enum(Country), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # 外键指向一个 Client 实例
    owner_id = Column(String(20), ForeignKey('client_table.id'), nullable=True)
    # 反向关联 Device
    devices = relationship('Device', backref='site_ref', lazy=True)

    def __repr__(self):
        return f'<Site: {self.name}>'
    
    @staticmethod
    def generate_site_id(mapper, connection, target):
        max_id = db.session.query(db.func.max(Site.id)).scalar()
        new_id_num = int(max_id.split('-')[1]) + 1 if max_id else 1
        target.id = f'SITE-{new_id_num:03d}'
        return

# 将事件监听器绑定到 Site 类的 before_insert 事件上
event.listen(Site, 'before_insert', Site.generate_site_id)



class Commission(db.Model):

    __tablename__ = 'commission_table'

    id = Column(String(20), primary_key=True)
    commission_on = Column(DateTime, default=lambda: datetime.now(timezone.utc).date())
    executor = Column(Enum(Member), nullable=False)
    # 外键指向一个 Site 实例
    site_id = Column(String(20), ForeignKey('site_table.id'), nullable=True)
    # 外键指向一个 Device 实例
    device_id = Column(String(20), ForeignKey('device_table.id'), nullable=True)

    def __repr__(self):
        return f'<Commission on: {self.commission_on}>'
    
    @staticmethod
    def generate_comm_id(mapper, connection, target):
        target.id = date_based_id(Commission, target, db.session, 'commission_on', prefix='RESUL')
        return

# 将事件监听器绑定到 Site 类的 before_insert 事件上
event.listen(Commission, 'before_insert', Commission.generate_comm_id)



# | id | title | title_cn | create_on | ticket_type | description | status |
# | first_response | first_response_on | final_resolution | close_on |
# Ticket <-- Task
# Ticket <-> Device
# Ticket <-> Issue
class Ticket(db.Model):

    __tablename__ = 'ticket_table'

    id = Column(String(20), primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    title_cn = Column(String(40), nullable=True, unique=True)
    create_on = Column(DateTime, default=lambda: datetime.now(timezone.utc).date())
    ticket_type = Column(Enum(Type), nullable=True)
    description = Column(String(160), nullable=False)
    status = Column(Enum(Status), default=Status.open, nullable=False)
    first_response = Column(String(80), nullable=True)
    first_response_on = Column(DateTime, nullable=True)
    final_resolution = Column(String(80), nullable=True)
    close_on = Column(DateTime, nullable=True)
    # 反向关联 Task，lazy='dynamic' 使得反向关系被访问时返回一个对象而不是列表
    tasks = relationship('Task', backref='ticket_ref', lazy=True)
    # 与 Issue 的多对多关系
    issues = relationship('Issue', secondary=ticket_issue_association, back_populates='tickets')
    # 与 Device 的多对多关系
    devices = relationship('Device', secondary=ticket_device_association, back_populates='tickets')

    def __repr__(self):
        return f'<Ticket: {self.id}>'
    
    @staticmethod
    def generate_ticket_id(mapper, connection, target):
        target.id = random_ticket_id()
        return

# 将事件监听器绑定到 Ticket 类的 before_insert 事件上
event.listen(Ticket, 'before_insert', Ticket.generate_ticket_id)



# | id | execute_on | action | description | on_site | result | ticket_id |
# Task --> Ticket
class Task(db.Model):

    __tablename__ = 'task_table'

    id = Column(String(20), primary_key=True)
    execute_on = Column(DateTime, default=lambda: datetime.now(timezone.utc).date())
    action = Column(Enum(Action), nullable=False)
    description = Column(String(80), nullable=False)
    on_site = Column(Boolean, default=False, nullable=False)
    result = Column(Enum(Result), default=Result.pending, nullable=False)
    # 外键指向一个 Ticket 实例
    ticket_id = Column(String(20), ForeignKey('ticket_table.id'), nullable=False)

    def __repr__(self):
        return f'<Resolution: {self.id}>'
    
    # 根据日期生成ID
    @staticmethod
    def generate_task_id(mapper, connection, target):
        target.id = date_based_id(Task, target, db.session, 'execute_on', prefix='TASK')
        return

# 绑定事件监听器
event.listen(Task, 'before_insert', Task.generate_task_id)



# | id | title | title_cn | report_on | category | description | severity | progress |
# | final_resolution | close_on | (resolutions) | (tickets) |
# Issue <-- Resolution
# Issue <-> Ticket
class Issue(db.Model):

    __tablename__ = 'issue_table'

    id = Column(String(20), primary_key=True)
    title = Column(String(40), nullable=False, unique=True)
    title_cn = Column(String(40), nullable=True)
    report_on = Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    report_by = Column(Enum(Member), nullable=False)
    category = Column(Enum(Category), nullable=False)
    description = Column(String(160), nullable=False)
    severity = Column(Enum(Severity), nullable=True)
    progress = Column(Enum(Progress), default=Progress.analyzing, nullable=False)
    final_resolution = Column(String(80), nullable=True)
    close_on = Column(DateTime, nullable=True)
    # 反向关联 Resolution，lazy='dynamic' 使得反向关系被访问时返回一个对象而不是列表
    resolutions = relationship('Resolution', backref='issue_ref', lazy=True)
    # 与 Ticket 的多对多关系
    tickets = relationship('Ticket', secondary=ticket_issue_association, back_populates='issues')

    def __repr__(self):
        return f'<Issue: {self.title}>'
    
    # 根据日期生成ID
    @staticmethod
    def generate_issue_id(mapper, connection, target):
        target.id = date_based_id(Issue, target, db.session, 'report_on', prefix='ISSUE')
        return

# 绑定事件监听器
event.listen(Issue, 'before_insert', Issue.generate_issue_id)



# | id | update_on | details | issue_id |
# Resolution --> Issue
class Resolution(db.Model):

    __tablename__ = 'resolution_table'

    id = Column(String(20), primary_key=True)
    update_on = Column(DateTime, default=lambda: datetime.now(timezone.utc).date())
    description = Column(String(80), nullable=False)
    # 外键指向一个 Issue 实例
    issue_id = Column(String(20), ForeignKey('issue_table.id'), nullable=False)

    def __repr__(self):
        return f'<Resolution: {self.id}>'
    
    # 根据日期生成ID
    @staticmethod
    def generate_resolution_id( mapper, connection, target):
        target.id = date_based_id(Resolution, target, db.session, 'update_on', prefix='RESUL')
        return

# 绑定事件监听器
event.listen(Resolution, 'before_insert', Resolution.generate_resolution_id)