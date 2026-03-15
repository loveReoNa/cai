# CAI (Cybersecurity AI) 使用解题指南

## 概述

CAI (Cybersecurity AI) 是一个专注于网络安全任务自动化的AI代理框架。它通过智能代理（Agents）、工具（Tools）、交接（Handoffs）和模式（Patterns）等核心概念，帮助安全研究人员、CTF选手和渗透测试人员自动化执行安全任务。

## 核心架构

CAI 基于8大支柱构建：

1. **代理（Agents）** - 执行安全任务的智能实体
2. **工具（Tools）** - 代理执行操作的能力接口
3. **交接（Handoffs）** - 代理之间的任务传递机制
4. **模式（Patterns）** - 代理协作的结构化设计范式
5. **轮次（Turns）** - 代理交互的循环周期
6. **追踪（Tracing）** - 执行过程的监控和记录
7. **防护栏（Guardrails）** - 安全防护机制
8. **人在回路（HITL）** - 人工干预和监控

## 快速开始

### 安装

```bash
# 使用pip安装
pip install cai-framework

# 创建虚拟环境（推荐）
python3.12 -m venv cai_env
source cai_env/bin/activate  # Linux/Mac
# 或
cai_env\Scripts\activate     # Windows

# 安装CAI
pip install cai-framework
```

### 配置环境变量

创建 `.env` 文件：

```bash
OPENAI_API_KEY="sk-your-key-here"  # 必需，可以是占位符
ANTHROPIC_API_KEY=""               # 可选
OLLAMA=""                          # 可选，本地模型
PROMPT_TOOLKIT_NO_CPR=1            # 推荐设置
```

### 启动CAI

```bash
cai
```

启动后将看到CAI的ASCII艺术标志和交互式提示符 `CAI>`。

## 基本使用示例

### 1. 简单代理执行命令

```python
import asyncio
from cai.sdk.agents import Runner, Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from cai.sdk.agents import function_tool
from cai.tools.common import run_command

@function_tool
def execute_cli_command(command: str) -> str:
    return run_command(command)

ctf_agent = Agent(
    name="CTF代理",
    description="专注于解决CTF挑战的安全专家",
    instructions="你是一名网络安全专家，正在参加CTF比赛",
    tools=[execute_cli_command],
    model=OpenAIChatCompletionsModel(
        model=os.getenv('CAI_MODEL', "qwen2.5:14b"),
        openai_client=AsyncOpenAI(),
    )
)

async def main():
    result = await Runner.run(ctf_agent, "列出当前目录的文件")
    print(result.final_output)

asyncio.run(main())
```

### 2. 使用交接（Handoffs）模式

交接允许代理将任务传递给更专业的代理：

```python
from cai.sdk.agents import handoff

# 创建专业代理
flag_extractor = Agent(
    name="Flag提取器",
    description="专门从输出中提取flag",
    instructions="你专门负责从CTF输出中提取flag",
    model=OpenAIChatCompletionsModel(...)
)

# 创建交接
flag_handoff = handoff(
    agent=flag_extractor,
    input_filter=lambda ctx, args: flag_extractor
)

# 将交接添加到主代理
ctf_agent.handoffs.append(flag_handoff)
```

### 3. 并行化模式

同时运行多个代理以提高效率：

```python
import asyncio

async def parallel_ctf():
    # 同时运行三个代理解决同一挑战
    results = await asyncio.gather(
        Runner.run(ctf_agent, challenge),
        Runner.run(ctf_agent, challenge),
        Runner.run(ctf_agent, challenge)
    )
    
    # 使用评估代理选择最佳方案
    evaluator = Agent(...)
    best_solution = await Runner.run(
        evaluator,
        f"挑战: {challenge}\n\n方案:\n{results}"
    )
```

## CTF解题流程

### 典型CTF解题步骤

1. **信息收集**
   ```bash
   cai> 扫描目标IP 192.168.1.100的开放端口
   ```

2. **漏洞分析**
   ```bash
   cai> 分析端口80的Web应用，寻找SQL注入漏洞
   ```

3. **漏洞利用**
   ```bash
   cai> 利用发现的SQL注入获取数据库信息
   ```

4. **权限提升**
   ```bash
   cai> 尝试从普通用户提升到root权限
   ```

5. **Flag提取**
   ```bash
   cai> 在系统中搜索包含"flag"的文件
   ```

### 自动化CTF解题示例

