# 可以从数据库读取数据，生成图表

## 1. 从数据库读取数据

- 使用 Python 的 `pandas` 库连接数据库
- 支持多种数据库类型：MySQL, PostgreSQL, SQLite
- 通过 SQL 查询获取所需数据

## 2. 生成图表

- 使用 `matplotlib` 和 `seaborn` 库绘制图表
- 支持多种图表类型：
  - 折线图
  - 柱状图
  - 饼图
  - 散点图
  - 热力图
- 可自定义图表样式和主题

## 3. 生成报告

- 使用 `python-docx` 生成 Word 文档
- 支持将图表直接嵌入文档
- 可添加自定义文本说明
- 支持导出为 PDF 格式

## 4. 使用要求

- Python 3.7+
- 所需依赖包：
  - pandas >= 1.3.0
  - matplotlib >= 3.4.0
  - seaborn >= 0.11.0
  - python-docx >= 0.8.11
  - sqlalchemy >= 1.4.0
  - pymysql >= 1.0.2 (MySQL连接器)
  - openpyxl >= 3.0.0 (Excel文件支持)
  - xlrd >= 2.0.0 (Excel文件支持)
  - python-dotenv >= 0.19.0 (环境变量管理)
  - tqdm >= 4.62.0 (进度条显示)

## 5. 使用方法

1. 创建并激活虚拟环境（推荐）：

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

2. 安装所需依赖包：

   ```bash
   # 方法1：使用pip直接安装基础依赖
   pip install pandas matplotlib seaborn python-docx sqlalchemy python-dotenv tqdm

   # 方法2：安装数据库连接器（根据需要选择安装）
   pip install pymysql  # MySQL

   # 方法3：安装Excel文件支持
   pip install openpyxl xlrd

   # 方法4：一次性安装所有依赖（推荐）
   pip install -r requirements.txt
   ```

3. 配置数据库连接信息：
   - 在 `config.py` 文件中配置数据库连接信息，包括数据库类型、用户名、密码、主机和端口等。

4. 编写 SQL 查询语句：
   - 在 `query.py` 文件中编写 SQL 查询语句，获取所需数据。

5. 生成图表：
   - 在 `chart.py` 文件中编写图表生成代码，根据需要选择合适的图表类型和样式。

6. 生成报告：
   - 在 `report.py` 文件中编写报告生成代码，将图表嵌入到 Word 文档中，并添加自定义文本说明。

7. 运行程序：
   - 在终端中运行 `python app.py` 命令，执行程序。

8. 查看结果：
   - 程序运行完成后，会在当前目录下生成一个 `report.docx` 文件，打开该文件即可查看生成的报告。
   - 如果需要导出为 PDF 格式，可以使用 `python-docx` 库提供的 `save` 方法，将 Word 文档保存为 PDF 文件。

## 6. 注意事项

- 请确保数据库连接信息正确，并且数据库中存在所需的表和数据。
- 请根据实际需求修改 SQL 查询语句和图表生成代码。
- 请确保 Python 环境中已安装所需的依赖包。
