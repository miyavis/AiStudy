# -*- coding: utf-8 -*-
"""minbpe 5 分钟上手实验（配合《导读-Tokenizer.md》使用）。

只依赖标准库。做三件事：
1) 在你的文档上训练一个小 BPE 分词器，肉眼看合并过程
2) 验证 encode/decode 完美可逆
3) 实测"中文比英文费 token"——原理篇 1.2 的亲手验证

运行：从 本目录 运行  python 00_train_demo.py
"""
import glob
import os
from minbpe.basic import BasicTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- 1. 拼语料：agent-教程 目录下的所有文档/代码（两卷共建一个词表） ----------
corpus_root = os.path.normpath(os.path.join(HERE, "..", ".."))   # → agent-教程
corpus_paths = []
for root, _dirs, files in os.walk(corpus_root):
    for name in files:
        if name.endswith((".md", ".txt", ".py")) and "minbpe" not in root:
            corpus_paths.append(os.path.join(root, name))

text = ""
for p in corpus_paths:
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        text += f.read() + "\n"
print(f"语料：{len(corpus_paths)} 个文件，共 {len(text)} 字符")

# ---------- 2. 训练：256 个基础字节 → 每次合并产出一个新 token ----------
tok = BasicTokenizer()
tok.train(text, vocab_size=288, verbose=True)   # 32 步合并，verbose 看每一步
print(f"\n训练完成：merges = {len(tok.merges)} 条  vocab = {len(tok.vocab)} 个 token")

# ---------- 3. 可逆性验证：这行断言通过 = tokenizer 工程合格 ----------
sample = "宫里的事，凡人不知道。(A quick test!)"
ids = tok.encode(sample)
assert tok.decode(ids) == sample, "解码不回原文，实现有 bug"
print(f"\n样例：{sample}")
print(f"→ 编码为 {len(ids)} 个 token：{ids}")
print(f"→ 解码回原文：{tok.decode(ids)}   [可逆性 OK]")
tok.save("my_tokenizer")   # 生成 my_tokenizer.model / .vocab，肉眼看 .vocab 文件
print("\n已保存 my_tokenizer.model / my_tokenizer.vocab —— 用记事本打开 vocab 看看每个 token 长什么样")

# ---------- 4. 中文 vs 英文 token 成本 ----------
cn = "这套分词器把文本切成模型能吃的最小单元"
en = "This tokenizer splits text into the smallest units a model can eat"
print(f"\n中文 {len(cn)} 字 → {len(tok.encode(cn))} token（平均 {len(tok.encode(cn))/len(cn):.2f} token/字）")
print(f"英文 {len(en)} 字符 → {len(tok.encode(en))} token（平均 {len(tok.encode(en))/len(en):.2f} token/字符）")
print("→ 语料里英文多，英文就占便宜；全中文语料训练后反过来。这就是词表的'偏向性'。")
