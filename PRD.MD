# 目标
一个由MasterAgent（项目管理角色）指挥多个Agent，去开发项目的系统。
MasterAgent作为人类代理，负责与项目团队的其他Agent成员角色协作，定制开发流程中的多种Agent角色。

# 人类偏好（你不要修改这个章节里的内容）
## shell脚本偏好
- 所有的 shell 脚本都需要按照下面的结构来编写
```bash
#!/bin/bash
# -----------------------------------------------------------------
# Author: username@company.ai
# Date: 2026-xx-xx
# Description: 
#   xxxxxxxxxxx
# -----------------------------------------------------------------

clear
set -e

################################################################################
## 变量定义
################################################################################
PROJECT_NAME="SubAgentTest"
FRONTEND_PORT=5600
BACKEND_PORT=8000

################################################################################
## 文件夹定义
################################################################################
DIR_PROJECT_ROOT=$(pwd)
DIR_CURRENT=${DIR_PROJECT_ROOT}
DIR_FRONTEND=${DIR_CURRENT}/${DIR_FRONTEND}
DIR_BACKEND=${DIR_CURRENT}/${DIR_BACKEND}
DIR_SPEC=${DIR_CURRENT}/spec
DIR_DOCS=${DIR_CURRENT}/docs
DIR_WORKSPACE=${DIR_CURRENT}/workspace

################################################################################
## 文件定义
################################################################################
FILE_START_SH="start.sh"
FILE_PROJECT_DB="project.db"

################################################################################
## 日志相关
################################################################################
# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志级别
LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARN=2
LOG_LEVEL_ERROR=3

# 当前日志级别设置为INFO
CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG
LOG_TAG="${PROJECT_NAME}-Logger"

# 日志函数
log_debug() {
    if [ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_DEBUG ]; then
        echo -e "${CYAN}[DEBUG]$(date '+%Y-%m-%d %H:%M:%S') [$LOG_TAG] $1${NC}"
    fi
}

log_info() {
    if [ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_INFO ]; then
        echo -e "${GREEN}[INFO]$(date '+%Y-%m-%d %H:%M:%S') [$LOG_TAG] $1${NC}"
    fi
}

log_warn() {
    if [ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_WARN ]; then
        echo -e "${YELLOW}[WARN]$(date '+%Y-%m-%d %H:%M:%S') [$LOG_TAG] $1${NC}"
    fi
}

log_error() {
    if [ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_ERROR ]; then
        echo -e "${RED}[ERROR]$(date '+%Y-%m-%d %H:%M:%S') [$LOG_TAG] $1${NC}"
    fi
    exit -1
}

log_critical() {
    if [ $CURRENT_LOG_LEVEL -le $LOG_LEVEL_ERROR ]; then
        echo -e "${RED}[CRITICAL]$(date '+%Y-%m-%d %H:%M:%S') [$LOG_TAG] $1${NC}"
    fi
}

# shell脚本开场打印
log_start() {
    title=$1
    log_info "==========================================================="
    log_info "| $title "
    log_info "| - $(date '+%Y-%m-%d %H:%M:%S')"
    log_info "| - Host: $(hostname)"
    log_info "| - User: $(whoami)" 
    log_info "| - Uname: $(uname -a)" 
    log_info "| - LogTag: $LOG_TAG" 
    log_info "| - CurrentLogLevel: $CURRENT_LOG_LEVEL" 
    log_info "==========================================================="
}

# shell方法调用指定顺序序号和标题
log_function_index_title() {
    index=$1
    title=$2
    log_info "==========================================================="
    log_info "| ($index) $title "
    log_info "==========================================================="
}

################################################################################
## 常用方法
################################################################################
# 函数定义
cmd() {
    cmd=$1
    log_debug "执行命令：$cmd"
    eval $cmd
}

cmd_with_bash() {
    cmd=$1
    log_debug "执行命令：bash -c '$cmd'"
    $(which bash) -c "$cmd"
}

safe_delete() {
    path=$1
    # 判断是文件还是文件夹
    if [ ! -e "$path" ]; then
        log_warn "$path 不存在，跳过删除。"
        return
    fi
    # 跟我进行交互，只有我确认删除，才删除
    while true; do
        read -p "确定要删除 $path 吗？(y/n) " yn
        case $yn in
            [Yy]* ) 
                cmd "rm -rf $path"
                break;;
            [Nn]* ) exit;;
            * ) echo "请输入 y 或 n.";;
        esac
    done
}

kill_port() {
    port=$1
    # lsof -i :5175 | awk 'NR>=2 {print $2}' | xargs kill -9
    PID=$(lsof -i :$port | awk 'NR>=2 {print $2}')
    if [ -n "$PID" ]; then
        log_info "清理已存在进程占用端口${port},PID: ${PID}"
        kill -9 $PID > /dev/null
        log_info "进程${PID}已终止"
    else
        log_info "端口${port}未被占用"
    fi
}

kill_process() {
    process_name=$1
    # ps aux | grep node | grep -v grep | awk 'NR>=2 {print $2}' | xargs sudo kill -9
    # ps aux | grep npm | grep -v grep | awk 'NR>=2 {print $2}' | xargs sudo kill -9
    PID=$(ps aux | grep "$process_name" | grep -v grep | awk 'NR>=2 {print $2}')
    if [ -n "$PID" ]; then
        log_info "已存在进程 $process_name, PID: $PID"
        log_info "尝试终止进程..."
        kill -9 $PID > /dev/null 2>&1
        log_info "进程 $PID 已终止"
    else
        log_info "进程 $process_name 未被占用"
    fi
}
```
## Agent偏好
- 所有具备代码编写能力的 Agent（如开发、测试等） 都需要强制先 Agent 调用 context7 获取对应的代码、框架的使用规范。
    - 使用context7，来杜绝AI编程助手因知识过时而生成错误或陈旧的代码，学习和使用新库，避免被过时的教程或博文误导。
    - 使用context7，来让AI能基于项目最新的官方文档来生成答案，确保代码的即时准确性。
    - 使用context7，最终让你无需手动查阅资料，在编辑器内就能高效获得可靠的编码帮助。
