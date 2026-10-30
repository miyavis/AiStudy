import os

from openai import OpenAI


def get_nvidia_api_key() -> str:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 NVIDIA_API_KEY 环境变量")
    return api_key


def create_nvidia_client() -> OpenAI:
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=get_nvidia_api_key(),
        timeout=60.0,
    )
