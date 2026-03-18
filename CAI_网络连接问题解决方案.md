# CAI 网络连接问题解决方案

## 问题描述

在 Kali Linux 上运行 CAI 时出现以下警告信息：

```
WARNING: Error fetching model pricing: HTTPSConnectionPool(host='raw.githubusercontent.com', port=443): Read timed out. (read timeout=2)
WARNING: Error fetching model pricing: HTTPSConnectionPool(host='raw.githubusercontent.com', port=443): Max retries exceeded with url: /BerriAI/litellm/main/model_prices_and_context_window.json (Caused by NewConnectionError("HTTPSConnection(host='raw.githubusercontent.com', port=443): Failed to establish a new connection: [Errno 101] Network is unreachable"))
```

## 问题分析

CAI 在启动时会尝试从 GitHub 获取模型定价信息（`model_prices_and_context_window.json`），用于计算使用成本。当网络连接不稳定或被阻止时，会出现此错误。

**重要**：这个警告**不会影响 CAI 的核心功能**，只是价格计算功能可能不准确。DeepSeek API 仍然可以正常工作。

## 解决方案

### 方案1：禁用价格检查（推荐）

这是最简单的解决方案，完全禁用价格检查功能。

#### 方法A：通过环境变量禁用

```bash
# 在启动 CAI 前设置环境变量
export LITELLM_LOCAL_MODEL_COST_MAP="true"
export CAI_DISABLE_PRICE_CHECK="true"

# 然后启动 CAI
cai
```

#### 方法B：修改 .env 文件

在 `.env` 文件中添加以下行：

```bash
# 禁用价格检查
LITELLM_LOCAL_MODEL_COST_MAP="true"
CAI_DISABLE_PRICE_CHECK="true"

# 设置超时时间更长
CAI_NETWORK_TIMEOUT=30
```

#### 方法C：在 CAI 交互界面中配置

```
CAI> /config set 15 "true"    # 禁用价格检查
CAI> /config set 16 "30"      # 设置网络超时为30秒
```

### 方案2：配置代理服务器

如果网络需要代理才能访问外部资源：

#### 设置 HTTP/HTTPS 代理

```bash
# 临时设置代理
export http_proxy="http://your-proxy:port"
export https_proxy="http://your-proxy:port"
export HTTP_PROXY="http://your-proxy:port"
export HTTPS_PROXY="http://your-proxy:port"

# 或者添加到 .env 文件
echo 'HTTP_PROXY="http://your-proxy:port"' >> .env
echo 'HTTPS_PROXY="http://your-proxy:port"' >> .env
```

#### 对于 Kali Linux 特定配置

```bash
# 查看当前网络配置
ip addr show
ping 8.8.8.8

# 如果使用 VPN 或特殊网络
sudo systemctl restart NetworkManager
```

### 方案3：增加超时时间

默认超时时间可能太短，可以增加：

```bash
# 设置更长的超时时间
export CAI_NETWORK_TIMEOUT=30
export LITELLM_TIMEOUT=30

# 或者使用命令行参数
cai --timeout 30
```

### 方案4：使用本地缓存文件

#### 下载定价文件到本地

```bash
# 创建缓存目录
mkdir -p ~/.cache/cai

# 手动下载定价文件
curl -o ~/.cache/cai/model_prices.json \
  https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json

# 设置环境变量指向本地文件
export LITELLM_MODEL_COST_MAP_FILE="~/.cache/cai/model_prices.json"
```

#### 创建简化的本地定价配置

创建文件 `~/.cache/cai/local_prices.json`：

```json
{
  "deepseek-chat": {
    "input_cost_per_token": 0.00000014,
    "output_cost_per_token": 0.00000028,
    "max_tokens": 32768
  },
  "gpt-4o": {
    "input_cost_per_token": 0.000005,
    "output_cost_per_token": 0.000015,
    "max_tokens": 128000
  }
}
```

然后在 `.env` 中引用：
```bash
LITELLM_MODEL_COST_MAP_FILE="/home/kali/.cache/cai/local_prices.json"
```

### 方案5：完全离线模式

如果需要在完全离线环境中使用：

```bash
# 1. 禁用所有网络检查
export CAI_OFFLINE_MODE="true"
export LITELLM_OFFLINE="true"
export CAI_DISABLE_PRICE_CHECK="true"

# 2. 使用本地模型（如 Ollama）
export OLLAMA="http://localhost:11434"
export CAI_MODEL="llama3.2"

# 3. 启动 CAI
cai
```

## 验证解决方案

### 测试网络连接

```bash
# 测试 GitHub 访问
curl -I https://raw.githubusercontent.com
ping raw.githubusercontent.com

# 测试 DeepSeek API 连接
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "test"}]}' \
  --connect-timeout 10
```

