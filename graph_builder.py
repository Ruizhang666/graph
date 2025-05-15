# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import json

# 辅助函数，用于递归解析children字段并添加节点和边
def _parse_children_recursive(parent_node_id, children_data, graph):
    if isinstance(children_data, str):
        try:
            # 替换策略：
            # 1. 将 CSV 中的 \' (代表实际的单引号) 替换为特殊占位符
            # 2. 将结构性的 ' 替换为 "
            # 3. 将占位符替换回 JSON 字符串中合法的 '
            processed_str = children_data.replace("\\'", "__TEMP_SINGLE_QUOTE__") 
            processed_str = processed_str.replace("'", '"')
            processed_str = processed_str.replace("__TEMP_SINGLE_QUOTE__", "'") 
            children_list = json.loads(processed_str)
        except json.JSONDecodeError as e_json_primary:
            try:
                # 备用：简单替换，如果上面的方法因为复杂引号失败
                children_list = json.loads(children_data.replace("'", '"'))
            except json.JSONDecodeError as e_json_fallback:
                print(f"GraphBuilder Warn: Could not parse children JSON string '{children_data}' for parent '{parent_node_id}'. Primary error: {e_json_primary}. Fallback error: {e_json_fallback}")
                return
        except Exception as e_general:
            print(f"GraphBuilder Warn: Unknown error parsing children string '{children_data}' for parent '{parent_node_id}'. Error: {e_general}")
            return
    elif isinstance(children_data, list):
        children_list = children_data
    else:
        print(f"GraphBuilder Warn: Children data is not a string or list for parent '{parent_node_id}'. Type: {type(children_data)}")
        return

    for child_info in children_list:
        child_name = child_info.get('name')
        child_eid = child_info.get('eid')
        
        if not pd.notna(child_name) or child_name == '':
            # print(f"GraphBuilder Info: Skipping child with no name from children list of {parent_node_id}.")
            continue

        child_node_id = child_eid if pd.notna(child_eid) and child_eid != '' else child_name
        
        # 添加或更新子节点属性
        node_attrs = {
            'name': child_name,
            'type': child_info.get('type', ''),
            'short_name': child_info.get('short_name', ''),
            'level': child_info.get('level', '')
        }
        if not graph.has_node(child_node_id):
            graph.add_node(child_node_id, **node_attrs)
        else:
            # 如果节点已存在，用children中的信息补充或更新（如果更详细）
            for attr, value in node_attrs.items():
                 if value or not graph.nodes[child_node_id].get(attr): # 更新空值或使用新值
                    graph.nodes[child_node_id][attr] = value

        # 添加从父节点到子节点的边
        edge_attrs = {
            'amount': child_info.get('amount', ''),
            'percent': child_info.get('percent', ''),
            'sh_type': child_info.get('sh_type', '')
        }
        # 只有当边不存在时才从children添加，优先信任主行数据中通过parent_id建立的边
        if not graph.has_edge(parent_node_id, child_node_id):
            graph.add_edge(parent_node_id, child_node_id, **edge_attrs)

        # 递归处理孙子节点
        grand_children_data = child_info.get('children')
        if grand_children_data:
            _parse_children_recursive(child_node_id, grand_children_data, graph)

def build_graph(csv_path='三层股权穿透输出数据.csv'):
    """
    从指定的CSV文件读取股权数据并构建一个NetworkX DiGraph。
    """
    try:
        df = pd.read_csv(csv_path, encoding='gbk')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_path, encoding='gb18030')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(csv_path, encoding='gb2312')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(csv_path, encoding='big5')
                except UnicodeDecodeError:
                    print(f"GraphBuilder Error: Could not decode CSV file '{csv_path}' with common Chinese encodings.")
                    raise # 重新抛出异常，让调用者处理
    
    G = nx.DiGraph()

    # 第一遍：添加所有在主行中定义了name的节点，并建立基于parent_id的边
    for _, row in df.iterrows():
        if pd.notna(row['name']):
            current_node_id = row['eid'] if pd.notna(row['eid']) and row['eid'] != '' else row['name']
            
            node_attrs = {
                'name': row['name'],
                'type': row['type'] if pd.notna(row['type']) else '',
                'short_name': row['short_name'] if pd.notna(row['short_name']) else '',
                'level': row['level'] if pd.notna(row['level']) else ''
            }
            if not G.has_node(current_node_id):
                G.add_node(current_node_id, **node_attrs)
            else: # 如果节点已存在（可能从之前的children解析中添加），用主行数据更新
                for attr, value in node_attrs.items():
                    G.nodes[current_node_id][attr] = value # 主行数据优先

            parent_id_val = row.get('parent_id')
            if pd.notna(parent_id_val) and parent_id_val != '':
                # 如果父节点不存在，暂时不创建，期望它有自己的主行数据
                # if not G.has_node(parent_id_val):
                # G.add_node(parent_id_val, name=f"Deferred Parent ({parent_id_val})") # 占位符
                edge_attrs = {
                    'amount': row['amount'] if pd.notna(row['amount']) else '',
                    'percent': row['percent'] if pd.notna(row['percent']) else '',
                    'sh_type': row['sh_type'] if pd.notna(row['sh_type']) else ''
                }
                G.add_edge(parent_id_val, current_node_id, **edge_attrs)
    
    # 第二遍：处理children字段，补充可能的节点和边
    # 这样做可以确保主行定义的节点和边属性优先
    for _, row in df.iterrows():
        if pd.notna(row['name']):
            current_node_id = row['eid'] if pd.notna(row['eid']) and row['eid'] != '' else row['name']
            children_json_str = row.get('children')
            if pd.notna(children_json_str) and children_json_str not in [[], '[]', '']:
                 # 确保父节点（current_node_id）在图中，如果它只有children而没有parent_id，第一遍可能没覆盖到
                if not G.has_node(current_node_id):
                     G.add_node(current_node_id, name=row['name']) # 至少有个名字
                _parse_children_recursive(current_node_id, children_json_str, G)
                
    print(f"GraphBuilder: Built graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

if __name__ == '__main__':
    # 测试函数
    print("Testing graph builder...")
    graph = build_graph()
    # print("Graph nodes:")
    # for node, data in list(graph.nodes(data=True))[:5]:
    # print(f"  {node}: {data}")
    # print("Graph edges:")
    # for u, v, data in list(graph.edges(data=True))[:5]:
    # print(f"  {u} -> {v}: {data}")
    print(f"Test graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.") 