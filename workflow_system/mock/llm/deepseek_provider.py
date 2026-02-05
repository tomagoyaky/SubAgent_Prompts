from .provider import LLMProvider
import requests
import json

class DeepSeekLLMProvider(LLMProvider):
    """DeepSeek大模型提供者"""
    
    def __init__(self, api_key=None, base_url="https://api.deepseek.com/v1/chat/completions"):
        """初始化DeepSeekLLMProvider
        
        Args:
            api_key (str, optional): DeepSeek API密钥
            base_url (str, optional): DeepSeek API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
    
    def generate(self, user_input, system_prompt=None, node_id=None):
        """根据用户输入、系统提示和节点ID生成回复
        
        Args:
            user_input (str): 用户输入
            system_prompt (str, optional): 系统提示
            node_id (str, optional): 节点ID
            
        Returns:
            str: DeepSeek大模型的回复
        """
        # 如果没有API密钥，返回模拟回复
        if not self.api_key:
            return f"DeepSeek API密钥未设置，返回模拟回复: {user_input[:50]}..."
        
        try:
            # 构建请求数据
            messages = []
            
            # 如果提供了系统提示，使用系统提示
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                # 否则使用默认的系统提示
                messages.append({
                    "role": "system",
                    "content": f"你是一个工作流节点的AI助手，节点ID: {node_id}。请根据输入提示生成专业的回复。"
                })
            
            # 添加用户输入
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"DeepSeek API请求失败: {response.status_code} - {response.text[:100]}..."
        
        except Exception as e:
            return f"DeepSeek API调用出错: {str(e)[:100]}..."
