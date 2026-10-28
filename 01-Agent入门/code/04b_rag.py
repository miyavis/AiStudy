# -*- coding: utf-8 -*-
"""第 4 步 B：RAG 文档问答 —— 让模型回答"它没见过的事"。
五步：读语料 → 切块 → 向量化 → 检索 → 拼进 prompt。
把只有 docs/ 里才有的内容写进文档，再提问来验证检索链路。
"""
import os
import glob
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
CHUNK = 400       # 切块长度是最重要的检索参数：太小会碎，太大会不精准
OVERLAP = 50      # 相邻块重叠，避免答案恰好跨块被腰斩

# —— 第 1 步：读语料 ——
documents = {}
for path in glob.glob(os.path.join(DOCS_DIR, "**", "*.md"), recursive=True) \
        + glob.glob(os.path.join(DOCS_DIR, "**", "*.txt"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        documents[path] = f.read()

# —— 第 2 步：切块 ——
chunks, owners = [], []
for doc_name, text in documents.items():
    text = text.replace("\r\n", "\n")
    for i in range(0, max(len(text), 1), CHUNK - OVERLAP):
        pieces = text[i:i + CHUNK]
        if pieces.strip():
            chunks.append(pieces)
            owners.append(doc_name)
print(f"已加载 {len(documents)} 个文件，切出 {len(chunks)} 块")

# —— 第 3 步：向量化（bge-m3 把文字变成语义坐标）——
def embed(texts):
    return np.asarray([client.embeddings.create(
        model="bge-m3", input=[t]).data[0].embedding for t in texts])

vecs = embed(chunks)

# —— 第 4 步：检索（余弦相似度 top-k）——
def search(query: str, k: int = 4):
    qe = client.embeddings.create(model="bge-m3", input=[query]).data[0].embedding
    qe = np.asarray(qe)
    sims = (vecs @ qe) / (np.linalg.norm(vecs, axis=1) + 1e-9) / np.linalg.norm(qe)
    return [(int(i), float(sims[i])) for i in sims.argsort()[::-1][:k]]

SYSTEM = ("你只依据给定资料回答。资料中没有的信息就回答'资料未提及'，"
          "不要使用自有知识补充。")

while True:
    user = input("\n问题> ").strip()
    if not user:
        break
    hits = search(user)
    context = "\n---\n".join(
        f"【{os.path.basename(owners[i])} | 相似度 {s:.3f}】\n{chunks[i]}"
        for i, s in hits)
    print("（命中的块： "
          + ", ".join(f"{os.path.basename(owners[i])}({s:.2f})" for i, s in hits)
          + "）")                                      # 把检索变白盒
    answer = client.chat.completions.create(
        model="qwen3:8b",
        messages=[{"role": "system", "content": SYSTEM + "\n\n资料：\n" + context},
                  {"role": "user", "content": user}],
    ).choices[0].message.content
    print(answer)