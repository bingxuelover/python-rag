import matplotlib.pyplot as plt
import seaborn as sns
from config import CHART_CONFIG
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

class ChartGenerator:
    def __init__(self):
        # 设置中文字体
        self._setup_chinese_font()
        
        self.config = {
            'figsize': (10, 6),
            'style': 'whitegrid'
        }
        sns.set_style(self.config['style'])
        
    def _setup_chinese_font(self):
        """设置中文字体"""
        # 尝试多个中文字体，按优先级排序
        chinese_fonts = [
            'SimHei',          # Windows 黑体
            'Microsoft YaHei', # Windows 微软雅黑
            'PingFang SC',     # macOS/iOS 苹方
            'Hiragino Sans GB' # macOS 冬青黑体
        ]
        
        # 设置字体
        for font in chinese_fonts:
            try:
                plt.rcParams['font.sans-serif'] = [font]
                # 测试字体
                plt.rcParams['axes.unicode_minus'] = False
                test_fig = plt.figure()
                test_fig.text(0.5, 0.5, '测试中文')
                plt.close(test_fig)
                print(f"成功使用字体: {font}")
                return
            except:
                continue
        
        print("警告：未能找到合适的中文字体，可能会导致中文显示异常")

    def create_line_chart(self, data, x, y, title):
        """创建折线图"""
        # 创建 DataFrame，使用所有列名
        df = pd.DataFrame(data, columns=['post_date', 'post_title', 'post_parent', 'post_type'])
        
        plt.figure(figsize=self.config['figsize'])
        # 只使用我们需要的两列来绘图
        sns.lineplot(data=df, x='post_date', y='post_title')
        
        plt.title(title)
        plt.xlabel('发布日期')
        plt.ylabel('标题')
        
        # 旋转 x 轴标签以防重叠
        plt.xticks(rotation=45, ha='right')
        
        # 调整布局以确保标签可见
        plt.tight_layout()
        
        return plt.gcf()

    def create_bar_chart(self, data, x, y, title):
        try:
            # 将数据转换为 DataFrame
            data_list = []
            for row in data:
                # 使用 _mapping 属性获取行数据
                data_list.append(dict(row._mapping))
            
            df = pd.DataFrame(data_list)
            
            # 创建图表
            plt.figure(figsize=self.config['figsize'])
            sns.barplot(data=df, x=x, y=y)
            
            # 设置标题和标签
            plt.title(title)
            plt.xlabel(x)
            plt.ylabel(y)
            
            # 旋转 x 轴标签
            plt.xticks(rotation=45, ha='right')
            
            # 调整布局
            plt.tight_layout()
            
            return plt.gcf()
            
        except Exception as e:
            print(f"创建图表时出错: {str(e)}")
            raise

    def create_pie_chart(self, data, type_column, title):
        try:
            # 将数据转换为 DataFrame
            df = pd.DataFrame(data, columns=['post_title', 'post_date', 'post_parent', 'post_type'])
            
            # 统计每种类型的数量
            type_counts = df[type_column].value_counts()
            
            plt.figure(figsize=self.config['figsize'])
            # 使用统计后的数据创建饼图
            plt.pie(type_counts.values, 
                   labels=type_counts.index, 
                   autopct='%1.1f%%')
            
            plt.title(title)
            plt.axis('equal')  # 使饼图为正圆形
            
            return plt.gcf()
            
        except Exception as e:
            print(f"创建饼图时出错: {str(e)}")
            print(f"数据示例: {data[:2] if data else 'No data'}")
            raise

    def create_monthly_chart(self, data, title):
        try:
            # 将数据转换为 DataFrame
            df = pd.DataFrame([dict(row._mapping) for row in data])
            
            # 将日期转换为月份格式
            df['month'] = pd.to_datetime(df['post_date']).dt.strftime('%Y-%m')
            
            # 按月份统计文章数量
            monthly_counts = df.groupby('month').size().reset_index()
            monthly_counts.columns = ['month', 'count']
            
            plt.figure(figsize=self.config['figsize'])
            
            # 创建柱状图
            sns.barplot(data=monthly_counts, x='month', y='count')
            
            # 在柱子上添加数值标签
            for i, v in enumerate(monthly_counts['count']):
                plt.text(i, v, str(v), ha='center', va='bottom')
            
            plt.title(title)
            plt.xlabel('月份')
            plt.ylabel('文章数量')
            
            # 旋转 x 轴标签以防重叠
            plt.xticks(rotation=45, ha='right')
            
            # 调整布局
            plt.tight_layout()
            
            return plt.gcf()
            
        except Exception as e:
            print(f"创建月度统计图表时出错: {str(e)}")
            raise

    def create_type_distribution(self, data, title):
        try:
            # 将数据转换为 DataFrame
            df = pd.DataFrame([dict(row._mapping) for row in data])
            
            # 统计每种类型的数量并排序
            type_counts = df['post_type'].value_counts()
            
            # 创建图表
            plt.figure(figsize=self.config['figsize'])
            
            # 绘制饼图
            patches, texts, autotexts = plt.pie(
                type_counts.values,
                labels=type_counts.index,
                autopct='%1.1f%%',  # 显示百分比
                textprops={'fontsize': 12}
            )
            
            # 设置标题
            plt.title(title)
            
            # 添加图例
            plt.legend(
                type_counts.index,
                title="文章类型",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            # 确保饼图为圆形
            plt.axis('equal')
            
            # 调整布局以显示完整的图例
            plt.tight_layout()
            
            # 打印调试信息
            print(f"类型统计: {type_counts.to_dict()}")
            
            return plt.gcf()
            
        except Exception as e:
            print(f"创建类型分布图表时出错: {str(e)}")
            print(f"数据示例: {data[:2] if data else '无数据'}")
            raise

    def create_time_distribution(self, data, title):
        try:
            # 将数据转换为 DataFrame
            df = pd.DataFrame([dict(row._mapping) for row in data])
            
            # 提取小时信息
            df['hour'] = pd.to_datetime(df['post_date']).dt.hour
            
            # 统计每个小时的文章数量
            hour_counts = df['hour'].value_counts().sort_index()
            
            plt.figure(figsize=self.config['figsize'])
            
            # 创建柱状图
            ax = sns.barplot(x=hour_counts.index, y=hour_counts.values)
            
            # 在柱子上添加数值标签
            for i, v in enumerate(hour_counts.values):
                ax.text(i, v, str(v), ha='center', va='bottom')
            
            # 设置标题和标签
            plt.title(title)
            plt.xlabel('发布时间（小时）')
            plt.ylabel('文章数量')
            
            # 设置 x 轴刻度
            plt.xticks(range(24), [f'{i:02d}:00' for i in range(24)], rotation=45)
            
            # 添加网格线使图表更易读
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            # 调整布局
            plt.tight_layout()
            
            # 打印调试信息
            print(f"时间分布统计: \n{hour_counts.to_string()}")
            
            return plt.gcf()
            
        except Exception as e:
            print(f"创建时间分布图表时出错: {str(e)}")
            print(f"数据示例: {data[:2] if data else '无数据'}")
            raise