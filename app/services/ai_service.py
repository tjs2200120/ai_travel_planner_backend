import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import dashscope
from dashscope import Generation
from ..core.config import settings


class AIService:
    """AI 服务 - 通义千问集成"""

    def __init__(self):
        dashscope.api_key = settings.DASHSCOPE_API_KEY

    def generate_trip_plan(
        self,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        budget: Optional[float],
        traveler_count: int,
        preferences: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        生成旅行计划

        Args:
            destination: 目的地
            start_date: 开始日期
            end_date: 结束日期
            budget: 预算
            traveler_count: 同行人数
            preferences: 旅行偏好

        Returns:
            AI 生成的旅行计划（JSON 格式）
        """
        # 计算旅行天数
        days = (end_date - start_date).days + 1

        # 构建提示词
        prompt = self._build_trip_prompt(
            destination, days, budget, traveler_count, preferences
        )

        try:
            # 调用通义千问 API
            response = Generation.call(
                model="qwen-max",
                prompt=prompt,
                result_format="message",
            )

            if response.status_code == 200:
                content = response.output.choices[0].message.content
                # 解析 AI 返回的 JSON
                return self._parse_ai_response(content, start_date, days)
            else:
                raise Exception(f"AI API 调用失败: {response.message}")

        except Exception as e:
            # 如果 AI 服务失败，返回一个基础模板
            return self._generate_fallback_plan(destination, start_date, days, budget)

    def _build_trip_prompt(
        self,
        destination: str,
        days: int,
        budget: Optional[float],
        traveler_count: int,
        preferences: Optional[Dict[str, Any]],
    ) -> str:
        """构建 AI 提示词"""

        budget_text = f"{budget}元" if budget else "不限"
        preferences_text = ""
        if preferences:
            pref_items = []
            if preferences.get("interests"):
                pref_items.append(f"兴趣：{', '.join(preferences['interests'])}")
            if preferences.get("travel_style"):
                pref_items.append(f"旅行风格：{preferences['travel_style']}")
            if preferences.get("accommodation_type"):
                pref_items.append(f"住宿偏好：{preferences['accommodation_type']}")
            preferences_text = "，".join(pref_items) if pref_items else "无特殊偏好"
        else:
            preferences_text = "无特殊偏好"

        prompt = f"""
请为用户生成一份详细的旅行计划，要求如下：

旅行信息：
- 目的地：{destination}
- 旅行天数：{days}天
- 同行人数：{traveler_count}人
- 预算：{budget_text}
- 偏好：{preferences_text}

请生成一个包含以下信息的JSON格式旅行计划：
1. 每天的详细行程安排
2. 推荐的景点（包括名称、位置、建议游玩时长、大致费用）
3. 推荐的餐厅（包括名称、位置、特色菜、人均消费）
4. 住宿建议（包括酒店名称、位置、价格区间）
5. 交通方式建议
6. 预算分配建议

返回格式示例：
{{
  "summary": "行程总结",
  "total_estimated_cost": 预计总费用,
  "days": [
    {{
      "day": 1,
      "title": "第一天标题",
      "activities": [
        {{
          "time": "09:00",
          "type": "attraction",
          "name": "景点名称",
          "location": "详细地址",
          "duration": 120,
          "cost": 100,
          "description": "简短描述"
        }},
        {{
          "time": "12:00",
          "type": "restaurant",
          "name": "餐厅名称",
          "location": "详细地址",
          "cost": 80,
          "description": "特色菜品"
        }}
      ]
    }}
  ],
  "budget_breakdown": {{
    "accommodation": 住宿费用,
    "food": 餐饮费用,
    "transport": 交通费用,
    "attraction": 景点门票,
    "shopping": 购物预算,
    "other": 其他费用
  }},
  "tips": ["实用建议1", "实用建议2"]
}}

请确保返回有效的 JSON 格式，不要包含其他文字说明。
"""
        return prompt

    def _parse_ai_response(
        self, content: str, start_date: datetime, total_days: int
    ) -> Dict[str, Any]:
        """解析 AI 响应"""
        try:
            # 尝试从内容中提取 JSON
            # 有时 AI 可能会在 JSON 前后添加一些文字说明
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                data = json.loads(json_str)

                # 为每天添加实际日期
                if "days" in data:
                    for idx, day in enumerate(data["days"]):
                        day["date"] = (start_date + timedelta(days=idx)).isoformat()

                return data
            else:
                raise ValueError("无法从响应中提取 JSON")

        except Exception as e:
            # 解析失败，返回基础计划
            return self._generate_fallback_plan(
                "未知目的地", start_date, total_days, None
            )

    def _generate_fallback_plan(
        self, destination: str, start_date: datetime, days: int, budget: Optional[float]
    ) -> Dict[str, Any]:
        """生成后备计划（当 AI 服务不可用时）"""

        daily_activities = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            daily_activities.append(
                {
                    "day": i + 1,
                    "date": day_date.isoformat(),
                    "title": f"第{i + 1}天 - {destination}探索",
                    "activities": [
                        {
                            "time": "09:00",
                            "type": "attraction",
                            "name": f"{destination}主要景点",
                            "location": destination,
                            "duration": 180,
                            "cost": 100,
                            "description": "建议提前查询当地热门景点",
                        },
                        {
                            "time": "12:00",
                            "type": "restaurant",
                            "name": "当地特色餐厅",
                            "location": destination,
                            "cost": 80,
                            "description": "品尝当地美食",
                        },
                        {
                            "time": "14:00",
                            "type": "attraction",
                            "name": f"{destination}次要景点",
                            "location": destination,
                            "duration": 120,
                            "cost": 50,
                            "description": "继续探索",
                        },
                    ],
                }
            )

        return {
            "summary": f"{destination}{days}日游基础行程",
            "total_estimated_cost": budget if budget else days * 500,
            "days": daily_activities,
            "budget_breakdown": {
                "accommodation": (budget or days * 500) * 0.3,
                "food": (budget or days * 500) * 0.3,
                "transport": (budget or days * 500) * 0.2,
                "attraction": (budget or days * 500) * 0.15,
                "other": (budget or days * 500) * 0.05,
            },
            "tips": [
                "此为基础行程模板，请根据实际情况调整",
                "建议提前预订住宿和门票",
                "注意查看天气预报",
            ],
        }

    def analyze_budget(self, expenses: list, budget: float) -> Dict[str, Any]:
        """
        分析预算使用情况

        Args:
            expenses: 费用列表
            budget: 总预算

        Returns:
            预算分析结果
        """
        # 计算总支出
        total_spent = sum(exp.get("amount", 0) for exp in expenses)

        # 按分类统计
        category_spending = {}
        for exp in expenses:
            category = exp.get("category", "other")
            category_spending[category] = (
                category_spending.get(category, 0) + exp.get("amount", 0)
            )

        # 计算百分比
        spending_percentage = (total_spent / budget * 100) if budget > 0 else 0
        remaining = budget - total_spent

        return {
            "total_budget": budget,
            "total_spent": total_spent,
            "remaining": remaining,
            "spending_percentage": round(spending_percentage, 2),
            "category_breakdown": category_spending,
            "status": "over_budget"
            if total_spent > budget
            else "on_track"
            if spending_percentage < 90
            else "warning",
        }
