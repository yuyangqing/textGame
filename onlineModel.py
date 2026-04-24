import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()
# 读取环境变量
api_key = os.environ.get("API_KEY")
base_url = os.environ.get("BASE_URL")
model = os.environ.get("MODEL")

client = OpenAI(api_key=api_key, base_url=base_url)

# 发起对话请求
response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一个有用的助手。'},
            {'role': 'user', 'content': '给出快速排序算法的python实现。'}
        ],
        temperature=0.7
    )
print(response.choices[0].message.content)