- 每个Agent必须按照要求，编写交付物到指定目录下的文件中，禁止生成交付物以外的文件。
- 每个Agent必须要检查自己的输入物是否存在，负责提示用户输入物不存在，并停止执行。
## 产品偏好
- 前后端分离架构

## 架构偏好
- 项目文件系统结构
    - 前端项目文件系统结构
        - <project_name>
            - frontend/
                - src/
                    - components/
                    - pages/
                    - utils/
                    - App.tsx
                    - index.html
                    - main.tsx
                    - styles.css
                - tsconfig.json
                - dist/
                - public/
                - styles/
                - scripts/
                    - build.sh
                    - dev.sh
    - 后端项目文件系统结构
        - <project_name>
            - backend/
                - src/
                    - app.js
                    - config/
                    - controllers/
                    - models/
                    - routes/
                    - utils/
                - package.json
                - .env.example
                - .env
                - scripts/
                    - build.sh
                    - dev.sh
    - 根目录
        - <project_name>
            - spec/         # 规范目录
            - docs/         # 文档目录
            - frontend/     # 前端项目目录
            - backend/      # 后端项目目录
            - workspace/     # 工作空间目录
                - logs/      # 日志目录
                - status/    # 项目状态目录
                - temp/      # 临时目录
                - db/         # 数据库目录
            - .gitignore     # Git 忽略文件
            - README.md      # 项目介绍文档
            - start.sh       # 启动脚本(支持独立和全部启动前后端项目)
- 启动脚本偏好
    - 独立启动：`./start.sh --frontend` 或 `./start.sh --backend`
    - 全部启动：`./start.sh`
    - 如果是 Python 项目，需要在 backend 目录下创建虚拟 Python 环境并激活：
        - `python -m venv venv`
        - `source venv/bin/activate` (Linux/Mac) 或 `venv\Scripts\activate` (Windows)
    - 如果是 Python 项目，需要安装依赖，但是不要重复安装，仅当依赖配置文件的 hash 值发生变化时才更新安装。
    - 如果是 Node.js 项目，需要安装依赖，但是不要重复安装，仅当依赖配置文件的 hash 值发生变化时才更新安装。
    - 启动前后端项目之前先执行 build 操作，确保编译无误。
    - 启动前后端项目使用 nohup 命令，确保项目在后台运行，不被终端关闭而中断。
    - 启动前端项目时，使用端口要在 5600到 5999 之间
    - 启动后端项目时，使用端口要在 8000到 8999 之间
    - 启动前后端项目时，需要清理历史端口占用。

## 前端偏好
- React + TypeScript + Vite + Shadcn-UI
- 自动化创建避免跟人类进行交互
- 具备路由功能（如 React Router）
- 具备状态管理功能（如 Redux Toolkit）
- 具备 UI 组件库（如 Shadcn-UI）
- 具备表单验证功能（如 Formik）
- 具备响应式设计（如 Tailwind CSS）
- 具备图表功能（如 Chart.js）
- 具备权限管理功能（如 React-Auth0）
- 具备国际化功能（如 i18next）
- UI 设计方面：
    - 左侧侧边栏菜单（多级菜单，最多支持到2级）
    - 顶部导航栏（包含项目名称、用户头像、通知图标等）
    - 子页面内容区域（根据路由显示不同的页面内容）
    - 子页面顶部面包屑导航栏
    - 子页面支持三种布局方式
        - 单区域布局
        - 左右布局（列表在左，详情在右）
        - 左中右布局（列表在左，内容在中，详情在右；常用语文档、聊天等场景）
    - 底部固定footer（作为状态栏，全局暴露更新状态的方法）
    - 列表组件（支持分页、搜索、筛选等功能）
    - 登录页面，包含用户名、密码输入框、登录按钮、忘记密码链接等
    - 注册页面，包含用户名、密码、确认密码输入框、注册按钮等

## 后端偏好
- Node.js + Express.js
- 数据库（开发环境：SQlite，生产环境：MySQL、MongoDB、PostgreSQL任意一个，按顺序优先级）
- 具备 RESTful API 设计（如 JSON:API）
- 具备 API 文档（如 Swagger）

