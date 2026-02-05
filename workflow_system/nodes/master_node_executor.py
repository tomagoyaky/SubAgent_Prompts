from .base_node_executor import BaseNodeExecutor

class MasterNodeExecutor(BaseNodeExecutor):
    def execute(self, input_data=None):
        """执行主节点任务，进行工作流调度"""
        # 1. 初始化工作流
        if self.global_vars.get_workflow_status() == 'ready':
            self.global_vars.set_workflow_status('executing')
            # 初始状态：RPC下发指令给需求分析节点
            next_node = 'REQ-ANALYSIS-001'
            self.global_vars.set_next_exec_node(next_node)
            print(f"[主节点] 工作流启动，第一个执行节点: {next_node}")
            return self.generate_rpc_response(f"工作流启动，第一个执行节点: {next_node}")
        
        # 2. 根据当前执行节点和状态决策下一个节点
        current_node = self.global_vars.get_current_exec_node()
        print(f"[主节点] 处理当前节点: {current_node} 的执行结果")
        
        # 3. 基于条件决策下一个节点
        next_node = self._decide_next_node()
        
        if next_node:
            if next_node == '工作流结束':
                # 工作流结束
                self.global_vars.set_workflow_status('finished')
                print("[主节点] 工作流执行完成")
                return self.generate_rpc_response("工作流执行完成")
            elif next_node == '工作流终止（人工介入）':
                # 工作流终止
                self.global_vars.set_workflow_status('terminated')
                print("[主节点] 工作流终止，需要人工介入")
                return self.generate_rpc_response("工作流终止，需要人工介入")
            else:
                # 设置下一个执行节点
                self.global_vars.set_next_exec_node(next_node)
                print(f"[主节点] 调度下一个节点: {next_node}")
                return self.generate_rpc_response(f"调度下一个节点: {next_node}")
        
        return self.generate_rpc_response("无下一个执行节点")
    
    def _decide_next_node(self):
        """基于条件决策下一个节点"""
        current_node = self.global_vars.get_current_exec_node()
        workflow_status = self.global_vars.get_workflow_status()
        
        # 模拟主节点的决策逻辑
        if workflow_status == 'ready':
            return 'REQ-ANALYSIS-001'
        elif current_node == 'REQ-ANALYSIS-001':
            return 'PRD-DESIGN-002'
        elif current_node == 'PRD-DESIGN-002':
            return 'ARCH-DESIGN-003'
        elif current_node == 'ARCH-DESIGN-003':
            return 'DEV-TASK-BREAK-004'
        elif current_node == 'DEV-TASK-BREAK-004':
            return 'DEV-CODE-IMPLEMENT-005'
        elif current_node == 'DEV-CODE-IMPLEMENT-005':
            return 'DEV-CODE-REVIEW-006'
        elif current_node == 'DEV-CODE-REVIEW-006':
            # 根据代码评审结果决策
            if self.global_vars.get_code_review_result() == 'pass':
                return 'TEST-UNIT-007'
            else:
                return 'DEV-CODE-IMPLEMENT-005'
        elif current_node == 'TEST-UNIT-007':
            # 根据单元测试通过率决策
            if self.global_vars.get_unit_test_pass_rate() >= 95:
                return 'TEST-INTEGRATION-008'
            else:
                return 'DEV-CODE-IMPLEMENT-005'
        elif current_node == 'TEST-INTEGRATION-008':
            # 根据集成测试结果决策
            if self.global_vars.get_integration_test_result() == 'pass':
                return 'TEST-SYSTEM-009'
            else:
                return 'DEV-CODE-IMPLEMENT-005'
        elif current_node == 'TEST-SYSTEM-009':
            # 根据系统测试结果和Bug状态决策
            if self.global_vars.get_system_test_result() == 'pass' and not self.global_vars.has_remaining_bugs():
                return 'MANUAL-MERGE-CODE-011'
            else:
                return 'BUG-FIX-ITERATION-010'
        elif current_node == 'BUG-FIX-ITERATION-010':
            # 根据Bug修复迭代次数和状态决策
            if self.global_vars.get_bug_fix_iteration() >= self.global_vars.get_max_bug_fix_iteration():
                return '工作流终止（人工介入）'
            elif self.global_vars.has_remaining_bugs():
                return 'TEST-SYSTEM-009'
            else:
                return 'MANUAL-MERGE-CODE-011'
        elif current_node == 'MANUAL-MERGE-CODE-011':
            # 代码合并完成，工作流结束
            return '工作流结束'
        
        return None
