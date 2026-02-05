import unittest
from unittest.mock import Mock
from nodes.master_node_executor import MasterNodeExecutor

class TestMasterNodeExecutor(unittest.TestCase):
    def setUp(self):
        # 创建模拟节点
        self.mock_node = Mock()
        self.mock_node.node_id = 'MASTER-001'
        self.mock_node.name = '主节点'
        
        # 创建模拟全局变量
        self.mock_global_vars = Mock()
        self.mock_global_vars.get_workflow_status.return_value = 'ready'
        self.mock_global_vars.get_current_exec_node.return_value = ''
        self.mock_global_vars.get_next_exec_node.return_value = ''
        self.mock_global_vars.get_code_review_result.return_value = 'pass'
        self.mock_global_vars.get_unit_test_pass_rate.return_value = 95
        self.mock_global_vars.get_integration_test_result.return_value = 'pass'
        self.mock_global_vars.get_system_test_result.return_value = 'pass'
        self.mock_global_vars.has_remaining_bugs.return_value = False
        self.mock_global_vars.get_bug_fix_iteration.return_value = 0
        self.mock_global_vars.get_max_bug_fix_iteration.return_value = 3
        
        # 创建MasterNodeExecutor实例
        self.executor = MasterNodeExecutor(self.mock_node, self.mock_global_vars)
    
    def test_initial_execution(self):
        """测试初始状态下的执行"""
        # 模拟初始状态
        self.mock_global_vars.get_workflow_status.return_value = 'ready'
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证工作流状态被更新为executing
        self.mock_global_vars.set_workflow_status.assert_called_with('executing')
        # 验证下一个执行节点被设置为REQ-ANALYSIS-001
        self.mock_global_vars.set_next_exec_node.assert_called_with('REQ-ANALYSIS-001')
        # 验证响应内容
        self.assertIn('工作流启动', response['response_content'])
        self.assertIn('REQ-ANALYSIS-001', response['response_content'])
    
    def test_decision_after_req_analysis(self):
        """测试需求分析节点执行后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'REQ-ANALYSIS-001'
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证下一个执行节点被设置为PRD-DESIGN-002
        self.mock_global_vars.set_next_exec_node.assert_called_with('PRD-DESIGN-002')
        # 验证响应内容
        self.assertIn('调度下一个节点', response['response_content'])
        self.assertIn('PRD-DESIGN-002', response['response_content'])
    
    def test_decision_after_code_review_pass(self):
        """测试代码评审通过后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'DEV-CODE-REVIEW-006'
        self.mock_global_vars.get_code_review_result.return_value = 'pass'
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证下一个执行节点被设置为TEST-UNIT-007
        self.mock_global_vars.set_next_exec_node.assert_called_with('TEST-UNIT-007')
        # 验证响应内容
        self.assertIn('调度下一个节点', response['response_content'])
        self.assertIn('TEST-UNIT-007', response['response_content'])
    
    def test_decision_after_code_review_fail(self):
        """测试代码评审失败后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'DEV-CODE-REVIEW-006'
        self.mock_global_vars.get_code_review_result.return_value = 'fail'
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证下一个执行节点被设置为DEV-CODE-IMPLEMENT-005
        self.mock_global_vars.set_next_exec_node.assert_called_with('DEV-CODE-IMPLEMENT-005')
        # 验证响应内容
        self.assertIn('调度下一个节点', response['response_content'])
        self.assertIn('DEV-CODE-IMPLEMENT-005', response['response_content'])
    
    def test_decision_after_unit_test_pass(self):
        """测试单元测试通过后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'TEST-UNIT-007'
        self.mock_global_vars.get_unit_test_pass_rate.return_value = 98
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证下一个执行节点被设置为TEST-INTEGRATION-008
        self.mock_global_vars.set_next_exec_node.assert_called_with('TEST-INTEGRATION-008')
        # 验证响应内容
        self.assertIn('调度下一个节点', response['response_content'])
        self.assertIn('TEST-INTEGRATION-008', response['response_content'])
    
    def test_decision_after_unit_test_fail(self):
        """测试单元测试失败后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'TEST-UNIT-007'
        self.mock_global_vars.get_unit_test_pass_rate.return_value = 85
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证下一个执行节点被设置为DEV-CODE-IMPLEMENT-005
        self.mock_global_vars.set_next_exec_node.assert_called_with('DEV-CODE-IMPLEMENT-005')
        # 验证响应内容
        self.assertIn('调度下一个节点', response['response_content'])
        self.assertIn('DEV-CODE-IMPLEMENT-005', response['response_content'])
    
    def test_decision_after_manual_merge(self):
        """测试人工合并节点执行后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'MANUAL-MERGE-CODE-011'
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证工作流状态被更新为finished
        self.mock_global_vars.set_workflow_status.assert_called_with('finished')
        # 验证响应内容
        self.assertIn('工作流执行完成', response['response_content'])
    
    def test_decision_bug_fix_exceeds_limit(self):
        """测试Bug修复迭代次数超过上限后的调度决策"""
        # 模拟工作流状态
        self.mock_global_vars.get_workflow_status.return_value = 'executing'
        self.mock_global_vars.get_current_exec_node.return_value = 'BUG-FIX-ITERATION-010'
        self.mock_global_vars.get_bug_fix_iteration.return_value = 3
        self.mock_global_vars.get_max_bug_fix_iteration.return_value = 3
        
        # 执行主节点
        response = self.executor.execute()
        
        # 验证工作流状态被更新为terminated
        self.mock_global_vars.set_workflow_status.assert_called_with('terminated')
        # 验证响应内容
        self.assertIn('工作流终止', response['response_content'])
        self.assertIn('人工介入', response['response_content'])

if __name__ == '__main__':
    unittest.main()
