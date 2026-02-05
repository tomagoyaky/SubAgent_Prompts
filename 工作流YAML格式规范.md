# 工作流 YAML 格式规范（主节点中心化调度版）
## 1. 规范概述
本规范定义了**中心化调度式工作流**的 YAML 格式标准，核心特性包括：主节点（master_node）统一调度、RPC 协议交互、全局变量驱动流程决策、结构化输入输出、语义化节点标识，适用于各类软件开发、自动化流程等场景，兼容之前迭代的所有核心能力（条件判断、循环迭代、人工节点、文件持久化）。

## 2. 整体结构
工作流 YAML 包含 4 个核心顶级字段，层级清晰、职责分离：
```yaml
# 元信息：工作流基础标识
meta:
  # 子字段...

# 全局配置：全流程通用配置、变量、路径
global:
  # 子字段...

# 节点定义：主节点 + 子节点（自动/人工）
nodes:
  # 主节点定义
  - node_id: xxx
    # 子字段...
  # 子节点定义
  - node_id: xxx
    # 子字段...

# （可选）扩展配置：插件、监控、日志等
extensions:
  # 子字段...
```

## 3. 详细字段定义
### 3.1 元信息（meta）
工作流的基础标识信息，必填，用于唯一标识和描述工作流。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| workflow_name         | string  | 是   | 工作流名称，简洁明了                                                 | 通用软件开发标准工作流                |
| workflow_version      | string  | 是   | 工作流版本，遵循语义化版本（主版本.次版本.修订版）| 5.0.0                                 |
| workflow_description  | string  | 是   | 工作流详细描述，说明核心能力、适用场景                               | 基于RPC主节点调度的软件开发全流程工作流 |
| master_node_id        | string  | 是   | 主节点唯一标识，与nodes中主节点node_id一致                           | MASTER-MANAGE-000                     |
| manual_nodes          | list    | 否   | 人工节点ID列表，标识需要人工干预的节点                               | [MANUAL-MERGE-CODE-011]               |
| workflow_features     | list    | 否   | 工作流核心特性列表，便于快速识别能力                                 | [主节点RPC调度, 条件判断, 循环迭代]   |
| create_time           | string  | 否   | 工作流创建时间                                                       | 2026-02-05 10:00:00                   |
| update_time           | string  | 否   | 工作流最后更新时间                                                   | 2026-02-05 14:30:00                   |

### 3.2 全局配置（global）
全流程通用配置，分为 4 个子模块：项目基础信息、文件路径配置、RPC 协议配置、流程控制变量，必填。

#### 3.2.1 项目基础信息（project_info）
工作流所属项目的基础信息，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| project_name          | string  | 是   | 项目名称                                                             | 通用软件开发项目                      |
| project_env           | string  | 是   | 运行环境（开发/测试/生产）| 开发环境                              |
| project_code_repo     | string  | 否   | 项目代码仓库地址                                                     | https://github.com/xxx/project.git    |
| frontend_stack        | string  | 否   | 前端技术栈                                                           | Vue3 + TypeScript                     |
| backend_stack         | string  | 否   | 后端技术栈                                                           | SpringBoot + MySQL                    |

#### 3.2.2 文件路径配置（file_paths）
全流程文件持久化的相对路径，统一管理，避免路径混乱，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| original_req_path     | string  | 是   | 人类原始需求文档存储路径                                             | /docs/原始需求/                       |
| master_rpc_path       | string  | 是   | 主节点RPC调度指令、响应数据存储路径                                   | /rpc/master/                          |
| prd_save_path         | string  | 是   | 需求文档存储路径                                                     | /docs/需求文档/                       |
| design_save_path      | string  | 是   | 设计文档存储路径                                                     | /docs/设计文档/                       |
| arch_save_path        | string  | 是   | 架构文档存储路径                                                     | /docs/架构文档/                       |
| dev_task_path         | string  | 是   | 开发任务文档存储路径                                                 | /docs/开发任务/                       |
| code_dev_path         | string  | 是   | 代码说明、调试日志存储路径                                           | /code/                                |
| review_report_path    | string  | 是   | 评审报告存储路径                                                     | /docs/评审报告/                       |
| test_case_path        | string  | 是   | 测试用例存储路径                                                     | /docs/测试用例/                       |
| test_report_path      | string  | 是   | 测试报告存储路径                                                     | /docs/测试报告/                       |
| bug_record_path       | string  | 是   | Bug记录、关闭清单存储路径                                             | /docs/bug记录/                        |
| fix_report_path       | string  | 是   | Bug修复、回归测试报告存储路径                                         | /docs/修复报告/                       |

