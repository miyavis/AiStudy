from datetime import datetime, timedelta
from functools import lru_cache
import json
from pathlib import Path
import stat

from config import create_nvidia_client

MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b"


def getNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")


def getRecentFiles(directory, minutes=5):
    if minutes < 0:
        raise ValueError("minutes 不能小于 0")

    now = datetime.now().timestamp()
    cutoff = now - timedelta(minutes=minutes).total_seconds()
    recent_files = []
    for path in Path(directory).iterdir():
        file_stat = path.stat()
        if (
            stat.S_ISREG(file_stat.st_mode)
            and cutoff <= file_stat.st_mtime
        ):
            recent_files.append(str(path))
    return recent_files


DISPATCH = {"getRecentFiles": getRecentFiles, "get_now": getNow}


def tool_of(name, desc, props, required=None):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": props,
                "required": list(props) if required is None else required,
                "additionalProperties": False,
            },
        },
    }


@lru_cache(maxsize=1)
def get_client():
    return create_nvidia_client()

TOOLS = [
    tool_of(
        "getRecentFiles",
        "查询指定目录下最近修改的文件列表",
        {
            "directory": {"type": "string", "description": "目录路径"},
            "minutes": {
                "type": "integer",
                "description": "时间范围，单位为分钟",
                "minimum": 0,
            },
        },
        required=["directory"],
    ),
    tool_of("get_now", "获取当前日期、时间和星期几", {}),
]

SYSTEM = (
    "你是一个能调用工具解决问题的助手。"
    "涉及事实信息（时间、文件列表查询）时必须先调工具，不要猜。"
)


def execute_tool(name, arguments):
    try:
        args = json.loads(arguments)
    except json.JSONDecodeError as error:
        return {"error": f"工具参数不是有效 JSON：{error.msg}"}

    if not isinstance(args, dict):
        return {"error": "工具参数必须是 JSON 对象"}

    function = DISPATCH.get(name)
    if function is None:
        return {"error": f"未知工具：{name}"}

    try:
        return function(**args)
    except (OSError, TypeError, ValueError) as error:
        return {"error": str(error)}


def run_agent(user_input: str, max_turns: int = 8) -> str:
    if max_turns < 1:
        raise ValueError("max_turns 必须大于 0")

    history = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_input},
    ]
    for turn in range(1, max_turns + 1):
        print(f"---- 第 {turn} 轮 ----")
        msg = get_client().chat.completions.create(
            model=MODEL, messages=history, tools=TOOLS,
        ).choices[0].message

        if not msg.tool_calls:
            if msg.content is None:
                raise RuntimeError("模型未返回文本内容")
            return msg.content

        # 把"模型要求调用"这条也写进历史，否则服务端对账报错
        history.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in msg.tool_calls
            ],
        })

        for tool_call in msg.tool_calls:
            name, arguments = (
                tool_call.function.name,
                tool_call.function.arguments,
            )
            print(f"  调用 {name}{arguments}")
            result = execute_tool(name, arguments)
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
    return "达到最大轮数，任务未完成。"

if __name__ == "__main__":
    print("Agent 启动。试试：现在离明天整整一周还剩多少小时？（回车退出）")
    while True:
        q = input("\n任务> ").strip()
        if not q:
            break
        print("\n结论：", run_agent(q))