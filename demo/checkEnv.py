from config import create_nvidia_client

client = create_nvidia_client()

try:
    models = client.models.list()
    print("可用模型列表:")
    for model in models.data:
        print(f"- {model.id} - {model.owned_by} - {model.model_config}")
except Exception as e:
    print(f"获取模型列表失败: {e}")