#### 3.2.3 RPC 协议配置（rpc_config）
主节点与子节点间 RPC 交互的通用配置，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| rpc_protocol          | string  | 是   | RPC 协议类型（RESTful/GRPC/HTTP）| RESTful RPC                           |
| rpc_timeout           | int     | 是   | RPC 请求超时时间，单位：毫秒                                           | 30000                                 |
| rpc_version           | string  | 是   | RPC 协议版本                                                         | 1.0.0                                 |
| rpc_data_format       | string  | 是   | RPC 交互数据格式，固定为 markdown                                     | markdown                              |

#### 3.2.4 流程控制变量（process_control）
驱动主节点智能调度的核心全局变量，必填，主节点基于这些变量动态决策下一步节点。

| 字段名                        | 类型    | 必填 | 说明                                                                 | 可选值/默认值                          |
|-------------------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| workflow_status               | string  | 是   | 工作流整体状态                                                       | ready（就绪）/executing（执行中）/finished（完成）/terminated（终止） |
| current_exec_node             | string  | 是   | 当前正在执行的子节点ID，主节点动态更新                               | 空字符串（初始）|
| next_exec_node                | string  | 是   | 下一个待执行的子节点ID，主节点动态决策                               | 空字符串（初始）|
| code_review_result            | string  | 是   | 代码评审结果                                                         | pending（待评审）/pass（通过）/fail（驳回） |
| unit_test_pass_threshold      | int     | 是   | 单元测试通过率阈值，百分比                                           | 95                                    |
| unit_test_actual_pass_rate    | int     | 是   | 单元测试实际通过率，主节点动态更新                                   | 0（初始）|
| integration_test_result       | string  | 是   | 集成测试结果                                                         | pending（待测试）/pass（通过）/fail（失败） |
| system_test_result            | string  | 是   | 系统测试结果                                                         | pending（待测试）/pass（通过）/fail（失败） |
| has_remaining_bugs            | bool    | 是   | 是否存在未修复的Bug，主节点动态更新                                   | false（初始）|
| current_bug_fix_iteration     | int     | 是   | Bug修复当前迭代次数，主节点动态更新                                   | 0（初始）|
| max_bug_fix_iteration         | int     | 是   | Bug修复最大迭代次数，超过则终止流程                                   | 3                                     |

### 3.3 节点定义（nodes）
工作流的核心执行单元，分为**主节点（master_node）** 和**子节点（auto 自动节点/manual 人工节点）**，必填，主节点唯一，子节点可扩展。

#### 3.3.1 节点通用基础字段
所有节点（主/子）均包含的基础字段，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 命名规范/示例                          |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| node_id               | string  | 是   | 节点唯一标识，语义化命名                                             | 主节点：MASTER-MANAGE-000；子节点：模块-功能-序号（如REQ-ANALYSIS-001） |
| name                  | string  | 是   | 节点名称，简洁描述功能                                               | 项目管理主节点（RPC调度中心）|
| description           | string  | 是   | 节点详细职责、功能描述                                               | 工作流RPC调度核心，下发任务、接收结果、动态决策 |
| type                  | string  | 是   | 节点类型                                                             | master（主节点）/auto（自动节点）/manual（人工节点） |

#### 3.3.2 节点输入（input）
节点执行所需的输入数据，遵循 RPC 交互规范，所有输入项均为列表，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| rpc_source_service    | string  | 是   | 输入数据的来源节点ID，人类输入固定为 HUMAN-INPUT                     | MASTER-MANAGE-000 / HUMAN-INPUT       |
| rpc_request_path      | string  | 是   | 输入数据的存储路径，引用global.file_paths中的路径                    | ${global.master_rpc_path}             |
| rpc_request_name      | string  | 是   | 输入数据的文件名，统一以.md结尾                                       | 子节点任务RPC执行指令.md              |
| rpc_data_format       | string  | 是   | 输入数据格式，固定引用global.rpc_config.rpc_data_format              | ${global.rpc_config.rpc_data_format}   |

#### 3.3.3 节点输出（output）
节点执行完成后的输出数据，遵循 RPC 交互规范，所有输出项均为列表，必填。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| rpc_content           | string  | 是   | 输出数据的内容描述                                                   | 标准化产品需求文档（PRD）|
| rpc_target_service    | string  | 是   | 输出数据的目标节点ID，子节点输出固定为 MASTER-MANAGE-000             | MASTER-MANAGE-000                     |
| rpc_request_path      | string  | 是   | 输出数据的存储路径，引用global.file_paths中的路径                    | ${global.prd_save_path}               |
| rpc_response_name     | string  | 是   | 输出数据的文件名，统一以.md结尾                                       | 标准化产品需求文档.md                 |
| rpc_data_format       | string  | 是   | 输出数据格式，固定引用global.rpc_config.rpc_data_format              | ${global.rpc_config.rpc_data_format}   |

