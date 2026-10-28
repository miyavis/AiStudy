# -*- coding: utf-8 -*-
"""第 3 步：while 循环 Agent —— 任一框架剥开后的真身。
看 trace 学模型如何自由组合工具；改 max_turns 感受死循环防护。
"""
import json
import datetime
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:8b"

# ---------- 真实的 Python 实现 ----------
def get_weather(city):
    return {"city": city, "天气": "多云转晴", "气温": 12}

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M %A")

def calc(expr):
    if not set(expr) <= set("0123456789+-*/(). "):
        return "仅支持四则运算"
    return eval(expr)  # 教学代码已做白名单；生产请改用 ast 安全求值

DISPATCH = {"get_weather": get_weather, "get_now": get_now, "calc": calc}

# ---------- tools 定义 ----------
def tool_of(name, desc, props, required=None):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": props,
                       "required": required or list(props)}}}

TOOLS = [
    tool_of("get_weather", "查询某个城市当前天气",
            {"city": {"type": "string", "description": "城市名，如'北京'"}}),
    tool_of("get_now", "获取当前日期、时间和星期几", {}),
    tool_of("calc", "计算一个四则运算表达式，如 '7*24-3'",
            {"expr": {"type": "string", "description": "算术表达式"}}),
]

SYSTEM = ("你是一个能调用工具解决问题的助手。"
          "涉及事实信息（时间、天气、计算）时必须先调工具，不要猜。")

def run_agent(user_input: str, max_turns: int = 8) -> str:
    history = [{"role": "system", "content": SYSTEM},
               {"role": "user", "content": user_input}]
    for turn in range(1, max_turns + 1):
        print(f"---- 第 {turn} 轮 ----")
        msg = client.chat.completions.create(
            model=MODEL, messages=history, tools=TOOLS,
        ).choices[0].message

        if not msg.tool_calls:            # 不再要工具 → 给出了最终回答
            return msg.content

        # 把"模型要求调用"这条也写进历史，否则服务端对账报错
        history.append({"role": "assistant", "tool_calls": [
            {"id": t.id, "type": "function",
             "function": {"name": t.function.name,
                          "arguments": t.function.arguments}}
            for t in msg.tool_calls]})

        for t in msg.tool_calls:          # 执行本轮每个工具调用
            name, args = t.function.name, json.loads(t.function.arguments)
            print(f"  调用 {name}{args}")
            try:
                result = DISPATCH[name](**args)
            except Exception as e:
                result = {"error": str(e)}  # 报错也回传：模型看到错误会自己修正
            history.append({"role": "tool", "tool_call_id": t.id,
                            "content": json.dumps(result, ensure_ascii=False)})
    return "达到最大轮数，任务未完成。"

if __name__ == "__main__":
    print("Agent 启动。试试：现在离明天整整一周还剩多少小时？（回车退出）")
    while True:
        q = input("\n任务> ").strip()
        if not q:
            break
        print("\n结论：", run_agent(q))