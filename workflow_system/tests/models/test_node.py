import unittest
from models.node import Node

class TestNode(unittest.TestCase):
    def setUp(self):
        # 创建测试节点数据
        self.node_data = {
            'node_id': 'TEST-NODE-001',
            'name': '测试节点',
            'description': '这是一个测试节点',
            'type': '自动节点',
            'input': [
                {
                    'rpc_source_service': 'SOURCE-001',
                    'rpc_request_path': '/path/to/input'
                }
            ],
            'output': [
                {
                    'rpc_target_service': 'TARGET-001',
                    'rpc_request_path': '/path/to/output'
                }
            ],
            'connections': {
                'conditions': [
                    {
                        'condition': 'global.process_control.workflow_status == "ready"',
                        'next_node': ['NEXT-NODE-001']
                    }
                ],
                'next_node': ['MASTER-001']
            },
            'system_prompt': '这是一个系统提示'
        }
        
        # 创建Node实例
        self.node = Node(self.node_data)
    
    def test_node_properties(self):
        """测试节点属性是否正确设置"""
        self.assertEqual(self.node.node_id, 'TEST-NODE-001')
        self.assertEqual(self.node.name, '测试节点')
        self.assertEqual(self.node.description, '这是一个测试节点')
        self.assertEqual(self.node.type, '自动节点')
        self.assertEqual(len(self.node.input), 1)
        self.assertEqual(len(self.node.output), 1)
        self.assertEqual(self.node.system_prompt, '这是一个系统提示')
    
    def test_get_conditions(self):
        """测试获取条件连接"""
        conditions = self.node.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertEqual(conditions[0]['condition'], 'global.process_control.workflow_status == "ready"')
        self.assertEqual(conditions[0]['next_node'], ['NEXT-NODE-001'])
    
    def test_get_next_nodes(self):
        """测试获取直接下一节点"""
        next_nodes = self.node.get_next_nodes()
        self.assertEqual(len(next_nodes), 1)
        self.assertEqual(next_nodes[0], 'MASTER-001')
    
    def test_is_auto(self):
        """测试判断是否为自动节点"""
        self.assertTrue(self.node.is_auto())
        self.assertFalse(self.node.is_manual())
    
    def test_is_manual(self):
        """测试判断是否为人工节点"""
        # 创建人工节点
        manual_node_data = self.node_data.copy()
        manual_node_data['type'] = '人工节点'
        manual_node = Node(manual_node_data)
        
        self.assertTrue(manual_node.is_manual())
        self.assertFalse(manual_node.is_auto())
    
    def test_default_values(self):
        """测试默认值"""
        # 创建只有必要字段的节点数据
        minimal_node_data = {
            'node_id': 'MINIMAL-NODE-001',
            'name': '最小节点'
        }
        minimal_node = Node(minimal_node_data)
        
        self.assertEqual(minimal_node.node_id, 'MINIMAL-NODE-001')
        self.assertEqual(minimal_node.name, '最小节点')
        self.assertEqual(minimal_node.description, None)
        self.assertEqual(minimal_node.type, None)
        self.assertEqual(len(minimal_node.input), 0)
        self.assertEqual(len(minimal_node.output), 0)
        self.assertEqual(len(minimal_node.get_conditions()), 0)
        self.assertEqual(len(minimal_node.get_next_nodes()), 0)
        self.assertEqual(minimal_node.system_prompt, '')

if __name__ == '__main__':
    unittest.main()