#### 3.3.4 节点调度逻辑（connections）
定义节点执行完成后的流转规则，主节点和子节点的调度逻辑不同，必填。

##### （1）主节点调度逻辑
主节点基于`global.process_control`变量，通过`conditions`列表动态决策下一个节点，每个 condition 包含条件表达式和目标节点。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| conditions            | list    | 是   | 调度条件列表，按顺序匹配，匹配成功则执行对应next_node                 | - condition: "xxx" <br>  next_node: ["xxx"] |
| condition             | string  | 是   | 条件表达式，基于global.process_control变量，支持逻辑运算（&&/||）| "global.process_control.workflow_status == 'ready'" |
| next_node             | list    | 是   | 条件匹配成功后，下一个执行的节点ID列表（单节点调度为单个元素）| [REQ-ANALYSIS-001]                    |

##### （2）子节点调度逻辑
子节点仅负责执行任务，执行完成后**固定流转回主节点**，无需条件判断。

| 字段名                | 类型    | 必填 | 说明                                                                 | 示例                                  |
|-----------------------|---------|------|----------------------------------------------------------------------|---------------------------------------|
| next_node             | list    | 是   | 子节点执行完成后，固定返回主节点                                       | [MASTER-MANAGE-000]                   |

#### 3.3.5 节点系统提示（system_prompt）
节点的核心职责、执行要求、输出规范，以字符串形式定义，必填，指导节点执行具体任务。

### 3.4 扩展配置（extensions）
可选，用于扩展工作流能力，如插件集成、监控告警、日志配置等，可根据需求自定义。

## 4. 命名规范
### 4.1 节点ID命名
- 主节点：`MASTER-MODULE-序号`，如`MASTER-MANAGE-000`
- 子节点：`模块缩写-功能-序号`，模块缩写统一：
  - REQ（需求）、PRD（产品）、ARCH（架构）、DEV（开发）、TEST（测试）、BUG（Bug修复）、MANUAL（人工）
  - 示例：REQ-ANALYSIS-001、DEV-CODE-IMPLEMENT-005、TEST-SYSTEM-009

### 4.2 文件命名
- 所有交互文件统一以`.md`结尾，语义化命名，如`标准化产品需求文档.md`、`代码评审RPC响应结果.md`
- 调度指令文件：`xxxRPC调度指令.md`、`xxxRPC执行指令.md`
- 结果报告文件：`xxxRPC响应结果.md`、`xxx执行结果报告.md`

### 4.3 路径命名
- 按模块分层，以`/`结尾，如`/docs/需求文档/`、`/rpc/master/`
- 路径名称简洁，与模块功能一致，避免冗余

