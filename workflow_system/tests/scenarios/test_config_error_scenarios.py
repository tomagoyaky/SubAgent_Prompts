import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from workflow_system.config.workflow_config import WorkflowConfig
from workflow_system.workflow.engine import WorkflowEngine
from workflow_system.tests.scenarios.base_scenario_test import BaseScenarioTest

class TestDevelopmentScenarios(BaseScenarioTest):
    def test_workflow_initialization(self):
        """测试工作流初始化场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 创建WorkflowEngine实例
        engine = WorkflowEngine(workflow_path)
        
        # 验证工作流初始化成功
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.config)
        self.assertIsNotNone(engine.global_vars)
        
        # 验证主节点存在
        master_node = engine.config.get_master_node()
        self.assertIsNotNone(master_node)
        self.assertEqual(master_node['node_id'], 'MASTER-MANAGE-000')
        
        # 验证工作流状态
        self.assertEqual(engine.get_workflow_status(), 'ready')
    
    def test_all_nodes_exist(self):
        """测试所有节点都存在的场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 创建WorkflowConfig实例
        config = WorkflowConfig(workflow_path)
        
        # 验证所有必要的节点都存在
        required_nodes = [
            'MASTER-MANAGE-000',
            'REQ-ANALYSIS-001',
            'PRD-DESIGN-002',
            'ARCH-DESIGN-003',
            'DEV-TASK-BREAK-004',
            'DEV-CODE-IMPLEMENT-005',
            'DEV-CODE-REVIEW-006',
            'TEST-UNIT-007',
            'TEST-INTEGRATION-008',
            'TEST-SYSTEM-009',
            'BUG-FIX-ITERATION-010',
            'MANUAL-MERGE-CODE-011'
        ]
        
        for node_id in required_nodes:
            node = config.get_node_by_id(node_id)
            self.assertIsNotNone(node, f"节点 {node_id} 不存在")
            self.assertEqual(node['node_id'], node_id)
    
    def test_workflow_structure_integrity(self):
        """测试工作流结构完整性场景"""
        # 使用实际的工作流配置文件
        workflow_path = self.get_workflow_config_path()
        
        # 创建WorkflowConfig实例
        config = WorkflowConfig(workflow_path)
        
        # 验证元信息
        meta = config.get_meta()
        self.assertIn('workflow_name', meta)
        self.assertIn('master_node_id', meta)
        self.assertIn('workflow_features', meta)
        
        # 验证全局变量
        global_vars = config.get_global()
        self.assertIn('process_control', global_vars)
        self.assertIn('rpc_config', global_vars)
        
        # 验证流程控制变量
        process_control = global_vars['process_control']
        required_process_vars = [
            'current_exec_node',
            'next_exec_node',
            'code_review_result',
            'unit_test_actual_pass_rate',
            'integration_test_result',
            'system_test_result',
            'has_remaining_bugs',
            'current_bug_fix_iteration',
            'max_bug_fix_iteration',
            'workflow_status'
        ]
        
        for var in required_process_vars:
            self.assertIn(var, process_control)
        
        # 验证RPC配置
        rpc_config = global_vars['rpc_config']
        self.assertIn('rpc_timeout', rpc_config)
        self.assertIn('rpc_data_format', rpc_config)
        self.assertIn('rpc_version', rpc_config)


if __name__ == '__main__':
    unittest.main()
