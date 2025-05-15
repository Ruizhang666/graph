# 三层股权穿透网络分析

本项目使用NetworkX库对三层股权穿透数据进行网络分析和可视化。

## 项目结构

主要脚本：
- `graph_model.py`: 基础网络建模和可视化。
- `advanced_analysis.py`: 高级网络分析和可视化。

辅助模块：
- `font_config.py`: 用于配置matplotlib中文字体。
- `graph_builder.py`: 用于从CSV数据构建股权网络图（NetworkX对象）。

数据文件：
- `三层股权穿透输出数据.csv`: 输入的股权数据。

输出文件示例：
- `股权关系网络图.png`
- `股权关系社区结构.png`
- `最终控制人网络图.png`

## 功能

该项目包含两个主要脚本：

1. `graph_model.py` - 基础网络建模和可视化
   - 构建股权网络图（节点为公司和个人，边为持股关系）
   - 基本可视化和统计分析
   - 输出网络结构基本指标

2. `advanced_analysis.py` - 高级网络分析
   - 中心性分析（度中心性、接近中心性、中介中心性、特征向量中心性）
   - 社区检测（使用Louvain算法）
   - 循环持股关系识别
   - 关键控制者分析
   - 最终控制人分析

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 将三层股权穿透数据保存为CSV文件（示例：`三层股权穿透输出数据.csv`）
2. 运行基础分析：

```bash
python graph_model.py
```

3. 运行高级分析：

```bash
python advanced_analysis.py
```

## 输出结果

- `股权关系网络图.png` - 基本网络可视化
- `股权关系社区结构.png` - 社区划分可视化
- `最终控制人网络图.png` - 最终控制人及其控制网络可视化
- 终端输出详细的分析结果

## 数据格式说明

输入CSV文件需要包含以下字段：
- `eid`: 实体ID
- `name`: 实体名称
- `type`: 实体类型（E-企业，P-个人，UE-其他类型）
- `short_name`: 简称
- `amount`: 投资金额
- `percent`: 持股比例
- `sh_type`: 股权类型
- `level`: 层级
- `parent_id`: 父节点ID

## 注意事项

- 社区检测需要安装python-louvain库
- 中文字体显示需要系统支持中文字体 