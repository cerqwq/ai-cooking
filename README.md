# 🍳 AI Cooking

AI烹饪工具，支持食谱生成、菜单规划、营养分析。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🍽️ 食谱生成
- 📅 周菜单规划
- 🥘 食材推荐
- 📊 营养分析
- 🔄 食谱转换
- 💡 烹饪技巧

## 🚀 快速开始

```bash
pip install openai

python tools.py
```

## 📖 使用

```python
from ai_cooking import create_tools

tools = create_tools()

# 生成食谱
recipe = tools.generate_recipe("宫保鸡丁", "川菜", "中等")

# 周菜单
menu = tools.generate_weekly_menu(preferences, 500)

# 食材推荐
recipes = tools.suggest_recipe_from_ingredients(["鸡肉", "土豆", "青椒"])

# 营养分析
nutrition = tools.analyze_nutrition("番茄炒蛋")

# 食谱转换
converted = tools.convert_recipe(recipe, "素食")

# 烹饪技巧
tips = tools.generate_cooking_tips("炒菜")
```

## 📁 项目结构

```
ai-cooking/
├── tools.py       # 烹饪工具核心
└── README.md
```

## 📄 许可证

MIT License
