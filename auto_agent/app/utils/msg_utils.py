"""
消息处理工具
用于处理与消息相关的功能
"""

import threading
import time
from typing import List, Dict, Any, Optional, Iterator

from app.utils.logger import global_logger as logger


def process_message(agent, user_input: str):
    """
    处理单个用户消息并显示响应

    参数:
        agent: 代理实例
        user_input: 用户输入文本
    """
    # 创建用于代理调用的消息
    messages = [
        {"role": "system", "content": "你是一个专业的助手"},
        {"role": "user", "content": user_input}
    ]
    
    try:
        logger.info(f"处理用户消息: {user_input[:50]}...")
        
        if not agent:
            print("Auto-Agent: 代理未初始化。")
            return
        
        # 检查 LLM 提供商是否支持流式响应
        streaming_supported = check_streaming_support(agent)
        
        logger.info(f"支持流式响应: {streaming_supported}")
        
        # 如果支持，始终尝试使用流式响应
        if streaming_supported and hasattr(agent, "stream"):
            logger.info("使用流式响应")
            handle_streaming_response(agent, messages)
        elif streaming_supported and hasattr(agent.model, "stream"):
            # 回退: 如果代理不支持流，使用直接模型流
            logger.info("使用直接模型流式响应")
            handle_direct_model_streaming(agent, messages)
        else:
            logger.info("使用非流式响应")
            handle_non_streaming_response(agent, messages)
    except Exception as e:
        logger.error(f"调用代理时出错: {e}")
        import traceback
        logger.error(f"堆栈跟踪: {traceback.format_exc()}")
        print("Auto-Agent: 处理您的请求时发生错误。")


def check_streaming_support(agent) -> bool:
    """
    检查 LLM 提供商是否支持流式响应

    参数:
        agent: 代理实例

    返回:
        是否支持流式响应
    """
    streaming_supported = True  # 默认支持
    if hasattr(agent, "model"):
        provider = agent.model
        if provider:
            logger.info(f"找到 LLM 提供商: {type(provider).__name__}")
            if hasattr(provider, "stream_mode"):
                logger.info(f"流模式: {provider.stream_mode}")
                streaming_supported = provider.stream_mode
            # 还要检查 LLM 实例本身是否有流能力
            elif hasattr(provider, "stream"):
                logger.info("LLM 实例有 stream 方法")
                streaming_supported = True
            else:
                logger.info("LLM 实例没有流能力")
                streaming_supported = False
    else:
        # 尝试从 kwargs 获取 LLM 提供商
        if hasattr(agent, "kwargs"):
            provider = agent.kwargs.get("llm_provider") or agent.kwargs.get("model")
            if provider:
                logger.info(f"从 kwargs 找到 LLM 提供商: {type(provider).__name__}")
                if hasattr(provider, "stream_mode"):
                    logger.info(f"流模式: {provider.stream_mode}")
                    streaming_supported = provider.stream_mode
                elif hasattr(provider, "stream"):
                    logger.info("LLM 实例有 stream 方法")
                    streaming_supported = True
                else:
                    logger.info("LLM 实例没有流能力")
                    streaming_supported = False
    return streaming_supported


