# LangGraph/app/agents/reviewer.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from typing import Any
from pydantic import BaseModel, Field, SecretStr
from app.core.config import settings
from app.core.state import IntelligenceState

# 1. 定义极其严格的“审稿结果”数据结构 (Pydantic Model)
class ReviewResult(BaseModel):
    is_pass: bool = Field(description="文章是否合格，具备深度和实质性技术细节？合格为 True，打回为 False。")
    feedback: str = Field(description="如果不合格，给出尖锐的修改建议；如果合格，简单评价一下。")

# 2. 初始化你的大模型 (设置 lower temperature 比如 0.1，让它保持客观理智)
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=SecretStr(settings.DEEPSEEK_API_KEY),
    base_url="https://api.deepseek.com",
    temperature=0.1
)


async def reviewer_node(state: IntelligenceState) -> dict[str, Any]:
    print("====== [NODE] Reviewer 开始交叉审阅... ======")
    
    draft = state.get("draft", "")
    current_revision = state.get("revision_count", 0)
    
    # 逻辑 A：防死循环机制
    # 如果 current_revision >= 2，说明已经改了太多次，直接放行 (返回 is_pass: True 和 revision_count 加 1)
    if current_revision >= 2:
        print("[Reviewer] 已经修改达到上限，强行通过！")
        return {"is_pass":True, "feedback":"达到最大修改次数，强制通过。", "revision_count":1}
    
    # 逻辑 B：拼装 Prompt
    # 写一个 SystemMessage：告诉它是一个苛刻的技术主编。
    # 写一个 HumanMessage：把 draft 塞进去让它读。
    parser = JsonOutputParser(pydantic_object=ReviewResult)
    format_instructions = parser.get_format_instructions()

    prompt = [
        SystemMessage(content=f"你是一个极其严苛的顶级AI技术博客主编。如果文章像口水文、仅仅是罗列没有见解，你必须打回并明确指出缺失的部分！\n\n【必须严格遵守的输出格式要求】：\n{format_instructions}"),
        HumanMessage(content=f"请审查以下技术报告：\n\n{draft}")
        ]

    # 逻辑 C：获取判定结果
    # review_result = await structured_llm.ainvoke(prompt)
    review = await llm.ainvoke(prompt)

    review_json = parser.invoke(review)

    is_pass = review_json["is_pass"]
    feedback = review_json["feedback"]

    # 逻辑 D：返回修改后的 State 字典
    # 把 review_result里的 is_pass, feedback，以及 current_revision + 1 组装成字典 return 出去。
    print(f"[Reviewer] 审阅结果：{'✅ 通过' if is_pass else '❌ 打回'}。反馈：{feedback}")

    update_state = {
        "is_pass": is_pass,
        "feedback": feedback,
        "revision_count": 1
        }
    
    if not is_pass:
        update_state["deep_dives"] = "CLEAR"
        
    return update_state