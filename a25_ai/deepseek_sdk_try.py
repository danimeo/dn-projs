from deepseek import DeepSeekClient

# 初始化客户端
client = DeepSeekClient(api_key="your_existing_api_key")

# 创建新的 API Key
new_api_key = client.create_api_key(name="my_new_key", permissions=["read", "write"])

print("New API Key:", new_api_key)