def handle_streaming_response(agent, messages: list):
    """
    处理来自代理的流式响应

    参数:
        agent: 代理实例
        messages: 发送给代理的消息列表
    """
    print("\nAuto-Agent: ", end="", flush=True)
    full_response = []
    try:
        # 使用模型的 chat 方法进行流式响应
        if hasattr(agent, "model") and hasattr(agent.model, "chat"):
            logger.info("使用 model.chat() 方法进行流式响应")
            # 提取系统提示和用户消息
            system_prompt = ""
            user_input = ""
            
            for message in messages:
                if message.get("role") == "system":
                    system_prompt = message.get("content", "")
                elif message.get("role") == "user":
                    user_input = message.get("content", "")
            
            logger.info(f"提取的系统提示: {system_prompt[:50]}...")
            logger.info(f"提取的用户输入: {user_input[:50]}...")
            
            # 使用模型的 chat 方法进行流式响应
            result = agent.model.chat(user_input, system_prompt)
            
            # 检查结果是否可迭代（流式）
            if hasattr(result, "__iter__") and not isinstance(result, str):
                logger.info("聊天结果是流式迭代器，开始迭代")
                for i, chunk in enumerate(result):
                    if chunk:
                        logger.info(f"收到聊天块 {i}: {chunk[:50]}...")
                        print(chunk, end="", flush=True)
                        full_response.append(chunk)
                    else:
                        logger.info(f"聊天块 {i} 为空")
            else:
                # 非流式响应
                logger.info("聊天结果是非流式的")
                if result:
                    print(result)
                    full_response.append(result)
        else:
            # 回退: 使用非流式响应
            logger.info("模型没有 chat() 方法，使用非流式响应")
            handle_non_streaming_response(agent, messages)
            return
        
        print()  # 流式完成后的新行
        logger.info(f"流式完成，收到 {len(full_response)} 个块")
        if not full_response:
            print("未收到响应。")
    except Exception as e:
        logger.error(f"流式响应时出错: {e}")
        import traceback
        logger.error(f"堆栈跟踪: {traceback.format_exc()}")
        print("\nAuto-Agent: 流式处理时发生错误。")


def handle_direct_model_streaming(agent, messages: list):
    """
    当代理不支持流时，处理直接模型流

    参数:
        agent: 代理实例
        messages: 发送给代理的消息列表
    """
    print("\nAuto-Agent: ", end="", flush=True)
    full_response = []
    try:
        if hasattr(agent.model, "stream"):
            # 提取系统提示和用户消息
            system_prompt = ""
            user_input = ""
            
            for message in messages:
                if message.get("role") == "system":
                    system_prompt = message.get("content", "")
                elif message.get("role") == "user":
                    user_input = message.get("content", "")
            
            # 直接使用模型的 stream 方法
            for chunk in agent.model.stream(user_input, system_prompt):
                if chunk:
                    print(chunk, end="", flush=True)
                    full_response.append(chunk)
        print()  # 流式完成后的新行
        if not full_response:
            print("未收到响应。")
    except Exception as e:
        logger.error(f"直接模型流式处理时出错: {e}")
        print("\nAuto-Agent: 流式处理时发生错误。")


