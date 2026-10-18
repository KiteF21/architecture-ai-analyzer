import os
import json
from openai import OpenAI

api_key = os.getenv("DEEPSEEK_API_KEY")

if api_key is None:
    print("没有找到 DEEPSEEK_API_KEY")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
    timeout=30.0,
    max_retries=0
)

def analyze_building(building_name):
    prompt = f"""
请只分析这一个建筑案例：{building_name}

要求：
1. 只返回合法 JSON
2. 最外层必须是一个 JSON 对象 {{}}
3. 不要返回 JSON 数组 []
4. 不要添加任何解释文字
5. 不要使用 Markdown 代码块
6. 必须包含以下所有字段
7. features 和 strategies 必须是数组

格式如下：
{{
    "name": "",
    "location": "",
    "architect": "",
    "type": "",
    "features": [],
    "strategies": []
}}
"""

    try:
        response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
        )
        print(f"DeepSeek 返回完成：{building_name}")

    except Exception as e:
        print(f"{building_name} 调用 AI 失败：")
        print(type(e).__name__)
        print(e)
        return None

    

    result = response.choices[0].message.content
    try :
        data = json.loads(result)
        
    except json.JSONDecodeError:
        print(f"无法解析 {building_name} 的响应")
        return None
    
    if not isinstance(data, dict):
        print(f"{building_name} 返回的数据不是 dict")
        return None
    
    return data

building_input = input("请输入多个建筑名称，用逗号隔开：")
building_input = building_input.replace("，",",")
buildings = building_input.split(",")

output_dir = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(output_dir, exist_ok=True)

for building_name in buildings:
    building_name = building_name.strip()

    if not building_name:
        continue

    print(f"正在分析：{building_name}")
    
    data = analyze_building(building_name)
     
    if data is None:
        continue
    print(data["name"])
     


    file_name = os.path.join(output_dir, f"{building_name}.json")
     
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

