import unittest
from unittest.mock import Mock, patch
import tempfile
import os
import yaml
from workflow.engine import WorkflowEngine

class TestWorkflowEngine(unittest.TestCase):
    def setUp(self):
        # 创建临时配置文件
        self.temp_config = {
            'meta': {
                'workflow_name': '测试工作流',
                'master_node_id': 'MASTER-001'
            },
            'global': {
                'process_control': {
                    'workflow_status': 'ready',
                    'current_exec_node': '',
                    'next_exec_node': ''
                },
                'rpc_config': {
                    'rpc_data_format': 'markdown'
                }
            },
            'nodes': [
                {
                    'node_id': 'MASTER-001',
                    'name': '主节点',
                    'type': '自动节点',
                    'input': [],
                    'output': [],
                    'connections': {},
                    'system_prompt': '主节点提示'
                },
                {
                    'node_id': 'REQ-ANALYSIS-001',
                    'name': '需求分析节点',
                    'type': '自动节点',
                    'input': [],
                    'output': [],
                    'connections': {
                        'next_node': ['MASTER-001']
                    },
                    'system_prompt': '需求分析提示'
                },
                {
                    'node_id': 'PRD-DESIGN-002',
                    'name': '产品设计节点',
                    'type': '自动节点',
                    'input': [],
                    'output': [],
                    'connections': {
                        'next_node': ['MASTER-001']
                    },
                    'system_prompt': '产品设计提示'
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
    
    def test_engine_initialization(self):
        """测试工作流引擎能够正确初始化"""
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(self.temp_file.name)
        
        # 验证主节点ID
        self.assertEqual(engine.master_node_id, 'MASTER-001')
        # 验证节点数量
        self.assertEqual(len(engine.nodes), 3)
        # 验证主节点存在
        self.assertIn('MASTER-001', engine.nodes)
        # 验证工作流状态
        self.assertEqual(engine.get_workflow_status(), 'ready')
    
    @patch('workflow.engine.MasterNodeExecutor')
    @patch('workflow.engine.SubNodeExecutor')
    def test_workflow_execution(self, mock_sub_executor, mock_master_executor):
        """测试工作流引擎能够正确执行工作流"""
        # 模拟MasterNodeExecutor
        mock_master_instance = Mock()
        # 初始执行返回调度REQ-ANALYSIS-001
        mock_master_instance.execute.side_effect = [
            {'response_content': '调度下一个节点: REQ-ANALYSIS-001'},
            {'response_content': '调度下一个节点: PRD-DESIGN-002'},
            {'response_content': '工作流执行完成'}
        ]
        mock_master_executor.return_value = mock_master_instance
        
        # 模拟SubNodeExecutor
        mock_sub_instance = Mock()
        mock_sub_instance.execute.return_value = {'response_content': '节点执行完成'}
        mock_sub_executor.return_value = mock_sub_instance
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(self.temp_file.name)
        
        # 模拟全局变量
        # 注意：这里我们需要修改engine.run方法的实现，或者在创建engine时就使用mock的global_vars
        # 为了简化测试，我们直接修改engine.global_vars的get_workflow_status方法
        original_get_workflow_status = engine.global_vars.get_workflow_status
        call_count = 0
        def mock_get_workflow_status():
            nonlocal call_count
            statuses = ['ready', 'executing', 'executing', 'finished']
            if call_count < len(statuses):
                result = statuses[call_count]
                call_count += 1
                return result
            return 'finished'
        engine.global_vars.get_workflow_status = mock_get_workflow_status
        
        # 模拟get_next_exec_node方法
        original_get_next_exec_node = engine.global_vars.get_next_exec_node
        next_node_call_count = 0
        def mock_get_next_exec_node():
            nonlocal next_node_call_count
            nodes = ['REQ-ANALYSIS-001', 'PRD-DESIGN-002', '']
            if next_node_call_count < len(nodes):
                result = nodes[next_node_call_count]
                next_node_call_count += 1
                return result
            return ''
        engine.global_vars.get_next_exec_node = mock_get_next_exec_node
        
        # 模拟get_current_exec_node方法
        engine.global_vars.get_current_exec_node = lambda: ''
        
        # 运行工作流
        status = engine.run()
        
        # 验证工作流状态
        self.assertEqual(status, 'finished')
        # 验证MasterNodeExecutor被调用
        self.assertEqual(mock_master_executor.call_count, 1)
        # 验证SubNodeExecutor被调用
        self.assertEqual(mock_sub_executor.call_count, 2)
        # 验证execute方法被调用的次数
        self.assertEqual(mock_master_instance.execute.call_count, 3)
        self.assertEqual(mock_sub_instance.execute.call_count, 2)

if __name__ == '__main__':
    unittest.main()
