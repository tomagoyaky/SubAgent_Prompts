#!/bin/bash
# -----------------------------------------------------------------
# Author: Auto Agent Team
# Date: 2026-02-06
# Description:
#   Auto Agent Startup Script
# -----------------------------------------------------------------

clear
set -e

################################################################################
## 变量定义
################################################################################
PROJECT_NAME="AutoAgent"
AGENT_PORT=8000
CLI_MODE=true
DEFAULT_USER_INPUT=""

################################################################################
## 文件夹定义
################################################################################
DIR_PROJECT_ROOT=$(pwd)
DIR_CURRENT=${DIR_PROJECT_ROOT}
DIR_LOGS=${DIR_CURRENT}/logs
DIR_WORKSPACE=${DIR_CURRENT}/workspace
DIR_VENV=${DIR_CURRENT}/.venv

################################################################################
## 文件定义
################################################################################
FILE_START_SH="start.sh"
FILE_RUN_PY="run.py"
FILE_REQUIREMENTS_TXT="requirements.txt"

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
CURRENT_LOG_LEVEL=$LOG_LEVEL_INFO
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

# 检查端口是否被占用
check_port() {
    port=$1
    PID=$(lsof -i :$port 2>/dev/null | awk 'NR>=2 {print $2}')
    if [ -n "$PID" ]; then
        log_warn "端口${port}已被占用，PID: ${PID}"
        return 1
    else
        log_info "端口${port}未被占用"
        return 0
    fi
}

# 杀死指定端口的进程
kill_port() {
    port=$1
    PID=$(lsof -i :$port 2>/dev/null | awk 'NR>=2 {print $2}')
    if [ -n "$PID" ]; then
        log_info "清理已存在进程占用端口${port}, PID: ${PID}"
        kill -9 $PID > /dev/null 2>&1
        log_info "进程${PID}已终止"
    else
        log_info "端口${port}未被占用"
    fi
}

# 检查虚拟环境是否存在
check_venv() {
    if [ -d "$DIR_VENV" ]; then
        log_info "虚拟环境已存在: $DIR_VENV"
        return 0
    else
        log_warn "虚拟环境不存在: $DIR_VENV"
        return 1
    fi
}

# 创建虚拟环境
create_venv() {
    log_info "创建虚拟环境..."
    cmd "python3 -m venv $DIR_VENV"
    log_info "虚拟环境创建成功"
}

# 激活虚拟环境
activate_venv() {
    if check_venv; then
        log_info "激活虚拟环境..."
        source "$DIR_VENV/bin/activate"
        log_info "虚拟环境激活成功"
        return 0
    else
        log_error "虚拟环境不存在，无法激活"
        return 1
    fi
}

# 安装依赖
install_deps() {
    if [ -f "$FILE_REQUIREMENTS_TXT" ]; then
        log_info "安装依赖..."
        cmd "pip install -r $FILE_REQUIREMENTS_TXT"
        log_info "依赖安装成功"
    else
        log_warn "依赖文件不存在: $FILE_REQUIREMENTS_TXT"
    fi
}

# 创建必要的目录
create_dirs() {
    log_info "创建必要的目录..."
    cmd "mkdir -p $DIR_LOGS $DIR_WORKSPACE"
    log_info "目录创建成功"
}

# 检查Python版本
check_python() {
    log_info "检查Python版本..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        log_info "Python版本: $PYTHON_VERSION"
        return 0
    else
        log_error "Python3未安装"
        return 1
    fi
}

################################################################################
## 主函数
################################################################################
main() {
    # 解析命令行参数
    parse_args "$@"
    
    # 脚本开场
    log_start "Auto Agent 启动脚本"
    
    # 1. 检查Python环境
    log_function_index_title "1" "检查Python环境"
    check_python
    
    # 2. 创建必要的目录
    log_function_index_title "2" "创建必要的目录"
    create_dirs
    
    # 3. 检查并创建虚拟环境
    log_function_index_title "3" "检查并创建虚拟环境"
    if ! check_venv; then
        create_venv
    fi
    
    # 4. 激活虚拟环境
    log_function_index_title "4" "激活虚拟环境"
    activate_venv
    
    # 5. 安装依赖
    log_function_index_title "5" "安装依赖"
    install_deps
    
    # 6. 检查端口
    log_function_index_title "6" "检查端口"
    check_port $AGENT_PORT
    
    # 7. 启动Auto Agent
    log_function_index_title "7" "启动Auto Agent"
    log_info "启动Auto Agent..."
    
    # 构建Python命令
    if [ -f "$FILE_RUN_PY" ]; then
        PYTHON_CMD="python \"$FILE_RUN_PY\""
        
        # 添加CLI模式参数
        if [ "$CLI_MODE" = true ]; then
            PYTHON_CMD="$PYTHON_CMD --cli"
        fi
        
        # 添加默认用户输入参数
        if [ -n "$DEFAULT_USER_INPUT" ]; then
            PYTHON_CMD="$PYTHON_CMD --default_user_input \"$DEFAULT_USER_INPUT\""
        fi
        
        log_info "执行: $PYTHON_CMD"
        eval "$PYTHON_CMD"
    else
        log_error "运行文件不存在: $FILE_RUN_PY"
    fi
}

################################################################################
## 解析命令行参数
################################################################################
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--cli)
                CLI_MODE=true
                log_info "CLI模式已启用"
                shift # 跳过参数值
                ;;
            --default_user_input)
                if [[ $# -gt 1 ]]; then
                    DEFAULT_USER_INPUT="$2"
                    log_info "默认用户输入已设置: $DEFAULT_USER_INPUT"
                    shift 2 # 跳过参数名和值
                else
                    log_warn "--default_user_input参数需要一个值"
                    shift # 跳过参数名
                fi
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_warn "未知参数: $1"
                shift # 跳过未知参数
                ;;
        esac
    done
}

################################################################################
## 显示帮助信息
################################################################################
show_help() {
    log_info "==========================================================="
    log_info "| Auto Agent 启动脚本帮助"
    log_info "==========================================================="
    log_info "| 用法: ./start.sh [选项]"
    log_info "|"
    log_info "| 选项:"
    log_info "|   -c, --cli                 启用CLI聊天模式"
    log_info "|   --default_user_input      模拟用户默认输入"
    log_info "|   -h, --help                显示帮助信息"
    log_info "==========================================================="
}

# 执行主函数
main "$@"