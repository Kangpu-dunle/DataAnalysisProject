import pandas as pd
import matplotlib.pyplot as plt
import chardet
from matplotlib.font_manager import FontProperties

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
zh_font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

# 读取数据
try:
    with open('data.csv', 'rb') as f:
        result = chardet.detect(f.read())
    df = pd.read_csv('data.csv', encoding=result['encoding'])
    print("数据加载成功！")
except Exception as e:
    print(f"读取文件失败: {e}")
    exit()

# 数据清洗
print("\n原始数据中的缺失值：")
print(df.isnull().sum())

df.dropna(inplace=True)
print("\n删除缺失值后的数据：")
print(df.isnull().sum())

print("\n原始数据中的重复值数量：", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("\n删除重复值后的数据数量：", len(df))

# 数据分析
summary = df.describe()
print("\n数据摘要：")
print(summary)

# 按pro_name统计学校数量
pro_name_counts = df.groupby('pro_name')['name'].count().reset_index()
print("\n按pro_name统计的学校数量：")
print(pro_name_counts)

# 可视化
plt.figure(figsize=(15, 8))
bar = plt.bar(pro_name_counts['pro_name'], pro_name_counts['name'], color='skyblue')

# 添加数值标签
for i, rect in enumerate(bar):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., height,
             f'{int(height)}',
             ha='center', va='bottom',
             fontproperties=zh_font)

# 绘制折线
y_values = [rect.get_height() for rect in bar]
x_values = range(len(y_values))
plt.plot(x_values, y_values, color='red', linestyle='--', linewidth=1)

# 设置图表属性
plt.title(' 不同地区学校数量分布', fontproperties=zh_font, fontsize=14)
plt.xlabel(' 地区 (pro_name)', fontproperties=zh_font, fontsize=12)
plt.ylabel(' 学校数量 (name)', fontproperties=zh_font, fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)

# 调整布局
plt.tight_layout()

# 保存为 PNG 文件
plt.savefig('school_distribution.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
print("\n图表已保存为 school_distribution.png")

# 显示图表
plt.show()

# 保存数据
try:
    df.to_csv('cleaned_data.csv', index=False, encoding='utf-8')
    print("数据已成功保存为 cleaned_data.csv")
except PermissionError:
    print("保存文件失败，请检查文件权限或关闭已打开的文件。")