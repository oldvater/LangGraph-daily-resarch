from app.core.state import IntelligenceState
from typing import Any, cast
from pydantic import BaseModel, Field, SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings

class PlannerOutput(BaseModel):
    themes: list[str] = Field(description="从原始新闻流中提炼出的 1 到 3 个最重要的技术趋势主题。")


def planner_node(state: IntelligenceState) -> dict[str, Any]:
    print("====== [NODE] Planner 开始工作 ======")
    
    raw_feeds = state.get("raw_feeds", [])
    feeds_text = "\n".join(raw_feeds)

    model = ChatOpenAI(
        model="deepseek-chat",
        api_key=SecretStr(settings.DEEPSEEK_API_KEY),
        base_url="https://api.deepseek.com",
        temperature=0.3
    ).with_structured_output(PlannerOutput, method="json_mode")

    # 🌟 3. 编写 Prompt 模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个眼光极度挑剔的科技主编。今天前端记者爬取了数十条新闻（raw_feeds）。
        请你对它们进行严格筛选和归类，只挑选出今天绝对不容错过的、最具颠覆性的 1 到 3 个核心技术趋势提取为深入调研的 Topic。
         （必须包含具体的产品名称/实体名，不要过度抽象！例如：'LangChain发布的最新版本特性' 优于 'AI框架迭代'）。
         必须以 JSON 格式输出，且 JSON 必须包含一个且仅包含一个键名为 "themes"，其值为字符串列表 (list[str])。
         """),
        ("human", "今日新闻流: {input_text}")
    ])
    
    run_chain = prompt | model
    result = cast(PlannerOutput, run_chain.invoke({"input_text": feeds_text}))
    
    # 🌟 你的任务 3：把你提取的假主题，组装成一个字典 `return` 出去
    # 想一想：你的字典的 key 应该叫什么，才能精确地更新 IntelligenceState 里的东西？
    return {"themes": result.themes}