import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()
# 读取环境变量
api_key = os.environ.get("API_KEY")
base_url = os.environ.get("BASE_URL")
model = os.environ.get("MODEL")

client = OpenAI(api_key=api_key, base_url=base_url)

def generate_adventure_game():
    print("🎮 欢迎来到AI文字冒险游戏！")
    print("="*50)
    
    # 获取用户输入的主题和简介
    theme = input("请输入冒险主题（如：魔法世界、奇幻世界、古代权谋等）: ")
    brief = input("请输入冒险简介（背景设定）: ")
    
    print("\n正在生成您的冒险故事...")
    
    # 初始提示
    initial_prompt = f"""
    你是一个专业的文字冒险游戏创作者。根据以下设定创作一个引人入胜的冒险故事：
    主题：{theme}
    背景：{brief}
    
    请按照以下格式输出：
    剧情介绍：
    [一段引人入胜的开场剧情描述]
    
    请选择接下来的行动：
    A. [选项A描述]
    B. [选项B描述]
    C. [选项C描述]
    """
    
    current_story = ""
    story_history = []
    
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
                    {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，善于创造引人入胜的故事。'},
                    {'role': 'user', 'content': initial_prompt}
                ],
                temperature=0.8
            )
            response_text = completion.choices[0].message.content
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
                1.请根据这个选择继续故事情节，保证情节连贯性和一致性
                2.提供三个选项，不要重复以前的选择，始终创造推进故事的新选项
                3.按照以下格式输出：
                剧情介绍：
                请选择接下来的行动：
                A. [选项A描述]
                B. [选项B描述]
                C. [选项C描述]
                """
            else:
                # 玩家选择预设选项
                selected_option_content = ""
                for line in options:
                    if line.startswith(f"{user_choice}."):
                        selected_option_content = line
                        break
                selected_choice = f"""
                玩家选择了{selected_option_content}
                1.请根据这个选择继续故事情节，保证情节连贯性和一致性
                2.提供三个选项，不要重复以前的选择，始终创造推进故事的新选项
                3.按照以下格式输出：
                剧情介绍：
                请选择接下来的行动：
                A. [选项A描述]
                B. [选项B描述]
                C. [选项C描述]
                """

            
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，善于根据玩家的选择推进故事发展。'},
                    {'role': 'user', 'content': f"当前剧情：\n{current_story}\n\n{selected_choice}"}
                ],
                temperature=0.8
            )
            response_text = completion.choices[0].message.content
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️ 本轮AI生成耗时: {execution_time:.2f}秒")
        
        # 解析AI响应，提取剧情和选项
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
        
        current_story = '\n'.join(story_part).replace('剧情介绍：', '').strip()
        print(f"\n📖 故事进展：\n{current_story}")
        
        # 判断是否进入结局阶段
        if round_num <= 3:
            # 前三轮必定显示选项
            print("\n🎯 请选择接下来的行动：")
            for option in options:
                if option.startswith('A.') or option.startswith('B.') or option.startswith('C.'):
                    print(option)
            print("D. 输入自定义选项")
        else:
            # 第四轮开始，按概率判断是否进入结局
            # 随着轮数增加，结束游戏的概率也逐渐增大
            end_probability = min(0.3 + (round_num - 4) * 0.1, 0.8)  # 递增概率，最高80%
            
            if random.random() < end_probability:
                print(f"\n🎲 概率判定：{end_probability*100:.0f}% 概率触发结局")
                # 跳出循环，进入结局阶段
                break
            else:
                print(f"\n🎲 概率判定：继续冒险 ({(1-end_probability)*100:.0f}% 概率)")
                # 继续显示选项
                print("\n🎯 请选择接下来的行动：")
                for option in options:
                    if option.startswith('A.') or option.startswith('B.') or option.startswith('C.'):
                        print(option)
                print("D. 输入自定义选项")
    
    # 生成结局
    print(f"\n{'='*20} 最终结局 {'='*20}")
    start_time = time.time()
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一个专业的文字冒险游戏创作者，负责为玩家的故事创作一个精彩的结局。'},
            {'role': 'user', 'content': f"这是冒险的过程：\n{current_story}\n\n请为这个故事创作一个精彩的结局。"}
        ],
        temperature=0.7
    )
    
    ending = completion.choices[0].message.content
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n📖 最终结局：\n{ending}")
    print(f"\n⏱️ 结局生成耗时: {execution_time:.2f}秒")
    
    print("\n🎉 冒险结束！感谢游玩！")

if __name__ == "__main__":
    generate_adventure_game()