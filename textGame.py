import os
import time
import random
import json
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()
# 读取环境变量
api_key = os.environ.get("API_KEY")
base_url = os.environ.get("BASE_URL")
model = os.environ.get("MODEL")

client = OpenAI(api_key=api_key, base_url=base_url)

def parse_json_response(response_text):
    """解析JSON格式的响应"""
    try:
        # 尝试找到JSON块
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # 如果找不到JSON格式，则使用原始解析方法作为备选
    lines = response_text.split('\n')
    story_part = []
    options = []
    
    in_story = True
    for line in lines:
        line = line.strip()
        if line.startswith('A.') or line.startswith('B.') or line.startswith('C.'):
            in_story = False
            options.append(line)
        elif '请选择接下来的行动：' in line:
            in_story = False
        elif in_story and line:
            story_part.append(line)
    
    # 返回模拟的JSON结构
    return {
        "story": "\n".join(story_part),
        "summary": "剧情摘要",
        "options": options
    }

def generate_adventure_game():
    print("🎮 欢迎来到AI文字冒险游戏！")
    print("="*50)
    
    # 获取用户输入的主题和简介
    theme = input("请输入冒险主题（如：魔法世界、奇幻世界、古代权谋等）: ")
    brief = input("请输入冒险简介（背景设定）: ")
    
    print("\n正在生成您的冒险身份...")
    
    # 生成三个身份
    character_prompt = f"""
    你是一个专业的身份设计师。根据以下冒险设定设计三个独特的角色身份，描述简练：
    主题：{theme}
    背景：{brief}
    
    输出是JSON格式：
    {{
        "characters": [
            {{"id": "A", "identity": "角色身份A", "description": "身份A特点和能力描述"}},
            {{"id": "B", "identity": "角色身份B", "description": "身份B特点和能力描述"}},
            {{"id": "C", "identity": "角色身份C", "description": "身份C特点和能力描述"}}
        ]
    }}
    """
    
    character_completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一个专业的身份设计师，擅长根据世界观创造有特色的人物身份。输出是JSON格式。'},
            {'role': 'user', 'content': character_prompt}
        ],
        temperature=0.8
    )
    
    character_data = parse_json_response(character_completion.choices[0].message.content)
    
    print(f"\n🎭 身份介绍：\n{character_data.get('introduction', '')}")
    print("\n🎯 可选角色身份：")
    for char in character_data.get('characters', []):
        print(f"{char['id']}. {char['identity']} - {char['description']}")
    print("D. 自定义角色身份")
    
    # 让玩家选择角色
    character_choice = input("\n请选择一个角色身份 (A/B/C/D): ").upper()
    while character_choice not in ['A', 'B', 'C', 'D']:
        character_choice = input("无效选择，请输入 A、B、C 或 D: ").upper()
    
    if character_choice == 'D':
        # 玩家自定义角色
        custom_character = input("请输入您的自定义角色身份和特点: ")
        player_character = custom_character
    else:
        # 找到选择的角色
        chosen_char = next((c for c in character_data.get('characters', []) if c['id'] == character_choice), None)
        if chosen_char:
            player_character = f"{chosen_char['identity']}"
        else:
            player_character = "未知身份"
    
    print(f"\n👤 您选择的身份是：{player_character}")
    
    # 构建初始提示，包含角色信息
    initial_prompt = f"""
    你是一个专业的文字冒险游戏创作者。根据以下设定创作一个引人入胜的冒险故事，以第二人称为主语：
    主题：{theme}
    背景：{brief}
    玩家身份：{player_character}
    
    输出是JSON格式：
    {{
        "story": "一段引人入胜的开场剧情描述，考虑玩家身份",
        "summary": "一句话总结当前剧情要点",
        "options": [
            {{"id": "A", "description": "选项A描述"}},
            {{"id": "B", "description": "选项B描述"}},
            {{"id": "C", "description": "选项C描述"}}
        ]
    }}
    """
    
    current_story = ""
    story_summary = ""
    history_summaries = []  # 存储历史摘要
    
    # 最大轮次数
    max_rounds = 15  # 设置一个最大轮数限制
    
    for round_num in range(1, max_rounds + 1):
        print(f"\n{'='*20} 第{round_num}轮 {'='*20}")
        
        start_time = time.time()
        
        if round_num == 1:
            # 第一轮：生成初始剧情
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，善于创造引人入胜的故事，以第二人称为主语。输出是JSON格式。'},
                    {'role': 'user', 'content': initial_prompt}
                ],
                temperature=0.8
            )
            response_data = parse_json_response(completion.choices[0].message.content)
        else:
            # 后续轮次：根据玩家选择继续故事
            user_choice = input("\n请选择一个选项 (A/B/C/D): ").upper()
            while user_choice not in ['A', 'B', 'C', 'D']:
                user_choice = input("无效选择，请输入 A、B、C或D: ").upper()
            
            if user_choice == 'D':
                # 玩家输入自定义选项
                custom_choice = input("请输入您的自定义行动: ")
                selected_choice = f"""
                玩家选择了自定义行动：{custom_choice}
                
                输出是JSON格式：
                {{
                    "story": "根据玩家选择继续创造前后连贯、引人入胜的故事情节",
                    "summary": "一句话总结当前剧情要点",
                    "options": [
                        {{"id": "A", "description": "选项A描述"}},
                        {{"id": "B", "description": "选项B描述"}},
                        {{"id": "C", "description": "选项C描述"}}
                    ]
                }}
                """
            else:
                # 玩家选择预设选项
                selected_option_desc = ""
                for opt in response_data.get('options', []):
                    if opt['id'] == user_choice:
                        selected_option_desc = opt['description']
                        break
                
                selected_choice = f"""
                玩家选择了{selected_option_desc}
                
                输出是JSON格式：
                {{
                    "story": "根据玩家选择继续创造前后连贯、引人入胜的故事情节",
                    "summary": "一句话总结当前剧情要点",
                    "options": [
                        {{"id": "A", "description": "选项A描述"}},
                        {{"id": "B", "description": "选项B描述"}},
                        {{"id": "C", "description": "选项C描述"}}
                    ]
                }}
                """
            
            # 更新历史摘要列表，保留最新的10条
            if story_summary:
                history_summaries.append(story_summary)
                if len(history_summaries) > 10:
                    history_summaries.pop(0)  # 移除最旧的摘要
            
            # 构建历史摘要字符串
            history_summary_text = "\n".join([f"{i+1}. {summary}" for i, summary in enumerate(history_summaries)])
            
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，善于根据玩家的选择推进故事发展，以第二人称为主语。输出是JSON格式。'},
                    {'role': 'user', 'content': f"当前剧情摘要：\n{story_summary}\n\n历史摘要：\n{history_summary_text}\n\n玩家选择：{selected_choice}"}
                ],
                temperature=0.8
            )
            response_data = parse_json_response(completion.choices[0].message.content)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️ 本轮AI生成耗时: {execution_time:.2f}秒")
        
        # 提取数据
        current_story = response_data.get("story", "")
        story_summary = response_data.get("summary", "")
        options = response_data.get("options", [])
        
        print(f"\n📖 故事进展：\n{current_story}")
        
        # 判断是否进入结局阶段
        if round_num <= 5:
            # 前三轮必定显示选项
            print("\n🎯 请选择接下来的行动：")
            for option in options:
                print(f"{option['id']}. {option['description']}")
            print("D. 输入自定义选项")
        else:
            # 第六轮开始，按概率判断是否进入结局
            # 随着轮数增加，结束游戏的概率也逐渐增大
            end_probability = min(0.3 + (round_num - 6) * 0.1, 0.8)  # 递增概率，最高80%
            
            if random.random() < end_probability:
                print(f"\n🎲 概率判定：{end_probability*100:.0f}% 概率触发结局")
                # 跳出循环，进入结局阶段
                break
            else:
                print(f"\n🎲 概率判定：继续冒险 ({(1-end_probability)*100:.0f}% 概率)")
                # 继续显示选项
                print("\n🎯 请选择接下来的行动：")
                for option in options:
                    print(f"{option['id']}. {option['description']}")
                print("D. 输入自定义选项")
    
    # 生成结局
    print(f"\n{'='*20} 最终结局 {'='*20}")
    start_time = time.time()
    
    # 结局使用历史摘要
    history_summary_text = "\n".join([f"{i+1}. {summary}" for i, summary in enumerate(history_summaries)])
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，负责为玩家的故事创作一个精彩的结局，以第二人称为主语。'},
            {'role': 'user', 'content': f"请为这个故事创作一个精彩的结局。\n\n这是故事的过程摘要：\n{story_summary}"}
        ],
        temperature=0.7
    )
    
    ending = completion.choices[0].message.content
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n📖 最终结局：\n{ending}")
    print(f"\n⏱️ 结局生成耗时: {execution_time:.2f}秒")
    
    print("\n🎉 冒险结束！感谢游玩！")

def ifGoToEnding(round_num):
    # 判断是否进入结局阶段
    if round_num <= 5:
        # 前五轮必定显示选项
        return False
    else:
        # 第六轮开始，按概率判断是否进入结局
        # 随着轮数增加，结束游戏的概率也逐渐增大
        end_probability = min(0.3 + (round_num - 6) * 0.1, 0.8)
        if random.random() < end_probability:
            print(f"\n🎲 概率判定：{end_probability*100:.0f}% 概率触发结局")
            # 跳出循环，进入结局阶段
            return True
        else:
            print(f"\n🎲 概率判定：继续冒险 ({(1-end_probability)*100:.0f}% 概率)")
            return False


if __name__ == "__main__":
    generate_adventure_game()