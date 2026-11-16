# -*- coding: utf-8 -*-
"""第 2 步：手工 Function Calling —— 一轮"两次调用"的完整流程。
观察点：第 1 次返回 content 为空、任务全在 tool_calls；tool_call_id 必须原样回传。
"""
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:8b"

# —— tools 定义：description/参数说明是写给【模型】看的说明书，抠清楚它才调得准 ——
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询某个城市当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，如'北京'"},
                "date": {"type": "string", "description": "可选，默认今天"},
            },
            "required": ["city"],
        },
    },
}]

def get_weather(city, date=None):
    return {"city": city, "date": date or "今天", "天气": "多云转晴", "气温": 12}

# —— 第 1 次调用：把 tools 一起发上去 ——
question = "北京今天该穿什么？先查天气"
first = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
    tools=tools,
).choices[0].message

print("第 1 次返回 content：", repr(first.content))
print("第 1 次返回 tool_calls：", first.tool_calls)
if not first.tool_calls:
    raise SystemExit("模型没要求调工具。检查 tools 定义或换 instruct 模型。")

# —— 你的代码执行工具 ——
tc = first.tool_calls[0]
args = json.loads(tc.function.arguments)
result = get_weather(**args)
print(f"→ 执行 get_weather(**{args}) = {result}")

# —— 第 2 次调用：过程消息（assistant 的调用要求 + tool 的结果）原样回传 ——
answer = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": question},
        {"role": "assistant", "tool_calls": [{
            "id": tc.id, "type": "function",
            "function": {"name": tc.function.name,
                         "arguments": tc.function.arguments}}],
        },
        {"role": "tool", "tool_call_id": tc.id,
         "content": json.dumps(result, ensure_ascii=False)},
    ],
    tools=tools,
).choices[0].message
print("\n最终回答：", answer.content)