```python
# 完整的CTF自动化流程
async def solve_ctf(target_ip):
    # 1. 侦察阶段
    recon_result = await Runner.run(recon_agent, f"扫描 {target_ip}")
    
    # 2. 漏洞分析
    vuln_result = await Runner.run(
        analysis_agent, 
        f"分析扫描结果: {recon_result.final_output}"
    )
    
    # 3. 利用阶段
    exploit_result = await Runner.run(
        exploit_agent,
        f"利用发现的漏洞: {vuln_result.final_output}"
    )
    
    # 4. 后渗透
    post_result = await Runner.run(
        post_exploit_agent,
        f"在目标系统上执行: {exploit_result.final_output}"
    )
    
    return post_result
```

## 高级功能

### 防护栏（Guardrails）

CAI内置多层防护机制，防止危险命令执行：

```python
# 启用防护栏（默认启用）
export CAI_GUARDRAILS=true

# 防护栏会检测和阻止：
# - 反向shell命令
# - 文件系统破坏命令
# - 数据泄露尝试
# - 权限提升攻击
```

### 追踪（Tracing）

监控代理执行过程：

```python
from cai.sdk.agents import trace

with trace(workflow_name="CTF工作流"):
    result = await Runner.run(agent, "执行安全任务")
    # 执行过程会被记录和追踪
```

### 人在回路（HITL）

随时按 Ctrl+C 中断代理执行，进行人工干预：

```bash
CAI> 开始自动化渗透测试
# 按 Ctrl+C 中断
[人类干预] 请输入下一步指令:
```

## 配置选项

### 环境变量

| 变量 | 描述 | 示例 |
|------|------|------|
| `CAI_MODEL` | 使用的AI模型 | `qwen2.5:14b` |
| `CAI_PRICE_LIMIT` | 价格限制（美元） | `0.004` |
| `CAI_MAX_TURNS` | 最大交互轮次 | `10` |
| `CAI_GUARDRAILS` | 启用防护栏 | `true` |
| `CTF_NAME` | CTF挑战名称 | `picoctf_static_flag` |

### 运行时配置

在CAI交互界面中使用 `/config` 命令：

```bash
CAI> /config
# 显示所有配置选项
CAI> /config set 18 "0.004"  # 设置价格限制
```

## 实用技巧

### 1. 使用继续模式（Continue Mode）

```bash
# 让代理自动继续执行任务
cai --continue --prompt "执行完整的安全审计"
```

### 2. 流式输出

```python
# 实时查看代理思考过程
result = Runner.run_streamed(agent, "复杂任务")
async for event in result.stream_events():
    print(event)  # 实时输出
```

### 3. 自定义工具

```python
@function_tool
def custom_security_scan(target: str) -> str:
    """自定义安全扫描工具"""
    # 实现扫描逻辑
    return scan_results

# 将工具添加到代理
agent.tools.append(custom_security_scan)
```

### 4. 代理模式选择

- **群集模式（Swarm）**: 多个代理协同工作
- **分层模式（Hierarchical）**: 主代理分配任务
- **思维链模式（Chain-of-Thought）**: 线性任务传递
- **并行模式（Parallelization）**: 同时执行多个任务

## 故障排除

### 常见问题

1. **代理不执行命令**
   - 检查工具权限
   - 验证环境变量配置
   - 查看防护栏是否阻止了命令

2. **模型响应慢**
   - 切换到本地模型（如Ollama）
   - 调整 `CAI_MAX_TURNS` 减少轮次
   - 使用更小的模型

3. **交接不工作**
   - 检查代理定义
   - 验证交接条件
   - 查看代理输出格式

### 调试模式

```bash
# 启用详细调试输出
export CAI_DEBUG=2
cai
```

## 资源

### 文档
- [官方文档](docs/) - 完整API和概念文档
- [示例代码](examples/) - 实用代码示例
- [研究论文](docs/research.md) - 理论基础

### 社区
- [GitHub仓库](https://github.com/aliasrobotics/cai)
- [问题追踪](https://github.com/aliasrobotics/cai/issues)
- [Discord社区](https://discord.gg/aliasrobotics)

### 进阶学习
1. 阅读 `examples/cai/` 中的示例
2. 尝试修改现有代理模式
3. 创建自定义安全工具
4. 参与CTF比赛实践

## 总结

CAI为网络安全自动化提供了强大的框架。通过合理使用代理、工具和模式，可以显著提高安全任务的效率和效果。建议从简单示例开始，逐步掌握高级功能，最终能够构建复杂的自动化安全工作流。

**记住**: 始终在合法授权范围内使用CAI，遵守网络安全伦理和法律法规。