def handle_non_streaming_response(agent, messages: list):
    """
    处理来自代理的非流式响应

    参数:
        agent: 代理实例
        messages: 发送给代理的消息列表
    """
    try:
        logger.info("调用代理获取非流式响应")
        # 添加代理调用的超时以防止挂起
        import threading
        import time
        
        result = None
        error = None
        
        def invoke_agent():
            nonlocal result, error
            try:
                logger.info("开始代理调用")
                result = agent.invoke({"messages": messages})
                logger.info("代理调用完成")
            except Exception as e:
                nonlocal error
                error = e
                logger.error(f"代理调用时出错: {e}")
        
        # 在单独的线程中启动代理调用
        invoke_thread = threading.Thread(target=invoke_agent)
        invoke_thread.daemon = True
        invoke_thread.start()
        
        # 等待调用完成，带有超时
        timeout = 60  # 更复杂任务的 60 秒超时
        start_time = time.time()
        
        # 首先等待超时，检查是否花费太长时间
        while invoke_thread.is_alive() and time.time() - start_time < timeout:
            time.sleep(0.5)
        
        if invoke_thread.is_alive():
            # 只显示警告，不要中断任务
            logger.warning("代理调用花费的时间比预期长")
            print("\nAuto-Agent: 此任务花费的时间比预期长。请等待，我们仍在处理中...")
            # 继续等待任务完成
            while invoke_thread.is_alive():
                time.sleep(1)
        
        if error:
            raise error
        
        # 显示结果
        logger.info(f"从代理收到类型为 {type(result).__name__} 的结果")
        if result:
            # 处理不同的结果结构
            if isinstance(result, dict):
                logger.info(f"结果是字典，键为: {list(result.keys())}")
                if "content" in result:
                    print(f"\nAuto-Agent: {result['content']}")
                elif "messages" in result and isinstance(result["messages"], list):
                    logger.info(f"结果包含消息列表，包含 {len(result['messages'])} 项")
                    # 过滤并只显示助手消息 (AIMessage)
                    assistant_messages = []
                    
                    for i, msg in enumerate(result["messages"]):
                        logger.info(f"消息 {i} 类型: {type(msg).__name__}")
                        
                        # 检查这是否是 AIMessage (助手消息)
                        msg_type = type(msg).__name__
                        if msg_type == "AIMessage":
                            # 从 AIMessage 提取内容
                            if hasattr(msg, "content"):
                                content = msg.content
                                logger.info(f"找到 AIMessage，内容: {content[:50]}..." if content else "找到 AIMessage 但无内容")
                                if content:
                                    assistant_messages.append(content)
                            elif isinstance(msg, dict) and "content" in msg:
                                content = msg["content"]
                                logger.info(f"找到 AIMessage 字典，内容: {content[:50]}..." if content else "找到 AIMessage 字典但无内容")
                                if content:
                                    assistant_messages.append(content)
                    
                    # 只显示最后一个助手消息 (最相关的响应)
                    if assistant_messages:
                        last_response = assistant_messages[-1]
                        print(f"\nAuto-Agent: {last_response}")
                    else:
                        logger.info("结果中未找到助手消息")
                        print("\nAuto-Agent: 未收到响应。")
                elif "output" in result:
                    output = result["output"]
                    if isinstance(output, dict) and "content" in output:
                        print(f"\nAuto-Agent: {output['content']}")
                    elif isinstance(output, str):
                        print(f"\nAuto-Agent: {output}")
                else:
                    print(f"\nAuto-Agent: {result}")
            elif isinstance(result, str):
                print(f"\nAuto-Agent: {result}")
            else:
                print(f"\nAuto-Agent: {result}")
        else:
            print("\nAuto-Agent: 未收到响应。")
    except Exception as e:
        logger.error(f"处理非流式响应时出错: {e}")
        import traceback
        logger.error(f"堆栈跟踪: {traceback.format_exc()}")
        print("\nAuto-Agent: 处理您的请求时发生错误。")