## 5. 完整示例（简化版）
```yaml
meta:
  workflow_name: 通用软件开发标准工作流
  workflow_version: 5.0.0
  workflow_description: 基于RPC主节点调度的软件开发全流程工作流
  master_node_id: MASTER-MANAGE-000
  manual_nodes: [MANUAL-MERGE-CODE-011]
  workflow_features: [主节点RPC调度, 条件判断, 循环迭代, 人工节点]
  create_time: 2026-02-05 10:00:00
  update_time: 2026-02-05 14:30:00

global:
  project_info:
    project_name: 通用软件开发项目
    project_env: 开发环境
    project_code_repo: https://github.com/xxx/project.git
    frontend_stack: Vue3 + TypeScript
    backend_stack: SpringBoot + MySQL

  file_paths:
    original_req_path: /docs/原始需求/
    master_rpc_path: /rpc/master/
    prd_save_path: /docs/需求文档/
    design_save_path: /docs/设计文档/
    arch_save_path: /docs/架构文档/
    dev_task_path: /docs/开发任务/
    code_dev_path: /code/
    review_report_path: /docs/评审报告/
    test_case_path: /docs/测试用例/
    test_report_path: /docs/测试报告/
    bug_record_path: /docs/bug记录/
    fix_report_path: /docs/修复报告/

  rpc_config:
    rpc_protocol: RESTful RPC
    rpc_timeout: 30000
    rpc_version: 1.0.0
    rpc_data_format: markdown

  process_control:
    workflow_status: ready
    current_exec_node: ""
    next_exec_node: ""
    code_review_result: pending
    unit_test_pass_threshold: 95
    unit_test_actual_pass_rate: 0
    integration_test_result: pending
    system_test_result: pending
    has_remaining_bugs: false
    current_bug_fix_iteration: 0
    max_bug_fix_iteration: 3

nodes:
  # 主节点
  - node_id: MASTER-MANAGE-000
    name: 项目管理主节点（RPC调度中心）
    description: 工作流RPC调度核心，下发任务、接收结果、动态决策
    type: master
    input:
      - rpc_source_service: HUMAN-INPUT
        rpc_request_path: ${global.original_req_path}
        rpc_request_name: 原始需求文档.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
      - rpc_source_service: REQ-ANALYSIS-001
        rpc_request_path: ${global.prd_save_path}
        rpc_response_name: 需求分析RPC响应结果.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    output:
      - rpc_content: 工作流启动RPC指令
        rpc_target_service: REQ-ANALYSIS-001
        rpc_request_path: ${global.master_rpc_path}
        rpc_request_name: 工作流启动RPC调度指令.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    connections:
      conditions:
        - condition: "global.process_control.workflow_status == 'ready'"
          next_node: [REQ-ANALYSIS-001]
        - condition: "global.process_control.current_exec_node == 'REQ-ANALYSIS-001'"
          next_node: [PRD-DESIGN-002]
    system_prompt: |
      你是项目管理主节点，负责RPC调度、结果解析、动态决策，按规则下发任务并更新全局变量。

  # 子节点：需求分析
  - node_id: REQ-ANALYSIS-001
    name: 需求接收与拆解（RPC执行节点）
    description: 接收主节点RPC指令，执行需求拆解，返回结果
    type: auto
    input:
      - rpc_source_service: MASTER-MANAGE-000
        rpc_request_path: ${global.master_rpc_path}
        rpc_request_name: 子节点任务RPC执行指令.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
      - rpc_source_service: HUMAN-INPUT
        rpc_request_path: ${global.original_req_path}
        rpc_request_name: 原始需求文档.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    output:
      - rpc_content: 标准化产品需求文档
        rpc_target_service: MASTER-MANAGE-000
        rpc_request_path: ${global.prd_save_path}
        rpc_response_name: 标准化产品需求文档.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
      - rpc_content: 需求分析RPC响应结果
        rpc_target_service: MASTER-MANAGE-000
        rpc_request_path: ${global.prd_save_path}
        rpc_response_name: 需求分析RPC响应结果.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    connections:
      next_node: [MASTER-MANAGE-000]
    system_prompt: |
      你是需求分析执行节点，按主节点RPC指令拆解需求，输出标准化文档并返回结果。

  # 子节点：人工合并代码
  - node_id: MANUAL-MERGE-CODE-011
    name: 人工合并代码（RPC人工节点）
    description: 接收主节点RPC指令，人工合并代码，返回结果
    type: manual
    input:
      - rpc_source_service: MASTER-MANAGE-000
        rpc_request_path: ${global.master_rpc_path}
        rpc_request_name: 子节点任务RPC执行指令.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
      - rpc_source_service: TEST-SYSTEM-009
        rpc_request_path: ${global.test_report_path}
        rpc_response_name: 系统测试RPC响应结果.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    output:
      - rpc_content: 代码合并完成记录
        rpc_target_service: MASTER-MANAGE-000
        rpc_request_path: ${global.code_dev_path}
        rpc_response_name: 代码合并完成记录.md
        rpc_data_format: ${global.rpc_config.rpc_data_format}
    connections:
      next_node: [MASTER-MANAGE-000]
    system_prompt: |
      你是人工合并节点，按主节点RPC指令合并代码，输出记录并返回结果。

extensions:
  monitor:
    enable: true
    alert_channel: 邮件+企业微信
  log:
    log_level: info
    log_path: /logs/workflow/
```

## 6. 规范使用说明
1. **主节点唯一性**：工作流中仅允许一个`type: master`的节点，作为唯一调度中心。
2. **子节点无决策**：所有子节点（auto/manual）仅执行任务，不参与流程决策，执行完成后固定返回主节点。
3. **RPC 字段必填**：所有节点的 input/output 必须遵循`rpc_`前缀规范，不得省略或修改字段名。
4. **全局变量驱动**：主节点的调度逻辑完全依赖`global.process_control`变量，子节点执行时需更新对应变量。
5. **扩展灵活**：可通过`extensions`字段集成监控、日志、插件等能力，无需修改核心结构。
6. **版本迭代**：修改工作流时，同步更新`meta.workflow_version`和`meta.update_time`，保证可追溯。