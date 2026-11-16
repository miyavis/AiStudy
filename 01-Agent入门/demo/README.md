# demo：云端对照实验（早期练手代码，保留备查）

> **定位**：学习第一卷时用 **NVIDIA 云端 API** 做的对照实验。`..\code\` 用本地 Ollama 教你「从零写」，本目录是同一套逻辑的「接云端」版本——两相对照，正好验证教程第 3 步的核心论断：**本地跑和云端跑，代码结构一模一样，只差一个 base_url。**
>
> 这些代码已完成使命，仅作参考留存；日常学习请以本卷教程与 `..\code\` 为主线。

## 文件一览

| 文件 | 对应教程 | 说明 |
|---|---|---|
| `config.py` | 第 0 步 | 云端客户端配置：`base_url=https://integrate.api.nvidia.com/v1`，密钥从环境变量 `NVIDIA_API_KEY` 读取（不落盘） |
| `checkEnv.py` | 00_check_env.py | 云端连通自检：列出可用模型 |
| `chat.py` | 01_chat.py | 最小聊天机器人（messages 历史重发） |
| `callTools.py` | 02_tool_calling.py | 手工 Function Calling（calc 工具，ast 安全求值） |
| `loopCall.py` | 03_agent_loop.py | **while 循环 Agent（本目录最有价值的文件）**：含对账回填、错误串回传、`tool_of()` 工具声明工厂，写得比早期文件规范 |

## 运行方法

```sh
cd D:\project\Study\01-Agent入门\demo
# .venv 已清理（原环境混入大量无关包）。重建只需一个依赖：
python -m venv .venv
.venv\Scripts\activate
pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple

set NVIDIA_API_KEY=你的密钥      # PowerShell 用 $env:NVIDIA_API_KEY="..."
python checkEnv.py               # 先验连通
python loopCall.py               # 跑云端 Agent
```

## 对照观察点（想复习原理时用）

1. 把 `loopCall.py` 与 `..\code\03_agent_loop.py` 并排 diff：除 `base_url` 和模型名外，主循环逐行同构；
2. 云端大模型的 `tool_calls` JSON 明显比 qwen3:8b 规整——印证原理篇 2.3「失败模式清单」里小模型的参数幻觉问题；
3. `config.py` 只从环境变量取密钥，是「密钥不进代码、不进 git」的最小实践（对照 `.gitignore` 里的 `.env` / `config.json` 条目）。
