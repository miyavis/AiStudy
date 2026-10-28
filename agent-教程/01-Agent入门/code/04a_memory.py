# -*- coding: utf-8 -*-
"""第 4 步 A：SQLite 长期记忆 —— 跨运行记得你的聊天机器人。
观察点：退出重进再问"我叫什么"，它记得；/记忆 查看数据库条数。
"""
import sqlite3
import datetime
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:8b"
DB = "chat_memory.db"
SYSTEM = "你是一个简洁的中文助手。请参考对话历史中的既有偏好和事实作答。"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created TEXT NOT NULL)""")

def load_history(limit=50):
    """每次启动读最近 N 条 —— limit 就是你的第一代"记忆策略"参数。
    太小丢早期偏好，太大烧 token。生产做法：摘要 + 最近 N 条分层。
    """
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT role, content FROM messages "
                       "ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def save(role, content):
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO messages(role, content, created) VALUES(?, ?, ?)",
                    (role, content, datetime.datetime.now().isoformat()))

def main():
    init_db()
    history = [{"role": "system", "content": SYSTEM}] + load_history()
    print("记忆机器人（回车退出；/记忆 查看已存条数）。跨运行记得你的话。")
    while True:
        user = input("\n你：").strip()
        if not user:
            break
        if user == "/记忆":
            with sqlite3.connect(DB) as con:
                n = con.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
            print(f"数据库已存 {n} 条消息（{DB}）")
            continue
        save("user", user)                       # 先存
        history.append({"role": "user", "content": user})
        answer = client.chat.completions.create(
            model=MODEL, messages=history).choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        save("assistant", answer)                # 后存
        print(f"助手：{answer}")

if __name__ == "__main__":
    main()