### 测试 CAI 启动

```bash
# 使用推荐的配置启动
export CAI_DISABLE_PRICE_CHECK="true"
export CAI_NETWORK_TIMEOUT=30
cai --debug
```

## 完整配置示例

### .env 文件配置

```bash
# DeepSeek API 配置
OPENAI_API_KEY="sk-your-deepseek-api-key"
OPENAI_BASE_URL="https://api.deepseek.com/v1"
CAI_MODEL="deepseek-chat"

# 网络优化配置
CAI_DISABLE_PRICE_CHECK="true"
LITELLM_LOCAL_MODEL_COST_MAP="true"
CAI_NETWORK_TIMEOUT=30
HTTP_PROXY=""
HTTPS_PROXY=""

# 其他配置
ANTHROPIC_API_KEY=""
OLLAMA=""
PROMPT_TOOLKIT_NO_CPR=1
CAI_STREAM=false
CAI_GUARDRAILS="true"
```

### 启动脚本

创建 `start_cai.sh`：

```bash
#!/bin/bash
# CAI 启动脚本 - 解决网络问题

# 设置环境变量
export CAI_DISABLE_PRICE_CHECK="true"
export LITELLM_LOCAL_MODEL_COST_MAP="true"
export CAI_NETWORK_TIMEOUT=30

# 加载 .env 文件
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 启动 CAI
echo "启动 CAI (DeepSeek 模式)..."
echo "模型: ${CAI_MODEL:-deepseek-chat}"
echo "API: ${OPENAI_BASE_URL:-https://api.deepseek.com/v1}"
echo ""

cai "$@"
```

给执行权限并运行：
```bash
chmod +x start_cai.sh
./start_cai.sh
```

## 故障排除

### 问题1：仍然看到警告

如果禁用价格检查后仍然看到警告：

```bash
# 检查环境变量是否生效
echo $CAI_DISABLE_PRICE_CHECK

# 尝试完全禁用 litellm 的价格更新
export LITELLM_UPDATE_MODEL_COST_MAP="false"
export LITELLM_CACHE="true"
```

### 问题2：DeepSeek API 连接失败

```bash
# 测试 DeepSeek API
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello"}]}'

# 如果返回 401，检查 API 密钥
# 如果返回 404，检查 OPENAI_BASE_URL
```

### 问题3：Kali Linux 网络配置

```bash
# 检查网络服务
sudo systemctl status NetworkManager
sudo systemctl status networking

# 重启网络
sudo systemctl restart NetworkManager

# 检查 DNS
cat /etc/resolv.conf
ping 8.8.8.8
```

### 问题4：防火墙阻止

```bash
# 检查防火墙
sudo ufw status
sudo iptables -L

# 临时禁用防火墙（仅测试用）
sudo ufw disable

# 添加规则允许出站
sudo ufw allow out 443/tcp
```

## 高级配置

### 使用本地 litellm 配置

创建 `~/.litellm/config.yaml`：

```yaml
model_cost:
  deepseek-chat:
    input_cost_per_token: 0.00000014
    output_cost_per_token: 0.00000028
    max_tokens: 32768

general_settings:
  drop_params: true
  disable_price_checking: true
  timeout: 30.0
```

### 修改 CAI 源代码

如果以上方法都不行，可以修改 CAI 源代码：

1. 找到价格检查相关代码：
```bash
grep -r "model_prices_and_context_window" src/
```

2. 注释掉相关代码或增加超时时间

## 性能优化建议

### 网络优化

```bash
# 调整 TCP 参数
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.wmem_max=26214400
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 26214400"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 26214400"

# 增加文件描述符限制
ulimit -n 65536
```

### CAI 配置优化

```bash
# 在 .env 中添加
CAI_MAX_CONCURRENT=3
CAI_CACHE_ENABLED=true
CAI_LOG_LEVEL="ERROR"  # 减少日志输出
```

## 总结

网络连接警告**不影响 CAI 核心功能**，只是价格计算可能不准确。推荐解决方案：

1. **最简单**：设置 `CAI_DISABLE_PRICE_CHECK="true"`
2. **最彻底**：配置代理并增加超时时间
3. **离线环境**：使用本地缓存文件

对于毕设演示，建议使用方案1，这样不会在演示时出现警告信息干扰。

## 快速修复命令

```bash
# 一键修复（在 CAI 目录下）
echo 'CAI_DISABLE_PRICE_CHECK="true"' >> .env
echo 'LITELLM_LOCAL_MODEL_COST_MAP="true"' >> .env
echo 'CAI_NETWORK_TIMEOUT=30' >> .env

# 重新启动
source venv/bin/activate
source .env
cai
```

这样配置后，CAI 将不再尝试获取远程定价信息，警告信息会消失，DeepSeek API 可以正常使用。