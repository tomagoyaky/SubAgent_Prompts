from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """LLM提供者的抽象基类"""
    
    @abstractmethod
    def generate(self, user_input, system_prompt=None, node_id=None):
        """根据用户输入、系统提示和节点ID生成回复
        
        Args:
            user_input (str): 用户输入
            system_prompt (str, optional): 系统提示
            node_id (str, optional): 节点ID
            
        Returns:
            str: LLM的回复
        """
        pass
