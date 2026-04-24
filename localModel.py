from openai import OpenAI
import time

# 初始化客户端
client = OpenAI(
    base_url='http://localhost:11434/v1',
    # Ollama 不需要真正的 Key，但不能留空
    api_key='ollama',
)

# 记录开始时间
start_time = time.time()

# 发起对话请求
response = client.chat.completions.create(
    model="qwen:7b",
    messages=[
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "你好，请简单介绍一下你自己。"},
    ]
)

# 记录结束时间
end_time = time.time()

# 计算运行时间
execution_time = end_time - start_time

print(response.choices[0].message.content)
print(f"运行时间：{execution_time:.2f} 秒")
