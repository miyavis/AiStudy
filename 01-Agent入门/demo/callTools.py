import ast
import json
import operator

from config import create_nvidia_client

client = create_nvidia_client()
MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b"
SYSTEM = "你是一个中文助手。计算任务时，使用对应工具。"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行加减乘除和括号等基础数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "只包含数字、括号和 + - * / // % ** 的数学表达式",
                    },
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
]


def calculate(expression: str) -> int | float:
    if len(expression) > 200:
        raise ValueError("表达式不能超过 200 个字符")

    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    unary_operators = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("指数绝对值不能超过 100")
            return binary_operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("表达式包含不支持的内容")

    return evaluate(ast.parse(expression, mode="eval"))


questions = "计算：8 % 3 + 2 * (5 - 1) * 2的结果是多少？"
first = (
    client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": questions},
        ],
        tools=tools,
    )
    .choices[0]
    .message
)
print(f"模型输出: {first.content}")
print("第 1 次返回 tool_calls：", first.tool_calls)

tc = first.tool_calls[0]
args = json.loads(tc.function.arguments)
result = calculate(args["expression"])
print(f"直接调用计算结果: {result}")

answer = (
    client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": questions},
               first.model_dump(exclude_none=True),
            # {
            #     "role": "assistant",
            #     "tool_calls": [
            #         {
            #             "id": tc.id,
            #             "type": "function",
            #             "function": {
            #                 "name": tc.function.name,
            #                 "arguments": tc.function.arguments,
            #             },
            #         }
            #     ],
            # },
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps({"result": result}),
            },
        ],
        tools=tools,
    )
    .choices[0]
    .message
)
print(f"最终回答: {answer.content}")
