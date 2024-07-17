import os
import random
import string
import subprocess

from datetime import datetime, timezone, timedelta


# 生成随机序列号
def generate_random_sn() -> str:
    sn = "A" + str(random.randint(10**9, 10**10 - 1))
    return sn


# 生成随机Ticket号
def generate_random_ticket() -> str:
    ticket_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=10))
    return ticket_id


# 生成特定长度随机字符串
def generate_random_string(length:int) -> str:
    # string.punctuation 特殊字符
    characters = string.ascii_letters + string.digits
    random_string = ''.join(
        random.choice(characters) for i in range(length))
    return random_string


# 生成矩形范围内随机经纬度
def generate_random_coordinates() -> tuple[float, float]:
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
def generate_random_date(*args, origin=None, direction=True) -> datetime:
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


# 根据类名和实例日期生成id
def date_to_id(model_name, date, sequence_number) -> str:
    date_str = date.strftime("%Y%m%d")
    return f"{model_name}-{date_str}-{sequence_number:03d}"


# 验证文件扩展名
def allowed_file(filename:str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


# 获取git最后提交日期
def get_last_commit_time() -> datetime:
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