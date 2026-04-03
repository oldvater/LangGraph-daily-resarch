# LangGraph/app/agents/synthesizer.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Any
from app.core.config import settings
from pydantic import SecretStr
from app.core.state import IntelligenceState

# 你可能需要在这里定义好 llm 实例
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=SecretStr(settings.DEEPSEEK_API_KEY),
    base_url="https://api.deepseek.com",
    temperature=0.3
)


async def synthesizer_node(state: IntelligenceState) -> dict[str, Any]:
    print("====== [NODE] Synthesizer 主编开始整合所有深度报告... ======")
    
    # 1. 拿数据：themes 和 deep_dives
    themes = state["themes"]
    deep_dives = state["deep_dives"]

    theme_text = "\n".join(themes)
    deep_dives_text = ""
    for dive in deep_dives:
        topic = dive["topic"]
        content = dive["content"]
        deep_dives_text += f"\n\n###收集的主题：{topic}\n{content}"
    
    # 2. 拼装 prompt：
    
    # SystemMessage 可以说："你是一个资深的技术报告主编..."
    # HumanMessage 里要把 plan 的结构，以及每一个 deep_dive 的 topic 和 content 喂给它。
    prompt = [SystemMessage(content="你是一个资深的技术报告主编。你的任务是将记者们发回来的零散报道，整合成一篇逻辑连贯、排版精美、结构严谨的长篇技术报告。"),
        HumanMessage(content=f"""
请严格按照以下原本设定好的大纲结构进行撰写：
【报告大纲】：
{theme_text}

以下是前方记者针对各个子主题收集到的深度研究笔记：
【研究素材】：
{deep_dives_text}

【整合要求】：
1. 结构清晰：利用 Markdown 格式（标题、加粗、列表等）进行排版。
2. 内容连贯：不要让人觉得是生硬拼凑的，章节之间要有自然的过渡和总结。
3. 如果收集的素材里有代码或参考链接，尽力保留它们。
请现在开始生成你的最终版深度整合报告。
""")]
    
    # 3. ainvoke 调用 LLM 获取结果
    final_draft = await llm.ainvoke(prompt)
    # 4. 返回包含草稿的字典：return {"draft": final_draft}
    return {"draft": final_draft.content}