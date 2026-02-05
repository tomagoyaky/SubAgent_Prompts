from .provider import LLMProvider

class MockLLMProvider(LLMProvider):
    """模拟大模型回复的提供者"""
    
    def __init__(self):
        """初始化MockLLMProvider"""
        pass
    
    def generate(self, user_input, system_prompt=None, node_id=None):
        """根据用户输入、系统提示和节点ID生成回复
        
        Args:
            user_input (str): 用户输入
            system_prompt (str, optional): 系统提示
            node_id (str, optional): 节点ID
            
        Returns:
            str: 模拟的大模型回复
        """
        # 根据节点ID生成不同的回复
        if node_id:
            if node_id == 'REQ-ANALYSIS-001':
                return self._generate_req_analysis_response(user_input)
            elif node_id == 'PRD-DESIGN-002':
                return self._generate_prd_design_response(user_input)
            elif node_id == 'ARCH-DESIGN-003':
                return self._generate_arch_design_response(user_input)
            elif node_id == 'DEV-TASK-BREAK-004':
                return self._generate_task_break_response(user_input)
            elif node_id == 'DEV-CODE-IMPLEMENT-005':
                return self._generate_code_implement_response(user_input)
            elif node_id == 'DEV-CODE-REVIEW-006':
                return self._generate_code_review_response(user_input)
            elif node_id == 'TEST-UNIT-007':
                return self._generate_unit_test_response(user_input)
            elif node_id == 'TEST-INTEGRATION-008':
                return self._generate_integration_test_response(user_input)
            elif node_id == 'TEST-SYSTEM-009':
                return self._generate_system_test_response(user_input)
            elif node_id == 'BUG-FIX-ITERATION-010':
                return self._generate_bug_fix_response(user_input)
            elif node_id == 'MANUAL-MERGE-CODE-011':
                return self._generate_manual_merge_response(user_input)
            elif node_id == 'MASTER-MANAGE-000':
                return self._generate_master_response(user_input)
        
        # 默认回复
        return f"模拟大模型回复: {user_input[:50]}..."
    
    def _generate_req_analysis_response(self, prompt):
        """生成需求分析节点的回复"""
        return "需求分析完成，已生成标准化PRD文档，包含功能需求、非功能需求和验收标准。"
    
    def _generate_prd_design_response(self, prompt):
        """生成产品设计节点的回复"""
        return "产品设计完成，已生成产品原型和业务流程图，包含用户界面设计和交互流程。"
    
    def _generate_arch_design_response(self, prompt):
        """生成架构设计节点的回复"""
        return "架构设计完成，已生成技术架构方案，包含系统架构图、模块划分和技术选型。"
    
    def _generate_task_break_response(self, prompt):
        """生成任务拆解节点的回复"""
        return "任务拆解完成，已生成细粒度开发任务清单，包含任务优先级和排期计划。"
    
    def _generate_code_implement_response(self, prompt):
        """生成代码开发节点的回复"""
        return "代码开发完成，已实现所有功能模块，包含单元测试和集成测试。"
    
    def _generate_code_review_response(self, prompt):
        """生成代码评审节点的回复"""
        return "代码评审完成，发现了一些问题需要修改，主要是代码风格和性能优化方面的问题。"
    
    def _generate_unit_test_response(self, prompt):
        """生成单元测试节点的回复"""
        return "单元测试完成，测试通过率为95%，发现了一些边界情况的问题需要修复。"
    
    def _generate_integration_test_response(self, prompt):
        """生成集成测试节点的回复"""
        return "集成测试完成，测试结果通过，所有模块之间的交互正常。"
    
    def _generate_system_test_response(self, prompt):
        """生成系统测试节点的回复"""
        return "系统测试完成，发现了一些Bug需要修复，主要是功能和性能方面的问题。"
    
    def _generate_bug_fix_response(self, prompt):
        """生成Bug修复节点的回复"""
        return "Bug修复完成，已修复所有发现的Bug，包含回归测试验证。"
    
    def _generate_manual_merge_response(self, prompt):
        """生成人工合并节点的回复"""
        return "代码合并完成，已将开发分支合并到主分支，包含代码审查和冲突解决。"
    
    def _generate_master_response(self, prompt):
        """生成主节点的回复"""
        return "工作流调度完成，已根据当前状态决策下一个执行节点。"

# 为了向后兼容，保留MockLLM类
MockLLM = MockLLMProvider
