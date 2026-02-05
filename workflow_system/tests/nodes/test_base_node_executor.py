import unittest
from unittest.mock import Mock
from nodes.base_node_executor import BaseNodeExecutor

class TestBaseNodeExecutor(unittest.TestCase):
    def setUp(self):
        # 创建模拟节点
        self.mock_node = Mock()
        self.mock_node.node_id = 'TEST-NODE-001'
        self.mock_node.name = '测试节点'
        
        # 创建模拟全局变量
        self.mock_global_vars = Mock()
        self.mock_global_vars.get_rpc_config.return_value = {
            'rpc_data_format': 'markdown'
        }
        
        # 创建BaseNodeExecutor实例
        self.executor = BaseNodeExecutor(self.mock_node, self.mock_global_vars)
    
    def test_generate_rpc_response(self):
        """测试生成RPC响应结果"""
        content = '测试响应内容'
        response = self.executor.generate_rpc_response(content)
        
        self.assertEqual(response['node_id'], 'TEST-NODE-001')
        self.assertEqual(response['node_name'], '测试节点')
        self.assertEqual(response['response_content'], content)
        self.assertIn('timestamp', response)
        self.assertEqual(response['rpc_data_format'], 'markdown')
    
    def test_simulate_ai_processing(self):
        """测试模拟AI大模型处理过程"""
        prompt = '测试提示内容'
        result = self.executor.simulate_ai_processing(prompt)
        
        self.assertIn('模拟大模型回复', result)
        self.assertIn('测试提示内容', result)

if __name__ == '__main__':
    unittest.main()
