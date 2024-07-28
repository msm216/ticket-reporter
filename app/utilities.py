import os
import random
import string
import subprocess

import pandas as pd

from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import func
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
def date_based_id(cls, target, session:Session, prefix:str) -> str:
    execute_date_str = target.execute_on.strftime('%Y%m%d')
    existing_tasks = session.query(cls).filter(
        func.strftime('%Y%m%d', cls.execute_on) == execute_date_str
    ).all()
    if existing_tasks:
        max_id_num = max([int(task.id.split('-')[-1]) for task in existing_tasks])
        new_id_num = max_id_num + 1
    else:
        new_id_num = 1
    return f'{prefix}-{execute_date_str}-{new_id_num:02d}'


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
# generate_random_date(30, 90)  # 过去90天至30天范围内的随机日期
# generate_random_date(90, origin=datetime(2024, 1, 1))  # 过去90天至基准日期（2024-01-01）范围内的随机日期
# generate_random_date(30, 90, origin=datetime(2024, 1, 1), direction=False)  # 基准日期（2024-01-01）之后30至90天范围内的随机日期
def random_date(*args, origin=None, direction=True) -> datetime:
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
def last_commit_time() -> datetime:
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
    
'''
# 修改 GSP 记录
def get_gsp_record() -> pd.DataFrame:


    gsp_df
    
    return gsp_df
'''



# 验证文件扩展名
def allowed_file(filename:str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


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
                details=row[''],
                status=row[''],
                first_response=row[''],
                first_response_on=row[''],
                final_resolution=row[''],
                close_on=row[''],
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
