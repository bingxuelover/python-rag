from query import DatabaseQuery
from chart import ChartGenerator
from report import ReportGenerator
from flask import Flask, render_template, send_file
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    # 生成报告和图表
    report_gen = ReportGenerator()
    chart_gen = ChartGenerator()
    
    # 获取数据
    db = DatabaseQuery()
    data = db.get_sample_data()
    
    # 生成图表并保存为 base64 字符串
    charts = []
    
    # 月度统计图
    monthly_fig = chart_gen.create_monthly_chart(data, '文章发布月度统计')
    charts.append(fig_to_base64(monthly_fig))
    report_gen.add_chart(monthly_fig)
    
    # 类型分布图
    type_fig = chart_gen.create_type_distribution(data, '文章类型分布')
    charts.append(fig_to_base64(type_fig))
    report_gen.add_chart(type_fig)

    # 文章发布时间分布图
    time_fig = chart_gen.create_time_distribution(data, '文章发布时间分布')
    charts.append(fig_to_base64(time_fig))
    report_gen.add_chart(time_fig)
    
    # 保存报告
    report_gen.save_report('report.docx')
    
    # 渲染网页
    return render_template('charts.html', charts=charts)

@app.route('/download')
def download():
    """下载报告文件"""
    try:
        return send_file('report.docx',
                        as_attachment=True,
                        download_name='数据分析报告.docx')
    except Exception as e:
        return f"下载失败: {str(e)}", 500

def fig_to_base64(fig):
    """将图表转换为 base64 字符串，并保证中文正常显示"""
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建字节流对象
        img = io.BytesIO()
        
        # 保存图表，确保 DPI 足够高以显示清晰的中文
        fig.savefig(img, 
                   format='png', 
                   bbox_inches='tight',
                   dpi=300,  # 提高 DPI 使文字更清晰
                   pad_inches=0.1,  # 添加小边距
                   facecolor='white',  # 设置白色背景
                   )
        
        # 将指针移到开始位置
        img.seek(0)
        
        # 转换为 base64 字符串
        return base64.b64encode(img.getvalue()).decode()
        
    except Exception as e:
        print(f"转换图表为 base64 时出错: {str(e)}")
        raise
    finally:
        # 清理资源
        plt.close(fig)
        img.close()

if __name__ == '__main__':
    app.run(debug=True) 