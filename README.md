这是一个在终端运行AI生成的文字冒险游戏，欢迎体验~

1.安装 Python 3.8+
2.安装依赖包：
pip install -r requirements.txt
3.接入大模型(可选云端大模型或本地大模型)
    a.云端大模型：获取API密钥，替换下列参数（textGame.py）
      api_key = os.environ.get("API_KEY") # 你的API密钥
      base_url = os.environ.get("BASE_URL") # 你的API基础URL
      model = os.environ.get("MODEL") # 你的模型名称
    b.本地大模型：替换下列参数（textGame.py）
      base_url='http://localhost:11434/v1' # 本地大模型地址
      api_key='ollama' #非空即可
      model = os.environ.get("MODEL") # 你的模型名称
4.运行游戏：
python textGame.py

测试用例
冒险主题：魔法世界
冒险简介：这是一个隐藏在现代麻瓜世界之中的魔法社会，拥有自己的政府、经济体系、交通方式和教育机构。作为一个小巫师，你即将进入霍格沃兹魔法学校就读

冒险主题：修仙世界
冒险简介：天地灵气渐衰，“飞升”已成千年传说。修士分炼气、筑基、金丹、元婴、化神五境。上古秘境相继现世，正邪两道为争夺残存的成仙契机，暗流涌动。你走向青云宗山门，决心踏入修仙之途