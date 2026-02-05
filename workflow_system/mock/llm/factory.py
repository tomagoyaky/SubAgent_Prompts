from .mock_llm_provider import MockLLMProvider
from .deepseek_provider import DeepSeekLLMProvider

class LLMProviderFactory:
    """LLM提供者工厂类"""
    
    @staticmethod
    def create(provider_type="mock", **kwargs):
        """创建LLM提供者实例
        
        Args:
            provider_type (str): 提供者类型，可选值: "mock", "deepseek"
            **kwargs: 传递给提供者构造函数的参数
            
        Returns:
            LLMProvider: LLM提供者实例
        """
        if provider_type == "deepseek":
            return DeepSeekLLMProvider(**kwargs)
        else:  # 默认使用mock
            return MockLLMProvider(**kwargs)
