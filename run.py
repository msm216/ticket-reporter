# 配置日志级别和环境变量 - 在导入其他模块之前设置
import os
import sys

# 设置环境变量 - 保留必要的设置，但不抑制 Flask 输出
os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'  # 忽略弃用警告

# 导入其他模块
import logging
import warnings
from app import create_app

# 过滤特定的警告
warnings.filterwarnings("ignore", category=UserWarning, module="gi.*")
warnings.filterwarnings("ignore", category=Warning, message=".*UWP app.*")

# 配置日志级别
logging.getLogger('weasyprint').setLevel(logging.ERROR)  # 设置 WeasyPrint 日志级别
logging.getLogger('fontTools').setLevel(logging.ERROR)   # 设置 fontTools 日志级别

# 配置基本日志
logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Access the application at: http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)  # 禁用重载器可能会减少一些警告