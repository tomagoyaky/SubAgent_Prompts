class Node:
    def __init__(self, node_data):
        self.node_id = node_data.get('node_id')
        self.name = node_data.get('name')
        self.description = node_data.get('description')
        self.type = node_data.get('type')
        self.input = node_data.get('input', [])
        self.output = node_data.get('output', [])
        self.connections = node_data.get('connections', {})
        self.system_prompt = node_data.get('system_prompt', '')
    
    def get_conditions(self):
        """获取节点的条件连接"""
        return self.connections.get('conditions', [])
    
    def get_next_nodes(self):
        """获取节点的直接下一节点"""
        return self.connections.get('next_node', [])
    
    def is_manual(self):
        """判断是否为人工节点"""
        return self.type == '人工节点'
    
    def is_auto(self):
        """判断是否为自动节点"""
        return self.type == '自动节点'
