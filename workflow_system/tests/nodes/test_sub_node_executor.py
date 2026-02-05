import unittest
from unittest.mock import Mock
from nodes.sub_node_executor import SubNodeExecutor

class TestSubNodeExecutor(unittest.TestCase):
    def setUp(self):
        # 创建模拟全局变量
        self.mock_global_vars = Mock()
        self.mock_global_vars.get_rpc_config.return_value = {
            'rpc_data_format': 'markdown'
        }
        
    def test_req_analysis_execution(self):
        """测试需求分析节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'REQ-ANALYSIS-001'
        mock_node.name = '需求分析节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('需求分析完成', response['response_content'])
        self.assertIn('标准化PRD', response['response_content'])
    
    def test_prd_design_execution(self):
        """测试产品设计节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'PRD-DESIGN-002'
        mock_node.name = '产品设计节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('产品设计完成', response['response_content'])
        self.assertIn('产品原型和业务流程', response['response_content'])
    
    def test_arch_design_execution(self):
        """测试架构设计节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'ARCH-DESIGN-003'
        mock_node.name = '架构设计节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('架构设计完成', response['response_content'])
        self.assertIn('技术架构方案', response['response_content'])
    
    def test_task_break_execution(self):
        """测试任务拆解节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'DEV-TASK-BREAK-004'
        mock_node.name = '任务拆解节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('任务拆解完成', response['response_content'])
        self.assertIn('开发任务清单', response['response_content'])
    
    def test_code_implement_execution(self):
        """测试代码开发节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'DEV-CODE-IMPLEMENT-005'
        mock_node.name = '代码开发节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('代码开发完成', response['response_content'])
        self.assertIn('模块开发代码', response['response_content'])
    
    def test_code_review_execution(self):
        """测试代码评审节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'DEV-CODE-REVIEW-006'
        mock_node.name = '代码评审节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证代码评审结果被设置
        self.mock_global_vars.set_code_review_result.assert_called()
        # 验证响应内容
        self.assertIn('代码评审完成', response['response_content'])
    
    def test_unit_test_execution(self):
        """测试单元测试节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'TEST-UNIT-007'
        mock_node.name = '单元测试节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证单元测试通过率被设置
        self.mock_global_vars.set_unit_test_pass_rate.assert_called()
        # 验证响应内容
        self.assertIn('单元测试完成', response['response_content'])
        self.assertIn('通过率', response['response_content'])
    
    def test_integration_test_execution(self):
        """测试集成测试节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'TEST-INTEGRATION-008'
        mock_node.name = '集成测试节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证集成测试结果被设置
        self.mock_global_vars.set_integration_test_result.assert_called()
        # 验证响应内容
        self.assertIn('集成测试完成', response['response_content'])
    
    def test_system_test_execution(self):
        """测试系统测试节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'TEST-SYSTEM-009'
        mock_node.name = '系统测试节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证系统测试结果和Bug状态被设置
        self.mock_global_vars.set_system_test_result.assert_called()
        self.mock_global_vars.set_has_remaining_bugs.assert_called()
        # 验证响应内容
        self.assertIn('系统测试完成', response['response_content'])
    
    def test_bug_fix_execution(self):
        """测试Bug修复节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'BUG-FIX-ITERATION-010'
        mock_node.name = 'Bug修复节点'
        
        # 模拟当前Bug修复迭代次数
        self.mock_global_vars.get_bug_fix_iteration.return_value = 0
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证Bug修复迭代次数和Bug状态被更新
        self.mock_global_vars.set_bug_fix_iteration.assert_called_with(1)
        self.mock_global_vars.set_has_remaining_bugs.assert_called()
        # 验证响应内容
        self.assertIn('Bug修复完成', response['response_content'])
        self.assertIn('迭代次数', response['response_content'])
    
    def test_manual_merge_execution(self):
        """测试人工合并节点的执行"""
        # 创建模拟节点
        mock_node = Mock()
        mock_node.node_id = 'MANUAL-MERGE-CODE-011'
        mock_node.name = '人工合并节点'
        
        # 创建SubNodeExecutor实例
        executor = SubNodeExecutor(mock_node, self.mock_global_vars)
        
        # 执行节点
        response = executor.execute()
        
        # 验证响应内容
        self.assertIn('代码合并完成', response['response_content'])
        self.assertIn('已合并到主分支', response['response_content'])

if __name__ == '__main__':
    unittest.main()
