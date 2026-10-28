# -*- coding: utf-8 -*-
"""第 1 步：命令行聊天机器人（带上下文记忆）。
观察点：1) 注释掉喂回 assistant 那行会失忆 2) prompt_tokens 每轮累加。
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:8b"
SYSTEM = "你是一个简洁的中文助手，回答不超过三句话。"

history = [{"role": "system", "content": SYSTEM}]
print("开始聊天（直接回车退出）")

while True:
    user = input("\n你：").strip()
    if not user:
        break
    history.append({"role": "user", "content": user})
    resp = client.chat.completions.create(model=MODEL, messages=history)
    answer = resp.choices[0].message.content
    print(f"\n助手：{answer}")
    print(f"（token：输入 {resp.usage.prompt_tokens}，输出 {resp.usage.completion_tokens}）")
    history.append({"role": "assistant", "content": answer})  # 关键行：喂回去才会"记"