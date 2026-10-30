from config import create_nvidia_client

client = create_nvidia_client()
MODEL= "nvidia/nemotron-3.5-super-vl-120b-a12b"
SYSTEM="你是一个中文助手，回答只会用科举八股文"

history = [{"role": "system", "content": SYSTEM}]
print("欢迎使用中文助手！(直接回车退出)")

while True:
    user_input = input("\n用户: ").strip()
    if not user_input:
        break

    history.append({"role": "user", "content": user_input})

    print("正在请求模型...", flush=True)
    resp =  client.chat.completions.create(
        model=MODEL,messages=history)
    answer = resp.choices[0].message.content
    print(f"\n助手: {answer}")
    print(f"(token:输入{resp.usage.prompt_tokens},输出{resp.usage.completion_tokens},总计{resp.usage.total_tokens})")

    history.append({"role": "assistant", "content": answer})
