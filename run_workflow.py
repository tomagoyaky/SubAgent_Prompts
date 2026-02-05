#!/usr/bin/env python3
"""
工作流运行脚本
"""

from workflow_system.workflow.engine import WorkflowEngine

if __name__ == "__main__":
    # 工作流配置文件路径
    workflow_config_path = "/Users/neolix/Documents/trae_projects/SubAgentTest/workflow.yaml"
    
    try:
        # 初始化工作流引擎
        engine = WorkflowEngine(workflow_config_path)
        
        # 运行工作流
        status = engine.run()
        
        print(f"工作流运行完成，状态: {status}")
    except Exception as e:
        print(f"工作流运行失败: {e}")
