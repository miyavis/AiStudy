# agent-教程 学习空间 —— 总地图

> 两卷独立学习线：**第一卷【用模型】（Agent 实战）→ 第二卷【懂模型】（从零造模型）**。
> 本目录（D:\project\Study）即 git 仓库根层，两卷是递进关系，不是替代关系。所有路径均相对本目录。

---

## 目录结构

```text
D:\project\Study（仓库根）\
├── README.md                        ← 本文件：总地图 + 进度登记
├── 资源清单.md                      ← 拓展学习材料（按阶段取用，防收藏夹吃灰）
│
├── 01-Agent入门\                    ★☆☆ 难度：低　产出：可运行的 Agent（已完成材料）
│   ├── 教程.md                      ← 操作手册：第 0~4 步，边读边跑（8~10 小时）
│   ├── 原理篇.md                    ← 原理教材：每一步背后的"为什么"（6~8 小时）＋第 6 章协议问答实录（Q1~Q11）
│   ├── code\
│   │   ├── 00_check_env.py          ← 环境自检（最先跑）
│   │   ├── 01_chat.py~04b_rag.py    ← 教程第 1~4 步的配套脚本
│   │   └── （跑通后会产生 chat_memory.db 等运行时文件，git 已忽略）
│   ├── docs\示例笔记.txt            ← RAG 测试语料
│   └── demo\                        ☆☆☆ 云端对照实验（早期练手，全部保留）
│       ├── README.md                ← 本目录定位与运行说明
│       ├── chat.py / callTools.py / loopCall.py
│       │                            ← 与本卷 code\ 同构，但走 NVIDIA 云端 API
│       │                               （教程"进阶方向·接云端"的参照物）
│       ├── checkEnv.py / config.py  ← 云端连通自检 / 客户端配置（读 NVIDIA_API_KEY 环境变量）
│       └── requirements.txt         ← 依赖仅 openai（.venv 已清理，用时重建）
│
└── 02-从零造模型\                   ★★☆ 难度：中　产出：亲手写的分词器（阶段 1 进行中：demo 已跑通）
    ├── 路线图.md                    ← 五阶段路线（tokenizer→GPT→预训练→SFT→对齐）
    └── minbpe\
        ├── 00_train_demo.py         ← 5 分钟上手实验（已验证可跑）
        ├── my_tokenizer.model/.vocab ← 训练产物：本卷第一个词表
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
| 第 4 周 | 综合实战：审计 Agent 项目（位于 `D:\project\Agent`，不在本仓库内） | 在项目目录运行 `.\start.ps1` 启动审计 Agent；标本评测达标（检出 ≥10/12、误报 ≤2、金融项 ≥5/6） |
| 第 5 周 | 02 卷：跑 `00_train_demo.py` → 读 `basic.py` → 亲手改词表大小/语料 | 能对着 merge 日志逐行讲出"合并发生了什么" |
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
- [ ] 01 卷自测清单全过（教程「总结与自测」+ 原理篇总表）
- [ ] 综合实战：审计 Agent（`D:\project\Agent`）跑通，标本评测达标（检出 ≥10/12、误报 ≤2、金融项 ≥5/6）
- [ ] 02 卷 demo 跑通
- [ ] minbpe/basic.py 通读
