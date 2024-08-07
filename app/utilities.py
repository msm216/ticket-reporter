import os
import re
import shutil
import random
import enum
import string
import subprocess

import pandas as pd

from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import func, inspect
from sqlalchemy.orm import Session

from . import db


# 生成随机序列号
def random_serial_number() -> str:
    serial_number = "A" + str(random.randint(10**9, 10**10 - 1))
    return serial_number


# 生成随机Ticket号
def random_ticket_id() -> str:
    ticket_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=10))
    return ticket_id


# 根据类名和实例日期生成id
def date_based_id(model, target, session:Session, date_attr:str, prefix:str) -> str:
    date_str = getattr(target, date_attr).strftime('%Y%m%d')
    existing_inst = session.query(model).filter(
        db.func.strftime('%Y%m%d', getattr(model, date_attr)) == date_str
    ).all()
    if existing_inst:
        max_id_num = max([int(task.id.split('-')[-1]) for task in existing_inst])
        new_id_num = max_id_num + 1
    else:
        new_id_num = 1
    return f'{prefix}-{date_str}-{new_id_num:02d}'


# 生成特定长度随机字符串
def random_string(length:int) -> str:
    # string.punctuation 特殊字符
    characters = string.ascii_letters + string.digits
    random_string = ''.join(
        random.choice(characters) for i in range(length))
    return random_string


# 生成矩形范围内随机经纬度
def random_coordinates() -> tuple[float, float]:
    # 欧洲大陆大致范围的经纬度
    min_latitude = 35.0   # 南部边界：约为地中海区域
    max_latitude = 71.0   # 北部边界：约为北极圈附近
    min_longitude = -10.0  # 西部边界：约为葡萄牙
    max_longitude = 40.0   # 东部边界：约为乌拉尔山脉
    # 生成随机的纬度和经度
    latitude = random.uniform(min_latitude, max_latitude)
    longitude = random.uniform(min_longitude, max_longitude)
    return latitude, longitude


# 生成特定范围内随机时间戳
# random_date(90)  # 过去90天范围内的随机日期
# random_date(30, 90)  # 过去90天至30天范围内的随机日期
# random_date(90, origin=datetime(2024, 1, 1))  # 基准日期（2024-01-01）过去90天至范围内的随机日期
# random_date(30, 90, origin=datetime(2024, 5, 7), direction=False)  # 基准日期（2024-05-07）之后30至90天范围内的随机日期
def random_date(*args, origin=None, direction: bool=True) -> datetime:
    # 随机日期范围
    if len(args) == 1:
        roll_back = args[0]
        start_day = 0
    elif len(args) == 2:
        start_day, roll_back = args
    else:
        raise ValueError("Function accepts either 1 or 2 arguments only.")
    # 判断基准时间
    if origin is None:
        origin = datetime.now(timezone.utc)
    delta_days = random.randint(start_day, roll_back)
    # 回溯或前推
    if direction:
        some_day = origin - timedelta(days=delta_days)
    else:
        some_day = origin + timedelta(days=delta_days)
    return some_day


# 将模型实例列表转换为 DataFrame
def model_to_dataframe(model) -> pd.DataFrame:
    if not issubclass(model, db.Model):
        raise TypeError("Input should be a subclass of SQLAlchemy db.Model.")
    instances = model.query.all()
    data = []
    for instance in instances:
        model_dict = {}
        for c in inspect(instance).mapper.column_attrs:
            value = getattr(instance, c.key)
            if isinstance(value, enum.Enum):
                model_dict[c.key] = value.name
            else:
                model_dict[c.key] = value
        data.append(model_dict)
    return pd.DataFrame(data)


# 确保日期格式为 <class 'datetime.datetime'>
def date_for_sqlite(meta_date:str) -> datetime:
    if meta_date == '':
        new_date = datetime.now(timezone.utc)
    else:
        new_date = datetime.strptime(meta_date, '%Y-%m-%d')
    return new_date


