class GlobalVars:
    def __init__(self, global_data):
        self.global_data = global_data
        self.process_control = global_data.get('process_control', {})
        self.rpc_config = global_data.get('rpc_config', {})
    
    def get_process_control(self):
        """获取流程控制变量"""
        return self.process_control
    
    def get_rpc_config(self):
        """获取RPC配置"""
        return self.rpc_config
    
    def update_process_control(self, updates):
        """更新流程控制变量"""
        self.process_control.update(updates)
        return self.process_control
    
    def get_current_exec_node(self):
        """获取当前执行节点"""
        return self.process_control.get('current_exec_node', '')
    
    def set_current_exec_node(self, node_id):
        """设置当前执行节点"""
        self.process_control['current_exec_node'] = node_id
    
    def get_next_exec_node(self):
        """获取下一个执行节点"""
        return self.process_control.get('next_exec_node', '')
    
    def set_next_exec_node(self, node_id):
        """设置下一个执行节点"""
        self.process_control['next_exec_node'] = node_id
    
    def get_workflow_status(self):
        """获取工作流状态"""
        return self.process_control.get('workflow_status', 'ready')
    
    def set_workflow_status(self, status):
        """设置工作流状态"""
        self.process_control['workflow_status'] = status
    
    def get_code_review_result(self):
        """获取代码评审结果"""
        return self.process_control.get('code_review_result', 'pending')
    
    def set_code_review_result(self, result):
        """设置代码评审结果"""
        self.process_control['code_review_result'] = result
    
    def get_unit_test_pass_rate(self):
        """获取单元测试通过率"""
        return self.process_control.get('unit_test_actual_pass_rate', 0)
    
    def set_unit_test_pass_rate(self, rate):
        """设置单元测试通过率"""
        self.process_control['unit_test_actual_pass_rate'] = rate
    
    def get_integration_test_result(self):
        """获取集成测试结果"""
        return self.process_control.get('integration_test_result', 'pending')
    
    def set_integration_test_result(self, result):
        """设置集成测试结果"""
        self.process_control['integration_test_result'] = result
    
    def get_system_test_result(self):
        """获取系统测试结果"""
        return self.process_control.get('system_test_result', 'pending')
    
    def set_system_test_result(self, result):
        """设置系统测试结果"""
        self.process_control['system_test_result'] = result
    
    def has_remaining_bugs(self):
        """判断是否有未修复的Bug"""
        return self.process_control.get('has_remaining_bugs', False)
    
    def set_has_remaining_bugs(self, value):
        """设置是否有未修复的Bug"""
        self.process_control['has_remaining_bugs'] = value
    
    def get_bug_fix_iteration(self):
        """获取Bug修复迭代次数"""
        return self.process_control.get('current_bug_fix_iteration', 0)
    
    def set_bug_fix_iteration(self, iteration):
        """设置Bug修复迭代次数"""
        self.process_control['current_bug_fix_iteration'] = iteration
    
    def get_max_bug_fix_iteration(self):
        """获取Bug修复最大迭代次数"""
        return self.process_control.get('max_bug_fix_iteration', 3)
