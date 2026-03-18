"""RND Agent - Research and Development Agent with Comprehensive Coverage
This agent integrates cutting-edge technologies and provides wide-ranging
problem-solving capabilities across multiple cybersecurity domains.
Optimized for DeepSeek API integration and maximum coverage.
"""
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from cai.sdk.agents import Agent, OpenAIChatCompletionsModel
from cai.util import load_prompt_template, create_system_prompt_renderer

load_dotenv()

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', os.getenv('OPENAI_API_KEY'))
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Create DeepSeek client
deepseek_client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

# Load system prompt (use red team prompt as base, can be customized)
try:
    rnd_agent_system_prompt = load_prompt_template("prompts/system_red_team_agent.md")
except:
    # Fallback to a default prompt if the file doesn't exist
    rnd_agent_system_prompt = """You are the RND (Research and Development) Agent, an advanced cybersecurity specialist with comprehensive coverage across all security domains. Your capabilities include reconnaissance, exploitation, defense, analysis, and reporting. You have access to a wide range of tools and should use them strategically to solve complex security challenges."""

# Define comprehensive tools list
tools = []

# Core execution tools
try:
    from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
    tools.append(generic_linux_command)
except ImportError:
    pass

try:
    from cai.tools.reconnaissance.exec_code import execute_code
    tools.append(execute_code)
except ImportError:
    pass

try:
    from cai.tools.command_and_control.sshpass import run_ssh_command_with_credentials
    tools.append(run_ssh_command_with_credentials)
except ImportError:
    pass

# Reconnaissance tools
try:
    from cai.tools.reconnaissance.shodan import shodan_search, shodan_host_info
    tools.append(shodan_search)
    tools.append(shodan_host_info)
except ImportError:
    pass

# Web security tools
try:
    from cai.tools.web.headers import web_request_framework
    tools.append(web_request_framework)
except ImportError:
    pass

try:
    from cai.tools.web.js_surface_mapper import js_surface_mapper
    tools.append(js_surface_mapper)
except ImportError:
    pass

# Network tools
try:
    from cai.tools.network.capture_traffic import capture_remote_traffic, remote_capture_session
    tools.append(capture_remote_traffic)
    tools.append(remote_capture_session)
except ImportError:
    pass

# Specialized tools
try:
    from cai.tools.misc.reasoning import think
    tools.append(think)
except ImportError:
    pass

# Search tools (conditional)
try:
    if os.getenv('PERPLEXITY_API_KEY'):
        from cai.tools.web.search_web import make_web_search_with_explanation
        tools.append(make_web_search_with_explanation)
except ImportError:
    pass

try:
    if os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_CX'):
        from cai.tools.web.google_search import google_search
        tools.append(google_search)
except ImportError:
    pass

# Advanced security testing tools (add if available)
try:
    from cai.tools.data_exfiltration.exfiltration import data_exfiltration_test
    tools.append(data_exfiltration_test)
except ImportError:
    pass

try:
    from cai.tools.exploitation.exploit import exploit_vulnerability
    tools.append(exploit_vulnerability)
except ImportError:
    pass

try:
    from cai.tools.lateral_movement.lateral import lateral_movement_test
    tools.append(lateral_movement_test)
except ImportError:
    pass

try:
    from cai.tools.privilege_scalation.escalation import privilege_escalation_test
    tools.append(privilege_escalation_test)
except ImportError:
    pass

# Security guardrails (optional)
try:
    from cai.agents.guardrails import get_security_guardrails
    input_guardrails, output_guardrails = get_security_guardrails()
except ImportError:
    input_guardrails, output_guardrails = [], []

# Create RND Agent
rnd_agent = Agent(
    name="RND Agent",
    instructions=create_system_prompt_renderer(rnd_agent_system_prompt),
    description="""Advanced Research and Development Agent with comprehensive cybersecurity coverage.
    
SPECIALIZATIONS:
• Full-spectrum security assessment: Reconnaissance, exploitation, lateral movement, privilege escalation
• Cutting-edge technology integration: AI-powered analysis, automated toolchains, adaptive methodologies
• Multi-domain expertise: Web security, network analysis, binary reverse engineering, cloud security
• Research-oriented approach: Novel vulnerability discovery, exploit development, defensive countermeasure design
• DeepSeek API optimization: Leveraging state-of-the-art language models for superior reasoning and code generation

CAPABILITIES:
1. Intelligent Reconnaissance: Automated target profiling, attack surface mapping, vulnerability identification
2. Advanced Exploitation: Custom payload development, bypass techniques, post-exploitation automation
3. Defensive Research: Security control evaluation, mitigation strategy development, incident response simulation
4. Toolchain Integration: Seamless coordination of security tools, workflow automation, result correlation
5. Knowledge Synthesis: Cross-domain pattern recognition, threat intelligence integration, predictive analysis

TECHNOLOGICAL EDGE:
• Adaptive problem-solving algorithms
• Multi-model AI orchestration
• Real-time threat intelligence feeds
• Automated reporting and documentation
• Continuous learning and improvement

This agent represents the pinnacle of cybersecurity automation, combining breadth of coverage with depth of expertise for unparalleled problem-solving capabilities.""",
    tools=tools,
    input_guardrails=input_guardrails,
    output_guardrails=output_guardrails,
    model=OpenAIChatCompletionsModel(
        model="deepseek-chat",  # DeepSeek model
        openai_client=deepseek_client,
    ),
)

# Transfer function for compatibility
def transfer_to_rnd_agent(**kwargs):
    """Transfer to RND Agent.
    Accepts any keyword arguments but ignores them."""
    return rnd_agent