# 验证文件扩展名
def if_allowed_file(filename:str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


# 获取git最后提交日期
def last_commit_time() -> str:
    try:
        # 获取最后提交的时间戳
        result = subprocess.run(['git', 'log', '-1', '--format=%ct'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            timestamp = int(result.stdout.decode('utf-8').strip())
            # 将时间戳转换为人类可读的格式
            last_commit_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return last_commit_time
        else:
            return "Unknown"
    except Exception as e:
        return f"Error: {e}"
    

# 验证文件扩展名
def allowed_file(filename:str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


# 验证GSP数据文件名
def valid_filename(filename) -> bool:
    # 定义正则表达式模式
    pattern = r"^案例清单列表_\d{14}\.(csv|xlsx)$"
    # 使用正则表达式进行匹配
    match = re.match(pattern, filename)
    return bool(match)


### 处理 GSP 数据 ###

# 检查指定目录中文件名符合规则且修改时间最新的csv文件，将其余文件移至arch归档（FINISHED）
def get_latest_csv(dir: str, pattern: str) -> tuple[str, datetime]:
    latest_file = None
    latest_mtime = 0
    # 创建 arch 文件夹如果不存在
    gsp_arch_dir = os.path.join(dir, 'arch')
    os.makedirs(gsp_arch_dir, exist_ok=True)
    # 遍历目录下的所有文件
    for filename in os.listdir(dir):
        # 使用正则表达式匹配文件名
        match = re.match(pattern, filename)
        #if filename.endswith(".csv"):
        if match:
            #print(f"Compliant csv file {filename} fund.")
            filepath = os.path.join(dir, filename)
            mtime = os.path.getmtime(filepath)
            # 比较修改时间，更新最新的文件和修改时间
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_file = filename
        else:
            #print(f"Not-compliant file {filename} fund.")
            pass
    # 如果找到了最新的文件
    if latest_file:
        # 获取最新文件的修改时间
        time_stempel = datetime.fromtimestamp(latest_mtime)
        print(f"Newest gsp record: {latest_file} exported at {time_stempel}")
        # 遍历目录下的所有文件，并将非最新的文件移动到 arch 文件夹
        for filename in os.listdir(dir):
            match = re.match(pattern, filename)
            if match and filename != latest_file:
                old_filepath = os.path.join(dir, filename)
                new_filepath = os.path.join(gsp_arch_dir, filename)
                shutil.move(old_filepath, new_filepath)
                print(f"Moved {filename} to {gsp_arch_dir}")
    else:
        print(f"No compliant GSP record fund under: {dir}")
    return latest_file, time_stempel


# 标准化 GSP 记录
def standardize_gsp(gsp_df:pd.DataFrame) -> pd.DataFrame:

    df = gsp_df
    
    # | id | title | title_cn | create_on | ticket_type | description | status |
    # | first_response | first_response_on | final_resolution | close_on |
    return df




# 根据上传的数据 DataFrame 更新表格
def update_tickets_from_dataframe(cls, df:pd.DataFrame):
    # 逐条遍历 DataFrame
    for _, row in df.iterrows():
        group_id = row['id']
        group_name = row['name']
        created_on = row['created_on']
        #first_register = row.get('first_register')
        #last_register = row.get('last_register')

        # 尝试根据 id 获取数据库中已有实例
        group = cls.query.get(group_id)
        if group is None:
            # 不存在同 id 实例则添加
            group = cls(
                id=row['id'], 
                title=row[''], 
                title_cn=row[''], 
                create_on=row[''],
                ticket_type=row[''],
                description=row[''],
                status=row[''],
                first_response=row[''],
                first_response_on=row[''],
                final_resolution=row[''],
                close_on=row['close_on'],
            )
            print(f"Add new instance: {group}")
            db.session.add(group)
        else:
            # 存在同 id 实例则更新部分属性
            print(f"Update instance: {group}")
            group.name = group_name
            group.created_on = created_on
            #group.first_register = first_register
            #group.last_register = last_register
            pass
        db.session.commit()
    
    return
