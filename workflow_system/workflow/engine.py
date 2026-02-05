from workflow_system.config.workflow_config import WorkflowConfig
from workflow_system.models.node import Node
from workflow_system.models.global_vars import GlobalVars
from workflow_system.nodes.master_node_executor import MasterNodeExecutor
from workflow_system.nodes.sub_node_executor import SubNodeExecutor

class WorkflowEngine:
    def __init__(self, config_path):
        # 1. 加载配置
        self.config = WorkflowConfig(config_path)
        
        # 2. 初始化全局变量
        global_data = self.config.get_global()
        self.global_vars = GlobalVars(global_data)
        
        # 3. 初始化节点
        self.nodes = {}
        for node_data in self.config.get_nodes():
            node = Node(node_data)
            self.nodes[node.node_id] = node
        
        # 4. 获取主节点
        self.master_node_id = self.config.get_meta().get('master_node_id')
        self.master_node = self.nodes.get(self.master_node_id)
        
        print(f"工作流引擎初始化完成，主节点: {self.master_node_id}")
    
    def run(self):
        """运行工作流"""
        print("=== 工作流开始运行 ===")
        
        # 1. 主节点初始化工作流
        master_executor = MasterNodeExecutor(self.master_node, self.global_vars)
        master_executor.execute()
        
        # 2. 循环执行工作流，直到结束
        while self.global_vars.get_workflow_status() == 'executing':
            # 获取下一个执行节点
            next_node_id = self.global_vars.get_next_exec_node()
            if not next_node_id:
                print("无下一个执行节点，工作流结束")
                break
            
            # 设置当前执行节点
            self.global_vars.set_current_exec_node(next_node_id)
            
            # 执行子节点任务
            if next_node_id != self.master_node_id:
                node = self.nodes.get(next_node_id)
                if node:
                    executor = SubNodeExecutor(node, self.global_vars)
                    executor.execute()
                else:
                    print(f"节点 {next_node_id} 不存在")
                    break
            
            # 主节点决策下一个节点
            master_executor.execute()
        
        print("=== 工作流运行结束 ===")
        print(f"工作流状态: {self.global_vars.get_workflow_status()}")
        return self.global_vars.get_workflow_status()
    
    def get_workflow_status(self):
        """获取工作流状态"""
        return self.global_vars.get_workflow_status()
    
    def get_current_node(self):
        """获取当前执行节点"""
        current_node_id = self.global_vars.get_current_exec_node()
        return self.nodes.get(current_node_id)
    
    def get_next_node(self):
        """获取下一个执行节点"""
        next_node_id = self.global_vars.get_next_exec_node()
        return self.nodes.get(next_node_id)