def process_stream_chunk(chunk, full_response):
    """
    处理单个流块

    参数:
        chunk: 流块
        full_response: 累积完整响应的列表
    """
    logger.info(f"处理类型为 {type(chunk).__name__} 的块")
    
    if isinstance(chunk, dict):
        logger.info(f"块是字典，键为: {list(chunk.keys())}")
        # 检查不同的响应结构
        if "content" in chunk:
            # 直接内容
            content = chunk["content"]
            logger.info(f"找到 'content' 字段: {content[:50]}..." if content else "找到 'content' 字段但为空")
            if content:
                print(content, end="", flush=True)
                full_response.append(content)
                logger.info(f"添加内容到 full_response，现在长度: {len(full_response)}")
        elif "messages" in chunk and isinstance(chunk["messages"], list):
            # 消息列表
            logger.info(f"找到 'messages' 字段，包含 {len(chunk['messages'])} 项")
            for i, msg in enumerate(chunk["messages"]):
                logger.info(f"处理类型为 {type(msg).__name__} 的消息 {i}")
                if isinstance(msg, dict):
                    logger.info(f"消息 {i} 是字典，键为: {list(msg.keys())}")
                    if "content" in msg:
                        content = msg["content"]
                        logger.info(f"消息 {i} 有 'content' 字段: {content[:50]}..." if content else "消息 {i} 有 'content' 字段但为空")
                        if content:
                            print(content, end="", flush=True)
                            full_response.append(content)
                            logger.info(f"添加消息内容到 full_response，现在长度: {len(full_response)}")
                elif hasattr(msg, "content"):
                    # LangChain 消息对象
                    content = msg.content
                    logger.info(f"消息 {i} 有 'content' 属性: {content[:50]}..." if content else "消息 {i} 有 'content' 属性但为空")
                    if content:
                        print(content, end="", flush=True)
                        full_response.append(content)
                        logger.info(f"添加 LangChain 消息内容到 full_response，现在长度: {len(full_response)}")
        elif "output" in chunk:
            # 输出字段
            output = chunk["output"]
            logger.info(f"找到类型为 {type(output).__name__} 的 'output' 字段")
            if isinstance(output, dict) and "content" in output:
                content = output["content"]
                logger.info(f"输出有 'content' 字段: {content[:50]}..." if content else "输出有 'content' 字段但为空")
                if content:
                    print(content, end="", flush=True)
                    full_response.append(content)
                    logger.info(f"添加输出内容到 full_response，现在长度: {len(full_response)}")
            elif isinstance(output, str):
                logger.info(f"输出是字符串: {output[:50]}..." if output else "输出是字符串但为空")
                if output:
                    print(output, end="", flush=True)
                    full_response.append(output)
                    logger.info(f"添加输出字符串到 full_response，现在长度: {len(full_response)}")
        else:
            # 尝试在其他可能的字段中查找内容
            logger.info("未找到常见内容字段，尝试查找其他可能的内容字段")
            # 检查 'text' 字段
            if "text" in chunk:
                text = chunk["text"]
                logger.info(f"找到 'text' 字段: {text[:50]}..." if text else "找到 'text' 字段但为空")
                if text:
                    print(text, end="", flush=True)
                    full_response.append(text)
                    logger.info(f"添加文本到 full_response，现在长度: {len(full_response)}")
            # 检查 'response' 字段
            elif "response" in chunk:
                response = chunk["response"]
                logger.info(f"找到类型为 {type(response).__name__} 的 'response' 字段")
                if isinstance(response, str):
                    logger.info(f"响应是字符串: {response[:50]}..." if response else "响应是字符串但为空")
                    if response:
                        print(response, end="", flush=True)
                        full_response.append(response)
                        logger.info(f"添加响应字符串到 full_response，现在长度: {len(full_response)}")
                elif isinstance(response, dict) and "content" in response:
                    content = response["content"]
                    logger.info(f"响应有 'content' 字段: {content[:50]}..." if content else "响应有 'content' 字段但为空")
                    if content:
                        print(content, end="", flush=True)
                        full_response.append(content)
                        logger.info(f"添加响应内容到 full_response，现在长度: {len(full_response)}")
            else:
                logger.info("在块中未找到内容")
    elif isinstance(chunk, str):
        # 直接字符串块
        logger.info(f"块是字符串: {chunk[:50]}..." if chunk else "块是字符串但为空")
        if chunk:
            print(chunk, end="", flush=True)
            full_response.append(chunk)
            logger.info(f"添加字符串块到 full_response，现在长度: {len(full_response)}")
    elif hasattr(chunk, "content"):
        # LangChain 消息块
        content = chunk.content
        logger.info(f"块有 'content' 属性: {content[:50]}..." if content else "块有 'content' 属性但为空")
        if content:
            print(content, end="", flush=True)
            full_response.append(content)
            logger.info(f"添加 LangChain 内容到 full_response，现在长度: {len(full_response)}")
    else:
        logger.info(f"未处理的块类型: {type(chunk).__name__}")
        # 尝试转换为字符串
        try:
            chunk_str = str(chunk)
            logger.info(f"将块转换为字符串: {chunk_str[:50]}..." if chunk_str else "将块转换为字符串但为空")
            if chunk_str:
                print(chunk_str, end="", flush=True)
                full_response.append(chunk_str)
                logger.info(f"添加转换后的字符串到 full_response，现在长度: {len(full_response)}")
        except Exception as e:
            logger.error(f"转换块为字符串时出错: {e}")
