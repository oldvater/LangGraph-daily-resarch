from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from typing import Any
from app.core.config import settings
from pydantic import SecretStr

from app.core.state import ExecutorPayload
from app.mcp.intelligence_tools import get_intelligence_tools

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=SecretStr(settings.DEEPSEEK_API_KEY),
    base_url="https://api.deepseek.com",
    temperature=0.3
)

# 注意！入参变了！它不再接受大字典，而是接收针对它的那一份"专题小字典"
async def executor_node(payload: ExecutorPayload) -> dict[str, Any]:
    current_topic = payload["topic"]
    print(f"====== [NODE] Executor 异步启动专列：主题 '{current_topic}' ======")

    tools = get_intelligence_tools()

    system_message = SystemMessage(
        content=f"""你是一个顶级的 AI 技术情报研究员。
你的任务是深入调查以下技术主题：【{current_topic}】。
你必须、必须、必须优先使用提供的工具去获取第一手资料！
【重要限制】：搜索不可超过 2 次！如果 2 次以内搜不到特别多内容，必须立即停止搜索，利用已有资料进行总结，决不能无限循环搜索！
最后，请把收集到的所有关键信息、数据、代码片段和原始链接，用高密度的要点（Bullet points）形式直接罗列出来。无需排版成优美的文章，只需保留最硬核的干货！。"""
    )

    # 限制研究员做无用功、滥用工具的次数，防止一次跑太久并消耗太多Token
    research_agent = create_agent(
        model=llm, 
        tools=tools,
        system_prompt=system_message
        )
    
    human_req = HumanMessage(content=f"请尽你所能去搜索和挖掘关于 {current_topic} 的资料吧！必须使用工具。最多查询2次。")

    try:
        # ainvoke 是异步执行！特种兵进入循环状态。
        result = await research_agent.ainvoke({"messages": [human_req]})
        final_report = result["messages"][-1].content

        import json
        for i, msg in enumerate(result["messages"]):
            print(f"[{i}] {type(msg).__name__}: {msg.content[:50]}...")
    except Exception as e:
        print(f"[Error in {current_topic}]: {e}")
        final_report = f"挖掘该主题时遇到了异常：{str(e)}"

    print(f"====== [NODE] Executor 完成主题 '{current_topic}' ======")    
    # 最后，按照原定协议，把金砖包在单列表的字典里丢给全局状态的 reducer
    return {"deep_dives": [{"topic": current_topic, "content": final_report}]}