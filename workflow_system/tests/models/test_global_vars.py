import unittest
from models.global_vars import GlobalVars

class TestGlobalVars(unittest.TestCase):
    def setUp(self):
        # 创建测试全局数据
        self.global_data = {
            'process_control': {
                'current_exec_node': 'NODE-001',
                'next_exec_node': 'NODE-002',
                'workflow_status': 'executing',
                'code_review_result': 'pass',
                'unit_test_actual_pass_rate': 95,
                'integration_test_result': 'pass',
                'system_test_result': 'pass',
                'has_remaining_bugs': False,
                'current_bug_fix_iteration': 0,
                'max_bug_fix_iteration': 3
            },
            'rpc_config': {
                'rpc_timeout': 30000,
                'rpc_data_format': 'markdown',
                'rpc_version': '1.0.0'
            }
        }
        
        # 创建GlobalVars实例
        self.global_vars = GlobalVars(self.global_data)
    
    def test_get_process_control(self):
        """测试获取流程控制变量"""
        process_control = self.global_vars.get_process_control()
        self.assertEqual(process_control['current_exec_node'], 'NODE-001')
        self.assertEqual(process_control['next_exec_node'], 'NODE-002')
        self.assertEqual(process_control['workflow_status'], 'executing')
    
    def test_get_rpc_config(self):
        """测试获取RPC配置"""
        rpc_config = self.global_vars.get_rpc_config()
        self.assertEqual(rpc_config['rpc_timeout'], 30000)
        self.assertEqual(rpc_config['rpc_data_format'], 'markdown')
        self.assertEqual(rpc_config['rpc_version'], '1.0.0')
    
    def test_update_process_control(self):
        """测试更新流程控制变量"""
        updates = {
            'current_exec_node': 'NODE-002',
            'workflow_status': 'finished'
        }
        updated_process_control = self.global_vars.update_process_control(updates)
        self.assertEqual(updated_process_control['current_exec_node'], 'NODE-002')
        self.assertEqual(updated_process_control['workflow_status'], 'finished')
        # 验证原始数据也被更新
        self.assertEqual(self.global_vars.get_process_control()['current_exec_node'], 'NODE-002')
    
    def test_current_exec_node(self):
        """测试获取和设置当前执行节点"""
        # 测试获取
        self.assertEqual(self.global_vars.get_current_exec_node(), 'NODE-001')
        
        # 测试设置
        self.global_vars.set_current_exec_node('NODE-003')
        self.assertEqual(self.global_vars.get_current_exec_node(), 'NODE-003')
    
    def test_next_exec_node(self):
        """测试获取和设置下一个执行节点"""
        # 测试获取
        self.assertEqual(self.global_vars.get_next_exec_node(), 'NODE-002')
        
        # 测试设置
        self.global_vars.set_next_exec_node('NODE-003')
        self.assertEqual(self.global_vars.get_next_exec_node(), 'NODE-003')
    
    def test_workflow_status(self):
        """测试获取和设置工作流状态"""
        # 测试获取
        self.assertEqual(self.global_vars.get_workflow_status(), 'executing')
        
        # 测试设置
        self.global_vars.set_workflow_status('finished')
        self.assertEqual(self.global_vars.get_workflow_status(), 'finished')
    
    def test_code_review_result(self):
        """测试获取和设置代码评审结果"""
        # 测试获取
        self.assertEqual(self.global_vars.get_code_review_result(), 'pass')
        
        # 测试设置
        self.global_vars.set_code_review_result('fail')
        self.assertEqual(self.global_vars.get_code_review_result(), 'fail')
    
    def test_unit_test_pass_rate(self):
        """测试获取和设置单元测试通过率"""
        # 测试获取
        self.assertEqual(self.global_vars.get_unit_test_pass_rate(), 95)
        
        # 测试设置
        self.global_vars.set_unit_test_pass_rate(98)
        self.assertEqual(self.global_vars.get_unit_test_pass_rate(), 98)
    
    def test_integration_test_result(self):
        """测试获取和设置集成测试结果"""
        # 测试获取
        self.assertEqual(self.global_vars.get_integration_test_result(), 'pass')
        
        # 测试设置
        self.global_vars.set_integration_test_result('fail')
        self.assertEqual(self.global_vars.get_integration_test_result(), 'fail')
    
    def test_system_test_result(self):
        """测试获取和设置系统测试结果"""
        # 测试获取
        self.assertEqual(self.global_vars.get_system_test_result(), 'pass')
        
        # 测试设置
        self.global_vars.set_system_test_result('fail')
        self.assertEqual(self.global_vars.get_system_test_result(), 'fail')
    
    def test_has_remaining_bugs(self):
        """测试获取和设置是否有未修复的Bug"""
        # 测试获取
        self.assertFalse(self.global_vars.has_remaining_bugs())
        
        # 测试设置
        self.global_vars.set_has_remaining_bugs(True)
        self.assertTrue(self.global_vars.has_remaining_bugs())
    
    def test_bug_fix_iteration(self):
        """测试获取和设置Bug修复迭代次数"""
        # 测试获取
        self.assertEqual(self.global_vars.get_bug_fix_iteration(), 0)
        
        # 测试设置
        self.global_vars.set_bug_fix_iteration(1)
        self.assertEqual(self.global_vars.get_bug_fix_iteration(), 1)
    
    def test_max_bug_fix_iteration(self):
        """测试获取Bug修复最大迭代次数"""
        self.assertEqual(self.global_vars.get_max_bug_fix_iteration(), 3)
    
    def test_default_values(self):
        """测试默认值"""
        # 创建只有部分数据的全局数据
        minimal_global_data = {
            'process_control': {
                'workflow_status': 'ready'
            }
        }
        minimal_global_vars = GlobalVars(minimal_global_data)
        
        # 测试获取不存在的流程控制变量
        self.assertEqual(minimal_global_vars.get_current_exec_node(), '')
        self.assertEqual(minimal_global_vars.get_next_exec_node(), '')
        self.assertEqual(minimal_global_vars.get_workflow_status(), 'ready')
        
        # 测试获取不存在的RPC配置
        self.assertEqual(len(minimal_global_vars.get_rpc_config()), 0)

if __name__ == '__main__':
    unittest.main()
