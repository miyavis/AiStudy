# 取自 karpathy/minbpe（gpt4 需要 tiktoken，故改为可选导入，Basic/Regex 不受影响）
from .basic import BasicTokenizer
from .regex import RegexTokenizer

try:
    from .gpt4 import GPT4Tokenizer
except ImportError:
    # 未安装 tiktoken 时 GPT4Tokenizer 不可用（学习用 Basic 就够了）
    pass
