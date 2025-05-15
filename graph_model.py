# -*- coding: utf-8 -*-
# import pandas as pd # No longer needed directly here
import networkx as nx
# import matplotlib.pyplot as plt # Removed
# import json # No longer needed directly here
# from matplotlib.font_manager import FontProperties # Removed

# 从新模块导入功能
# from font_config import get_font_properties # Removed, font config not needed
from graph_builder import build_graph

# 1. 设置字体 # Removed
# font = get_font_properties() # Removed

# 2. 构建图
print("正在从 graph_builder 构建图...")
G = build_graph() # Uses graph_builder to get the graph object
print("图构建完成。")

# 移除本地的 parse_children 函数，因为它已在 graph_builder 中
# 移除本地的图构建循环 for _, row in df.iterrows(): 因为它已在 graph_builder 中

# 检查图是否为空
if G.number_of_nodes() == 0:
    print("图为空。请检查CSV文件和 graph_builder.py 的日志输出。")
else:
    # 输出一些网络统计信息
    print(f"\n节点总数: {G.number_of_nodes()}")
    print(f"边总数: {G.number_of_edges()}")

    # 找出入度最高的前5个节点（被最多公司/个人持股的实体）
    if G.number_of_nodes() > 0:
        in_degrees = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)
        print("\n被持股最多的实体 (前5名):")
        for node, degree in in_degrees[:5]:
            node_name = G.nodes[node].get('name', str(node))
            # 检查节点是否存在于图中，以防万一
            if node not in G:
                print(f"- 节点ID {node} (在度数计算中出现，但无法在G.nodes中找到详细信息)")
                continue
            print(f"- {node_name}: 被{degree}个实体持股")

        # 找出出度最高的前5个节点（持有最多公司股份的股东）
        out_degrees = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)
        print("\n持股最多的股东 (前5名):")
        for node, degree in out_degrees[:5]:
            node_name = G.nodes[node].get('name', str(node))
            if node not in G:
                print(f"- 节点ID {node} (在度数计算中出现，但无法在G.nodes中找到详细信息)")
                continue
            print(f"- {node_name}: 持有{degree}个实体的股份")

# 移除所有 matplotlib 绘图相关的代码
# plt.figure(figsize=(20, 15))
# ... (所有 nx.draw_... 和 plt.savefig/show 代码块被移除) ...
# print("'股权关系网络图.png' 已保存。")
# plt.show()

print("\ngraph_model.py 执行完毕，已输出图的统计信息。") 