import unittest
import os
from unittest.mock import Mock, patch

class BaseScenarioTest(unittest.TestCase):
    def setUp(self):
        # 使用工作流模板配置文件
        self.workflow_config_path = '/Users/neolix/Documents/trae_projects/SubAgentTest/workflow.template.yaml'
        # 验证配置文件存在
        self.assertTrue(os.path.exists(self.workflow_config_path), f"工作流配置文件不存在: {self.workflow_config_path}")
    
    def get_workflow_config_path(self):
        """获取工作流配置文件路径"""
        return self.workflow_config_path
    
    def create_mock_master_executor(self, side_effect=None):
        """创建模拟的主节点执行器"""
        mock_master = Mock()
        if side_effect:
            mock_master.execute.side_effect = side_effect
        else:
            mock_master.execute.return_value = {'response_content': '调度下一个节点: REQ-ANALYSIS-001'}
        return mock_master
    
    def create_mock_sub_executor(self, return_value=None):
        """创建模拟的子节点执行器"""
        mock_sub = Mock()
        if return_value:
            mock_sub.execute.return_value = return_value
        else:
            mock_sub.execute.return_value = {'response_content': '节点执行完成'}
        return mock_sub
    
    def simulate_workflow_status_changes(self, statuses):
        """模拟工作流状态变化"""
        call_count = 0
        def mock_get_workflow_status():
            nonlocal call_count
            if call_count < len(statuses):
                result = statuses[call_count]
                call_count += 1
                return result
            return statuses[-1]
        return mock_get_workflow_status
    
    def simulate_process_control_changes(self, process_control_values):
        """模拟流程控制变量变化"""
        call_count = 0
        def mock_get_process_control():
            nonlocal call_count
            if call_count < len(process_control_values):
                result = process_control_values[call_count]
                call_count += 1
                return result
            return process_control_values[-1]
        return mock_get_process_control
