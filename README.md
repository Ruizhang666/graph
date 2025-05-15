# 三层股权穿透网络分析与查询

本项目使用 Python 和 NetworkX 等库，对符合特定格式的股权穿透数据CSV文件进行网络建模、高级分析、可视化以及节点邻域查询。

## 项目特色

- **股权网络构建**: 从CSV数据准确构建有向图，正确处理`parent_id`和嵌套的`children`字段确定的股权关系 (遵循 Child -> Parent 规则)。
- **多样化分析**: 
    - `graph_model.py`: 提供基础的图统计数据和整体股权网络图的可视化。
    - `advanced_analysis.py`: 执行深入分析，包括中心性分析（度、接近、中介、特征向量）、社区检测（Louvain算法）、循环持股识别、关键控制者识别、最终控制人分析以及链路合理性检查，并生成详细的文本报告和可视化图表。
    - `query_node_neighborhood.py`: 允许用户通过节点名称查询其指定度数（默认为2度）的邻域网络，输出详细的节点/边信息到文本文件，并生成邻域可视化图。
- **模块化设计**: 
    - `graph_builder.py`: 封装了核心的图构建逻辑。
    - `font_config.py`: 统一管理中文字体配置，确保图表中文显示正常。
- **可配置输出**: 生成多种图片（.png）和文本报告（.txt）便于结果查阅和分享。

## 项目结构

```
graph/
├── graph_model.py               # 基础网络建模与可视化
├── advanced_analysis.py         # 高级网络分析与报告生成
├── query_node_neighborhood.py   # 节点邻域查询与可视化
├── graph_builder.py             #核心图构建模块
├── font_config.py               # 中文字体配置模块
├── 三层股权穿透输出数据.csv       # 【示例】输入的股权数据CSV文件
├── requirements.txt             # Python依赖包列表
├── README.md                    # 本文件
├── graph_model_visualization.png # graph_model.py 输出的示例图
├── 股权关系社区结构.png           # advanced_analysis.py 输出的示例图
├── 最终控制人网络图.png           # advanced_analysis.py 输出的示例图
├── advanced_analysis_report.txt # advanced_analysis.py 输出的文本报告
├── query_result_*.png           # query_node_neighborhood.py 输出的示例图
└── query_result_*.txt           # query_node_neighborhood.py 输出的文本报告
```

## 安装依赖

1.  确保您已安装 Python 3.8 或更高版本。
2.  建议使用虚拟环境以避免包冲突：
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```
3.  安装所需的依赖包：
    ```bash
    pip install -r requirements.txt
    ```

## 数据格式说明

输入的CSV文件（例如 `三层股权穿透输出数据.csv`）应包含但不限于以下关键字段，用于构建股权关系网络：

- `eid`: 实体唯一ID (推荐，如果名称可能重复)。如果缺失，将使用`name`作为ID。
- `name`: 实体名称（公司或个人）。
- `type`: 实体类型 (例如: 'E'代表企业, 'P'代表个人)。用于可视化时的节点区分。
- `level`: 实体在股权结构中的层级。用于可视化标签。
- `parent_id`: 该实体直接父节点的ID。关系为：当前实体 -> `parent_id`实体。
- `children`: 一个JSON字符串，描述直接持有当前实体股份的股东信息。每个股东对象可包含`name`, `eid`, `type`, `level`, `percent`等。关系为：`children`中的股东 -> 当前实体。
- `percent`: 持股比例 (例如 '10.5%' 或 '10.5')。
- `amount`: 投资金额。
- `sh_type`: 股东类型/持股类型。

**重要**: `graph_builder.py` 会尝试使用多种中文编码（gbk, gb18030, gb2312, utf-8, big5）读取CSV文件。

## 使用方法

确保您的CSV数据文件与脚本在同一目录，或在脚本中指定正确的文件路径。

1.  **基础网络建模与整体可视化 (`graph_model.py`)**
    ```bash
    python graph_model.py
    ```
    - 输出: 
        - 控制台打印图的基本统计信息。
        - 生成 `graph_model_visualization.png` 图片。

2.  **高级网络分析与报告生成 (`advanced_analysis.py`)**
    ```bash
    python advanced_analysis.py
    ```
    - 输出:
        - 控制台打印分析过程和总结。
        - 生成 `advanced_analysis_report.txt` 包含详细分析结果和逻辑说明的文本报告。
        - 生成/更新 `股权关系社区结构.png` 和 `最终控制人网络图.png` 等可视化图片。

3.  **节点邻域查询 (`query_node_neighborhood.py`)**
    
    查询特定节点的N度邻域信息 (默认为2度)。
    ```bash
    python query_node_neighborhood.py "节点的确切名称"
    ```
    例如:
    ```bash
    python query_node_neighborhood.py "阿里巴巴（中国）网络技术有限公司"
    ```
    查询指定度数的邻域 (例如1度):
    ```bash
    python query_node_neighborhood.py "节点名称" --radius 1
    ```
    - 输出:
        - 控制台打印查询过程和总结。
        - 生成 `query_result_节点名称.txt` 包含该节点及其N度邻域内其他节点和关系的详细信息。
        - 生成 `query_result_节点名称.png` 可视化该邻域网络。

## 注意事项

- **中文字体**: 项目包含 `font_config.py` 以尝试自动配置中文字体。如果图表中的中文显示为方框，请确保您的系统中安装了常见的中文字体 (如SimHei, Microsoft YaHei等)，或者根据需要修改 `font_config.py` 中的字体列表。
- **性能**: 对于非常大的CSV文件和复杂的网络，图的生成、布局计算和分析可能需要较长时间和较多内存。
- **CSV编码**: 脚本会尝试多种常见中文编码。如果您的CSV文件使用非常特殊的编码，可能需要手动在 `graph_builder.py` 的 `pd.read_csv()` 部分指定。

## 未来可能的改进

- 增加更复杂的权重计算和边属性利用。
- 提供交互式可视化选项 (例如使用 Pyvis 或 Dash)。
- 优化超大图的处理性能。
- 增加更多高级网络分析算法。 