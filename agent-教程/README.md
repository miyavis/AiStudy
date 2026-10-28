# agent-教程 学习空间 —— 总地图

> 两卷独立学习线：**第一卷【用模型】（Agent 实战）→ 第二卷【懂模型】（从零造模型）**。
> 本卷间是递进关系，不是替代关系。所有路径均相对本目录。

---

## 目录结构

```text
agent-教程\
├── README.md                        ← 本文件：总地图 + 进度登记
│
├── 01-Agent入门\                    ★☆☆ 难度：低　产出：可运行的 Agent（已完成材料）
│   ├── 教程.md                      ← 操作手册：第 0~4 步，边读边跑（8~10 小时）
│   ├── 原理篇.md                    ← 原理教材：每一步背后的"为什么"（6~8 小时）
│   ├── code\
│   │   ├── 00_check_env.py          ← 环境自检（最先跑）
│   │   ├── 01_chat.py~04b_rag.py    ← 教程第 1~4 步的配套脚本
│   │   └── （跑通后会产生 chat_memory.db / *.model.db 等运行时文件）
│   └── docs\示例笔记.txt            ← RAG 测试语料
│
└── 02-从零造模型\                   ★★☆ 难度：中　产出：亲手写的分词器（材料建设中）
    ├── 路线图.md                    ← 五阶段路线（tokenizer→GPT→预训练→SFT→对齐）
    └── minbpe\
        ├── 00_train_demo.py         ← 5 分钟上手实验（已验证可跑）
        ├── my_tokenizer.model/.vocab ← demo 产物：你自己训练出的第一个词表！
        └── minbpe\                  ← Karpathy 的 minbpe 源码包
            ├── basic.py             ← 核心读物：~90 行的纯 BPE
            ├── base.py              ← 基类 + get_stats/merge 两个算法函数
            ├── regex.py / gpt4.py   ← 生产版扩展（可后置）
            └── __init__.py
```

## 推荐学习顺序

| 周 | 做什么 | 验收标志 |
|---|---|---|
| 第 1 周 | 01 卷：跑 `00_check_env.py` → 教程第 1~2 步 → 原理篇第 1~2 章 | 聊天机器人活着；能解释 tool_calls 生命周期 |
| 第 2 周 | 01 卷：教程第 3 步 + 原理篇第 3 章 | while 循环 Agent 默写 |
| 第 3 周 | 01 卷：教程第 4 步 + 原理篇第 4 章 | 记忆机器人跨会话记得你；RAG 能答语料专属词条 |
| 第 4 周 | 02 卷：跑 demo → 读 `basic.py` → 亲手改词表大小/语料 | 能对着 merge 日志逐行讲出"合并发生了什么" |
| 之后 | 02 卷路线图.md 第 2 阶段起 | —— |

## 环境速查

- 依赖：Ollama（qwen3:8b + bge-m3）＋ Python venv（`openai` `numpy` `regex`）
- pip 走清华源：`pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple`
- qwen3 思考模式太慢时：用户消息加 ` /no_think`

## 进度登记（自己维护）

- [ ] 00_check_env 通过（两个 [OK]）
- [ ] 01_chat 跑通，观察点 1 复现（注释失忆实验）
- [ ] 02_tool_calling 跑通
- [ ] 03_agent_loop 跑通 trace 实验
- [ ] 04a_memory 跨会话记忆验证
- [ ] 04b_rag 专属词条检索验证
- [ ] 01 卷结业自测（原理篇 5 张总表默写）
- [ ] 02 卷 demo 跑通
- [ ] minbpe/basic.py 通读
