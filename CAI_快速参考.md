# CAI 快速参考指南

## 安装与启动

```bash
# 安装
pip install cai-framework

# 启动交互式界面
cai

# 带参数启动
cai --continue --prompt "执行安全扫描"

# 指定模型
CAI_MODEL="qwen2.5:14b" cai
```

## 基本命令

### 在CAI交互界面中
```
CAI> 扫描目标 192.168.1.1
CAI> 分析端口 80,443
CAI> 查找SQL注入漏洞
CAI> /help          # 查看帮助
CAI> /config        # 配置设置
CAI> /exit          # 退出
```

### 直接运行Python脚本
```python
import asyncio
from cai.sdk.agents import Runner, Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# 创建代理
agent = Agent(
    name="安全代理",
    instructions="你是网络安全专家",
    model=OpenAIChatCompletionsModel(
        model="qwen2.5:14b",
        openai_client=AsyncOpenAI()
    )
)

# 运行代理
result = await Runner.run(agent, "执行安全任务")
```

## 常用工具

### 命令行工具
```python
from cai.tools.common import run_command
from cai.sdk.agents import function_tool

@function_tool
def run_cmd(command: str) -> str:
    """执行系统命令"""
    return run_command(command)
```

### 网络扫描工具
```python
@function_tool
def scan_ports(target: str, ports: str = "1-1000") -> str:
    """扫描目标端口"""
    return run_command(f"nmap -p {ports} {target}")
```

### 文件分析工具
```python
@function_tool  
def analyze_file(filepath: str) -> str:
    """分析文件内容"""
    return run_command(f"file {filepath} && strings {filepath}")
```

## CTF解题模板

### 1. 基础CTF代理
```python
ctf_agent = Agent(
    name="CTF解题代理",
    description="专门解决CTF挑战",
    instructions="""你是一名CTF选手，擅长：
    1. 信息收集和侦察
    2. 漏洞分析和利用
    3. 权限提升
    4. Flag提取
    使用提供的工具完成任务。""",
    tools=[run_cmd, scan_ports, analyze_file],
    model=...
)
```

### 2. 多代理协作
```python
# 侦察代理
recon_agent = Agent(name="侦察", instructions="收集目标信息")

# 分析代理  
analysis_agent = Agent(name="分析", instructions="分析漏洞")

# 利用代理
exploit_agent = Agent(name="利用", instructions="利用漏洞")

# 设置交接
recon_agent.handoffs.append(analysis_agent)
analysis_agent.handoffs.append(exploit_agent)
```

## 环境配置

### .env 文件示例
```bash
# 必需
OPENAI_API_KEY="sk-xxx"
# 或使用本地模型
OLLAMA="http://localhost:11434"
CAI_MODEL="qwen2.5:14b"

# 可选
CAI_PRICE_LIMIT="0.01"
CAI_MAX_TURNS="20"
CAI_GUARDRAILS="true"
CTF_NAME="练习挑战"
```

### 运行时配置命令
```
CAI> /config set 1 "qwen2.5:14b"    # 设置模型
CAI> /config set 18 "0.01"          # 设置价格限制
CAI> /config set 22 "true"          # 启用防护栏
```

## 实用示例

### 示例1：自动化端口扫描
```bash
cai --continue --prompt "扫描192.168.1.1的1-1000端口，分析开放服务"
```

### 示例2：Web应用测试
```bash
cai --continue --prompt "测试http://target.com的SQL注入和XSS漏洞"
```

### 示例3：文件分析
```bash
cai --continue --prompt "分析可疑文件malware.exe，提取IOC指标"
```

### 示例4：完整CTF流程
```python
async def solve_ctf():
    # 1. 侦察
    await agent.run("扫描目标，发现开放端口")
    # 2. Web目录爆破
    await agent.run("爆破Web目录，寻找敏感文件")
    # 3. 漏洞利用
    await agent.run("利用发现的漏洞获取shell")
    # 4. 权限提升
    await agent.run("提权到root用户")
    # 5. 寻找flag
    await agent.run("在系统中搜索flag文件")
```

## 调试技巧

### 启用调试输出
```bash
export CAI_DEBUG=2
cai
```

### 查看代理思考过程
```python
# 流式输出
result = Runner.run_streamed(agent, "任务")
async for event in result.stream_events():
    print(f"事件: {event.type} - {event.content}")
```

### 临时禁用防护栏
```bash
CAI_GUARDRAILS="false" cai
# 注意：仅用于调试，生产环境请保持启用
```

## 安全最佳实践

1. **始终在授权范围内测试**
2. **使用防护栏防止意外操作**
3. **设置价格限制控制成本**
4. **定期查看代理执行日志**
5. **重要操作前人工确认**
6. **备份重要数据和配置**

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 代理不响应 | 模型连接问题 | 检查API密钥和网络 |
| 命令被阻止 | 防护栏拦截 | 检查命令安全性或临时禁用防护栏 |
| 内存不足 | 模型太大 | 使用更小模型或增加系统内存 |
| 执行缓慢 | 网络延迟 | 使用本地模型（Ollama） |

## 获取帮助

- 查看文档：`docs/` 目录
- 运行示例：`examples/` 目录
- 社区支持：GitHub Issues
- 紧急问题：Discord社区

---

**提示**: CAI是强大的工具，请负责任地使用。始终遵守法律法规和道德准则。