# MasterAgent的提示词
你现在是项目管理员，准从《spec/项目开发流程规范.md》和《spec/Git开发规范.md》，按照产品->架构师->后端开发工程师->前端开发工程师->测试工程师->运维工程师->运营专家的顺序，指挥多个 Agent 去开发项目。

# 生成标准规范
- 生成《spec/项目开发流程规范.md》
> <你需要解释一下文档的内容、章节>
- 生成《spec/Git开发规范.md》
> <你需要解释一下文档的内容、章节>
- 生成《spec/Agent/Agent上下文提示词规范.md》
> <你需要解释一下文档的内容、章节>

# 生成Agent角色提示词
#### 输入物
- 使用《spec/Agent/Agent上下文提示词规范.md》
#### 交付物
- 生成《roles/产品专家.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/架构师.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/前端开发工程师.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/后端开发工程师.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/测试工程师.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/运维工程师.md》
> <你需要解释一下文档的内容、章节>
- 生成《roles/运营专家.md》
> <你需要解释一下文档的内容、章节>


# 全局工具、MCP、SKILLs
## 工具
- WebSearchTool
> <你需要解释一下文档的内容、章节>
- FileTool
> <你需要解释一下文档的内容、章节>
- DockerTool
> <你需要解释一下文档的内容、章节>
- GitTool
> <你需要解释一下文档的内容、章节>
## MCP服务
- context7
> <你需要解释一下文档的内容、章节>
## SKILLs
- architect-skill
> <你需要解释一下文档的内容、章节>
- backend-engineer-skill
> <你需要解释一下文档的内容、章节>
- frontend-engineer-skill
> <你需要解释一下文档的内容、章节>
- test-engineer-skill
> <你需要解释一下文档的内容、章节>
- devops-engineer-skill
> <你需要解释一下文档的内容、章节>
- product-manager-skill
> <你需要解释一下文档的内容、章节>
- devops-engineer-skill
> <你需要解释一下文档的内容、章节>

## 重要要求
### 产品专家
#### 交付物
- 必须生成《spec/产品设计/产品需求规格说明书.md》
> <你需要解释一下文档的内容、章节>

### 架构师
#### 输入物
- 使用《spec/产品设计/产品需求规格说明书.md》
#### 交付物
- 必须生成《spec/架构设计/架构设计文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/架构设计/项目文件系统结构.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/架构设计/技术栈配置文档.md》
> <你需要解释一下文档的内容、章节>

### 后端开发工程师
#### 输入物
- 使用《spec/产品设计/产品需求规格说明书.md》
- 使用《spec/架构设计/架构设计文档.md》
- 使用《spec/架构设计/项目文件系统结构.md》
- 使用《spec/架构设计/技术栈配置文档.md》
#### 交付物
- 必须生成《spec/后端开发/后端代码规范.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/后端开发/后端路由配置文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/后端开发/后端数据库设计文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/后端开发/后端接口文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/后端单元测试报告.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/后端项目配置表.md》（定义如何访问后端服务）
> <你需要解释一下文档的内容、章节>
- 交付后端项目代码

### 前端开发工程师
#### 输入物
- 使用《spec/产品设计/产品需求规格说明书.md》
- 使用《spec/架构设计/架构设计文档.md》
- 使用《spec/架构设计/项目文件系统结构.md》
- 使用《spec/架构设计/技术栈配置文档.md》
- 使用《spec/后端开发/后端接口文档.md》
#### 交付物
- 必须生成《spec/前端开发/前端代码规范.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/前端组件库文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/前端路由配置文档.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/前端单元测试报告.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/前端开发/前端项目配置表.md》（定义如何访问前端服务）
> <你需要解释一下文档的内容、章节>
- 交付前端项目代码

### 测试工程师
#### 输入物
- 使用《spec/后端开发/后端代码规范.md》
- 使用《spec/后端开发/后端路由配置文档.md》
- 使用《spec/后端开发/后端数据库设计文档.md》
- 使用《spec/后端开发/后端接口文档.md》
- 使用《spec/前端开发/后端单元测试报告.md》
- 使用《spec/前端开发/后端项目配置表.md》
- 获得后端项目代码
- 使用《spec/前端开发/前端代码规范.md》
- 使用《spec/前端开发/前端组件库文档.md》
- 使用《spec/前端开发/前端路由配置文档.md》
- 使用《spec/前端开发/前端单元测试报告.md》
- 使用《spec/前端开发/前端项目配置表.md》
- 获得前端项目代码
#### 交付物
- 必须生成《spec/测试开发/前端测试用例检测项.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/前端测试记录.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/前端测试报告.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/后端测试用例检测项.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/后端测试记录.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/后端测试报告.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/测试开发/完整测试报告.md》

### 运维工程师
#### 交付物
- 必须生成《spec/运维开发/运维规范.md》
> <你需要解释一下文档的内容、章节>
- 必须生成《spec/运维开发/运维文档.md》
> <你需要解释一下文档的内容、章节>
