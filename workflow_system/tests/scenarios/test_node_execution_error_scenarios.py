import unittest
import sys
import os
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from workflow_system.workflow.engine import WorkflowEngine
from workflow_system.tests.scenarios.base_scenario_test import BaseScenarioTest

class TestDevelopmentProcessScenarios(BaseScenarioTest):
    @patch('workflow_system.workflow.engine.MasterNodeExecutor')
    @patch('workflow_system.workflow.engine.SubNodeExecutor')
    def test_normal_development_process(self, mock_sub_executor, mock_master_executor):
        """测试正常的开发流程场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 模拟MasterNodeExecutor
        mock_master_instance = Mock()
        # 模拟正常的开发流程调度
        mock_master_instance.execute.side_effect = [
            {'response_content': '调度下一个节点: REQ-ANALYSIS-001'},
            {'response_content': '调度下一个节点: PRD-DESIGN-002'},
            {'response_content': '调度下一个节点: ARCH-DESIGN-003'},
            {'response_content': '调度下一个节点: DEV-TASK-BREAK-004'},
            {'response_content': '调度下一个节点: DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-REVIEW-006'},
            {'response_content': '调度下一个节点: TEST-UNIT-007'},
            {'response_content': '调度下一个节点: TEST-INTEGRATION-008'},
            {'response_content': '调度下一个节点: TEST-SYSTEM-009'},
            {'response_content': '调度下一个节点: MANUAL-MERGE-CODE-011'},
            {'response_content': '工作流执行完成'}
        ]
        mock_master_executor.return_value = mock_master_instance
        
        # 模拟SubNodeExecutor
        mock_sub_instance = Mock()
        mock_sub_instance.execute.return_value = {'response_content': '节点执行完成'}
        mock_sub_executor.return_value = mock_sub_instance
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(workflow_path)
        
        # 模拟工作流状态变化
        def mock_get_workflow_status():
            # 检查主节点执行次数
            if mock_master_instance.execute.call_count >= 11:
                return 'finished'
            return 'executing'
        engine.global_vars.get_workflow_status = mock_get_workflow_status
        
        # 模拟流程控制变量
        engine.global_vars.get_current_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.get_next_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.set_workflow_status = lambda status: None
        engine.global_vars.set_current_exec_node = lambda node: None
        engine.global_vars.set_next_exec_node = lambda node: None
        
        # 运行工作流
        status = engine.run()
        
        # 验证工作流执行完成
        self.assertEqual(status, 'finished')
        # 验证主节点执行了多次
        self.assertGreater(mock_master_instance.execute.call_count, 5)
        # 验证子节点执行了多次
        self.assertGreater(mock_sub_instance.execute.call_count, 5)
    
    @patch('workflow_system.workflow.engine.MasterNodeExecutor')
    @patch('workflow_system.workflow.engine.SubNodeExecutor')
    def test_code_review_failure_process(self, mock_sub_executor, mock_master_executor):
        """测试代码评审失败的流程场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 模拟MasterNodeExecutor
        mock_master_instance = Mock()
        # 模拟代码评审失败的流程
        mock_master_instance.execute.side_effect = [
            {'response_content': '调度下一个节点: REQ-ANALYSIS-001'},
            {'response_content': '调度下一个节点: PRD-DESIGN-002'},
            {'response_content': '调度下一个节点: ARCH-DESIGN-003'},
            {'response_content': '调度下一个节点: DEV-TASK-BREAK-004'},
            {'response_content': '调度下一个节点: DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-REVIEW-006'},
            {'response_content': '代码评审失败，调度回 DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-REVIEW-006'},
            {'response_content': '调度下一个节点: TEST-UNIT-007'},
            {'response_content': '工作流执行完成'}
        ]
        mock_master_executor.return_value = mock_master_instance
        
        # 模拟SubNodeExecutor
        mock_sub_instance = Mock()
        mock_sub_instance.execute.return_value = {'response_content': '节点执行完成'}
        mock_sub_executor.return_value = mock_sub_instance
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(workflow_path)
        
        # 模拟工作流状态变化
        def mock_get_workflow_status():
            # 检查主节点执行次数
            if mock_master_instance.execute.call_count >= 11:
                return 'finished'
            return 'executing'
        engine.global_vars.get_workflow_status = mock_get_workflow_status
        
        # 模拟流程控制变量
        engine.global_vars.get_current_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.get_next_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.set_workflow_status = lambda status: None
        engine.global_vars.set_current_exec_node = lambda node: None
        engine.global_vars.set_next_exec_node = lambda node: None
        engine.global_vars.set_code_review_result = lambda result: None
        
        # 运行工作流
        status = engine.run()
        
        # 验证工作流执行完成
        self.assertEqual(status, 'finished')
        # 验证主节点执行了多次（包括评审失败后的重试）
        self.assertGreater(mock_master_instance.execute.call_count, 8)
    
    @patch('workflow_system.workflow.engine.MasterNodeExecutor')
    @patch('workflow_system.workflow.engine.SubNodeExecutor')
    def test_bug_fix_process(self, mock_sub_executor, mock_master_executor):
        """测试Bug修复流程场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 模拟MasterNodeExecutor
        mock_master_instance = Mock()
        # 模拟Bug修复的流程
        mock_master_instance.execute.side_effect = [
            {'response_content': '调度下一个节点: REQ-ANALYSIS-001'},
            {'response_content': '调度下一个节点: PRD-DESIGN-002'},
            {'response_content': '调度下一个节点: ARCH-DESIGN-003'},
            {'response_content': '调度下一个节点: DEV-TASK-BREAK-004'},
            {'response_content': '调度下一个节点: DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-REVIEW-006'},
            {'response_content': '调度下一个节点: TEST-UNIT-007'},
            {'response_content': '调度下一个节点: TEST-INTEGRATION-008'},
            {'response_content': '调度下一个节点: TEST-SYSTEM-009'},
            {'response_content': '发现Bug，调度下一个节点: BUG-FIX-ITERATION-010'},
            {'response_content': '调度下一个节点: BUG-FIX-ITERATION-010'},
            {'response_content': 'Bug修复完成，调度下一个节点: TEST-SYSTEM-009'},
            {'response_content': '调度下一个节点: MANUAL-MERGE-CODE-011'},
            {'response_content': '工作流执行完成'}
        ]
        mock_master_executor.return_value = mock_master_instance
        
        # 模拟SubNodeExecutor
        mock_sub_instance = Mock()
        mock_sub_instance.execute.return_value = {'response_content': '节点执行完成'}
        mock_sub_executor.return_value = mock_sub_instance
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(workflow_path)
        
        # 模拟工作流状态变化
        def mock_get_workflow_status():
            # 检查主节点执行次数
            if mock_master_instance.execute.call_count >= 11:
                return 'finished'
            return 'executing'
        engine.global_vars.get_workflow_status = mock_get_workflow_status
        
        # 模拟流程控制变量
        engine.global_vars.get_current_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.get_next_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.set_workflow_status = lambda status: None
        engine.global_vars.set_current_exec_node = lambda node: None
        engine.global_vars.set_next_exec_node = lambda node: None
        engine.global_vars.set_has_remaining_bugs = lambda has_bugs: None
        engine.global_vars.set_bug_fix_iteration = lambda iteration: None
        
        # 运行工作流
        status = engine.run()
        
        # 验证工作流执行完成
        self.assertEqual(status, 'finished')
        # 验证主节点执行了多次（包括Bug修复流程）
        self.assertGreater(mock_master_instance.execute.call_count, 10)
    
    @patch('workflow_system.workflow.engine.MasterNodeExecutor')
    @patch('workflow_system.workflow.engine.SubNodeExecutor')
    def test_manual_merge_process(self, mock_sub_executor, mock_master_executor):
        """测试人工合并代码流程场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 模拟MasterNodeExecutor
        mock_master_instance = Mock()
        # 模拟人工合并代码的流程
        mock_master_instance.execute.side_effect = [
            {'response_content': '调度下一个节点: REQ-ANALYSIS-001'},
            {'response_content': '调度下一个节点: PRD-DESIGN-002'},
            {'response_content': '调度下一个节点: ARCH-DESIGN-003'},
            {'response_content': '调度下一个节点: DEV-TASK-BREAK-004'},
            {'response_content': '调度下一个节点: DEV-CODE-IMPLEMENT-005'},
            {'response_content': '调度下一个节点: DEV-CODE-REVIEW-006'},
            {'response_content': '调度下一个节点: TEST-UNIT-007'},
            {'response_content': '调度下一个节点: TEST-INTEGRATION-008'},
            {'response_content': '调度下一个节点: TEST-SYSTEM-009'},
            {'response_content': '调度下一个节点: MANUAL-MERGE-CODE-011'},
            {'response_content': '工作流执行完成'}
        ]
        mock_master_executor.return_value = mock_master_instance
        
        # 模拟SubNodeExecutor
        mock_sub_instance = Mock()
        mock_sub_instance.execute.return_value = {'response_content': '节点执行完成'}
        mock_sub_executor.return_value = mock_sub_instance
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(workflow_path)
        
        # 模拟工作流状态变化
        def mock_get_workflow_status():
            # 检查主节点执行次数
            if mock_master_instance.execute.call_count >= 11:
                return 'finished'
            return 'executing'
        engine.global_vars.get_workflow_status = mock_get_workflow_status
        
        # 模拟流程控制变量
        engine.global_vars.get_current_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.get_next_exec_node = lambda: 'REQ-ANALYSIS-001'
        engine.global_vars.set_workflow_status = lambda status: None
        engine.global_vars.set_current_exec_node = lambda node: None
        engine.global_vars.set_next_exec_node = lambda node: None
        
        # 运行工作流
        status = engine.run()
        
        # 验证工作流执行完成
        self.assertEqual(status, 'finished')
        # 验证主节点执行了多次
        self.assertGreater(mock_master_instance.execute.call_count, 5)


if __name__ == '__main__':
    unittest.main()
