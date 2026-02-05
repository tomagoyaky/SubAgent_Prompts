import unittest
import tempfile
import os
import yaml
from config.workflow_config import WorkflowConfig

class TestWorkflowConfig(unittest.TestCase):
    def setUp(self):
        # 创建临时配置文件
        self.temp_config = {
            'meta': {
                'workflow_name': '测试工作流',
                'master_node_id': 'MASTER-001'
            },
            'global': {
                'process_control': {
                    'workflow_status': 'ready'
                }
            },
            'nodes': [
                {
                    'node_id': 'MASTER-001',
                    'name': '主节点',
                    'type': '自动节点'
                },
                {
                    'node_id': 'NODE-001',
                    'name': '测试节点',
                    'type': '自动节点'
                }
            ]
        }
        
        # 创建临时文件
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(self.temp_config, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        # 清理临时文件
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_config(self):
        """测试配置文件能够正确加载和解析"""
        config = WorkflowConfig(self.temp_file.name)
        
        # 测试元信息
        meta = config.get_meta()
        self.assertEqual(meta['workflow_name'], '测试工作流')
        self.assertEqual(meta['master_node_id'], 'MASTER-001')
        
        # 测试全局变量
        global_vars = config.get_global()
        self.assertIn('process_control', global_vars)
        self.assertEqual(global_vars['process_control']['workflow_status'], 'ready')
        
        # 测试节点信息
        nodes = config.get_nodes()
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0]['node_id'], 'MASTER-001')
        self.assertEqual(nodes[1]['node_id'], 'NODE-001')
    
    def test_get_node_by_id(self):
        """测试根据节点ID获取节点信息"""
        config = WorkflowConfig(self.temp_file.name)
        
        # 测试获取存在的节点
        master_node = config.get_node_by_id('MASTER-001')
        self.assertIsNotNone(master_node)
        self.assertEqual(master_node['node_id'], 'MASTER-001')
        self.assertEqual(master_node['name'], '主节点')
        
        # 测试获取不存在的节点
        non_existent_node = config.get_node_by_id('NON-EXISTENT')
        self.assertIsNone(non_existent_node)
    
    def test_get_master_node(self):
        """测试获取主节点信息"""
        config = WorkflowConfig(self.temp_file.name)
        
        master_node = config.get_master_node()
        self.assertIsNotNone(master_node)
        self.assertEqual(master_node['node_id'], 'MASTER-001')
    
    def test_file_not_found(self):
        """测试配置文件不存在时的错误处理"""
        non_existent_path = 'non_existent_file.yaml'
        with self.assertRaises(FileNotFoundError):
            WorkflowConfig(non_existent_path)

if __name__ == '__main__':
    unittest.main()
