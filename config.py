import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test'),
}

# 图表配置
CHART_CONFIG = {
    'style': 'seaborn',  # 图表样式
    'figsize': (10, 6),  # 图表大小
    'dpi': 100,         # 图表分辨率
}

# 报告配置
REPORT_CONFIG = {
    'template': 'template.docx',  # 报告模板
    'output': 'report.docx',      # 输出文件名
} 