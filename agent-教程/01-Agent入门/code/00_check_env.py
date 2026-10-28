# -*- coding: utf-8 -*-
"""环境自检：确认本地 Ollama API 存活、模型已就位。
运行前提：ollama pull qwen3:8b 和 bge-m3 已完成。
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

try:
    models = [m.id for m in client.models.list().data]
    print("已发现的模型：", models)
    for need in ("qwen3:8b", "bge-m3"):
        if any(need in m for m in models):
            print(f"  [OK] {need}")
        else:
            print(f"  [缺] {need}  → 执行 ollama pull {need}")
except Exception as e:
    print(f"[X] 连接失败：{e}")
    print("    排查：ollama serve 是否启动？端口 11434 是否被占用？")
