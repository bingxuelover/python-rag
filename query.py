import pandas as pd
from sqlalchemy import create_engine, text
from config import DB_CONFIG
import time

class DatabaseQuery:
    def __init__(self):
        # 创建数据库连接字符串
        self.connection_string = (
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        # 创建数据库引擎
        self.engine = create_engine(
            self.connection_string,
            pool_recycle=3600,  # 设置连接回收时间为1小时
            pool_pre_ping=True  # 在每次使用连接前ping一下数据库
        )

    def execute_query(self, query):
        max_retries = 3
        retry_count = 0
        last_error = None

        while retry_count < max_retries:
            try:
                self.engine.dispose()
                with self.engine.connect() as connection:
                    connection.execute(text("SET SESSION wait_timeout=28800"))
                    connection.execute(text("SET SESSION interactive_timeout=28800"))
                    
                    # 执行查询
                    result = connection.execute(text(query))
                    data = result.fetchall()
                    
                    # 添加调试信息
                    print("查询结果示例：")
                    print(f"数据行数: {len(data)}")

                    # 将数据导出为xlsx文件
                    df = pd.DataFrame(data, columns=result.keys())
                    # 导出文件地址为当前目录
                    df.to_excel('data.xlsx', index=False)

                    # 打印第一行数据
                    if data:
                        print(f"第一行数据: {data[0]}")
                        print(f"数据列: {result.keys()}")
                    
                    return data
                    
            except Exception as e:
                last_error = e
                retry_count += 1
                print(f"查询执行错误 (尝试 {retry_count}/{max_retries}): {str(e)}")
                time.sleep(retry_count * 2)
                
                if retry_count == max_retries:
                    print(f"达到最大重试次数，最后错误: {str(last_error)}")
                    raise last_error

    def get_sample_data(self):
        """获取示例数据"""
        # 定义SQL查询语句
        sql = """
        SELECT 
            post_date,
            post_title,
            post_parent,
            post_type
        FROM wp_posts
        WHERE post_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
        ORDER BY post_date
        """
        # 执行SQL查询并返回DataFrame
        return self.execute_query(sql) 