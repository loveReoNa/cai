# CAI 快速解题指南 - 直接操作步骤

## 快速开始

### 步骤1：启动CAI并配置

```bash
# 在Kali终端中，进入CAI目录
cd ~/cai

# 激活虚拟环境
source venv/bin/activate

# 设置环境变量（禁用价格检查警告）
export CAI_DISABLE_PRICE_CHECK="true"

# 启动CAI
cai
```

### 步骤2：选择CTF解题代理

在 `CAI>` 提示符下：

```
CAI> /agent select redteam_agent
```

或者使用bug bounty代理：
```
CAI> /agent select bug_bounter_agent
```

### 步骤3：直接输入URL解题

**格式1：简单扫描**
```
CAI> 扫描 http://靶机URL 并找出flag
```

**格式2：详细测试**
```
CAI> 对 http://靶机URL 进行完整的安全测试，包括端口扫描、目录爆破、漏洞检测
```

**格式3：CTF特定挑战**
```
CAI> 这是一个CTF Web挑战，URL是 http://靶机URL，请帮我找到隐藏的flag
```

## 实际示例

### 示例1：测试DVWA靶机
```
CAI> 扫描 http://192.168.1.100/dvwa 并找出SQL注入漏洞
```

### 示例2：测试bWAPP靶机
```
CAI> 对 http://192.168.1.101/bWAPP 进行安全测试，寻找flag
```

### 示例3：快速CTF解题
```
CAI> 这是一个CTF挑战，访问 http://ctf.example.com:8080，请帮我解题获取flag
```

## 快捷命令

### 单行命令模式（不进入交互界面）

```bash
# 直接运行解题命令
cai --continue --prompt "扫描 http://靶机URL 并找出flag"

# 示例
cai --continue --prompt "测试 http://testphp.vulnweb.com 的SQL注入漏洞"
```

### 常用CTF命令

1. **信息收集**
   ```
   CAI> $ nmap -sV -sC 靶机IP
   CAI> $ dirb http://靶机URL
   ```

2. **漏洞扫描**
   ```
   CAI> $ nikto -h http://靶机URL
   ```

3. **Web测试**
   ```
   CAI> 测试 http://靶机URL/login.php 的登录表单
   ```

## 配置优化

### 创建快速启动脚本

创建文件 `quick_ctf.sh`：
```bash
#!/bin/bash
cd ~/cai
source venv/bin/activate
export CAI_DISABLE_PRICE_CHECK="true"
cai --continue --prompt "扫描 $1 并找出flag"
```

使用方式：
```bash
chmod +x quick_ctf.sh
./quick_ctf.sh "http://靶机URL"
```

### 一键测试命令

```bash
# 测试常见漏洞
echo "测试 http://靶机URL" | cai --continue

# 批量测试
for url in "http://target1" "http://target2"; do
    cai --continue --prompt "扫描 $url" >> results.txt
done
```

## 注意事项

1. **确保网络连通**：靶机必须可访问
2. **使用正确代理**：如果需要选择redteam_agent
3. **查看结果**：CAI会输出详细步骤和发现
4. **交互模式**：可以继续提问，如"如何利用这个漏洞？"

## 故障排除

如果命令不工作：
1. 确保CAI已正确启动
2. 检查代理选择：`/agent list`
3. 尝试简单命令：`CAI> $ whoami`

## 演示示例

完整流程：
```bash
# 终端1：启动CAI
cd ~/cai
source venv/bin/activate
cai

# 在CAI交互界面中：
CAI> /agent select redteam_agent
CAI> 扫描 http://192.168.1.100 并找出开放端口和Web服务
```

CAI将自动执行：
1. 端口扫描
2. Web目录枚举
3. 漏洞检测
4. 提供攻击建议

现在你可以直接使用这些命令开始解题！