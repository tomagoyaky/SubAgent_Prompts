import yaml
import os

class WorkflowConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """加载并解析workflow.yaml文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get_meta(self):
        """获取工作流元信息"""
        return self.config.get('meta', {})
    
    def get_global(self):
        """获取全局变量"""
        return self.config.get('global', {})
    
    def get_nodes(self):
        """获取所有节点信息"""
        return self.config.get('nodes', [])
    
    def get_node_by_id(self, node_id):
        """根据节点ID获取节点信息"""
        for node in self.get_nodes():
            if node.get('node_id') == node_id:
                return node
        return None
    
    def get_master_node(self):
        """获取主节点信息"""
        meta = self.get_meta()
        master_node_id = meta.get('master_node_id')
        if master_node_id:
            return self.get_node_by_id(master_node_id)
        return None
