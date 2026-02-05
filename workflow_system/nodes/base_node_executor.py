from workflow_system.mock.llm.factory import LLMProviderFactory

class BaseNodeExecutor:
    def __init__(self, node, global_vars):
        self.node = node
        self.global_vars = global_vars
        # 从全局变量中获取LLM提供者类型，默认使用mock
        llm_provider_type = global_vars.get_rpc_config().get('llm_provider', 'mock')
        # 从全局变量中获取LLM配置
        llm_config = global_vars.get_rpc_config().get('llm_config', {})
        # 确保llm_config是一个字典
        if not isinstance(llm_config, dict):
            llm_config = {}
        # 创建LLM提供者实例
        self.llm = LLMProviderFactory.create(llm_provider_type, **llm_config)
    
    def execute(self, input_data=None):
        """执行节点任务，返回执行结果"""
        raise NotImplementedError("子类必须实现execute方法")
    
    def generate_rpc_response(self, content):
        """生成RPC响应结果"""
        # 模拟生成RPC响应
        response = {
            'node_id': self.node.node_id,
            'node_name': self.node.name,
            'response_content': content,
            'timestamp': '2026-02-05T10:00:00Z',
            'rpc_data_format': self.global_vars.get_rpc_config().get('rpc_data_format', 'markdown')
        }
        return response
    
    def simulate_ai_processing(self, prompt):
        """模拟AI大模型处理过程"""
        # 使用MockLLM模拟AI大模型的处理过程
        print(f"[{self.node.name}] 正在处理: {prompt[:100]}...")
        # 模拟处理延迟
        import time
        time.sleep(0.1)  # 减少测试时间
        # 使用正确的参数顺序调用generate方法
        result = self.llm.generate(prompt, self.node.system_prompt, self.node.node_id)
        print(f"[{self.node.name}] 处理完成")
        return result
