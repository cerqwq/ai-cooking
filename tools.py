"""
AI Cooking - AI烹饪工具
支持食谱生成、菜单规划、营养分析
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AICookingTools:
    """
    AI烹饪工具
    支持：食谱、菜单、营养
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_recipe(self, dish_name: str, cuisine: str, difficulty: str) -> Dict:
        """生成食谱"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请生成{cuisine}菜系的{dish_name}食谱：

难度：{difficulty}

请返回JSON格式：
{{
    "name": "菜名",
    "servings": "份量",
    "prep_time": "准备时间",
    "cook_time": "烹饪时间",
    "ingredients": [{{"item": "食材", "amount": "用量"}}],
    "steps": ["步骤1", "步骤2"],
    "tips": ["小贴士"],
    "nutrition": {{"calories": 卡路里, "protein": "蛋白质", "carbs": "碳水", "fat": "脂肪"}}
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"recipe": content}

    def generate_weekly_menu(self, preferences: Dict, budget: float) -> Dict:
        """生成周菜单"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prefs_text = json.dumps(preferences, ensure_ascii=False)

        prompt = f"""请生成一周菜单：

偏好：{prefs_text}
预算：{budget}元

请返回JSON格式：
{{
    "weekly_menu": [
        {{"day": "周一", "breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}}
    ],
    "grocery_list": [{{"item": "食材", "amount": "用量", "estimated_cost": "预估费用"}}],
    "total_cost": "总费用"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"menu": content}

    def suggest_recipe_from_ingredients(self, ingredients: List[str]) -> Dict:
        """根据食材推荐食谱"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        ingredients_text = ", ".join(ingredients)

        prompt = f"""请根据以下食材推荐食谱：

食材：{ingredients_text}

请返回JSON格式：
{{
    "recipes": [
        {{"name": "菜名", "difficulty": "难度", "time": "时间", "description": "描述"}}
    ]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"recipes": content}

    def analyze_nutrition(self, meal: str) -> Dict:
        """分析营养"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请分析以下餐食的营养成分：

{meal}

请返回JSON格式：
{{
    "calories": 卡路里,
    "protein": "蛋白质",
    "carbs": "碳水化合物",
    "fat": "脂肪",
    "fiber": "纤维",
    "vitamins": ["维生素"],
    "assessment": "营养评价",
    "suggestions": ["改进建议"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"nutrition": content}

    def convert_recipe(self, recipe: str, dietary_restriction: str) -> str:
        """转换食谱"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请将以下食谱转换为{dietary_restriction}版本：

{recipe[:1000]}

要求：
1. 替换不兼容的食材
2. 保持风味
3. 说明替换原因"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        return response.choices[0].message.content

    def generate_cooking_tips(self, dish_type: str) -> List[str]:
        """生成烹饪技巧"""
        if not self.client:
            return ["LLM客户端未配置"]

        prompt = f"""请提供{dish_type}的烹饪技巧：

请返回JSON数组格式：["技巧1", "技巧2", ...]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return [response.choices[0].message.content]


def create_tools(**kwargs) -> AICookingTools:
    """创建烹饪工具"""
    return AICookingTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Cooking Tools")
    print()

    # 测试
    recipe = tools.generate_recipe("宫保鸡丁", "川菜", "中等")
    print(json.dumps(recipe, ensure_ascii=False, indent=2))
