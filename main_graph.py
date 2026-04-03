from dotenv import load_dotenv
load_dotenv()

import asyncio
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from app.core.state import IntelligenceState
from app.agents.planner import planner_node
from app.agents.executor import executor_node
from app.agents.synthesizer import synthesizer_node
from app.agents.reviewer import reviewer_node
from app.mcp.feed_fetchers import fetch_github_trending, fetch_hackernews, fetch_reddit_ai, fetch_techmeme

# =====================================
# 🌟 你的任务 1：请在这里补全我上面提到的路由发包函数 distribute_topics
# 提示：照抄我上面的那个发包函数，或者你凭借理解直接默写
# ...你的发包函数填写区域...
def distribute(state: IntelligenceState):
    """
    边缘路由函数：负责把大数组劈开，装进一个个 Send 导弹里发射！
    """
    themes = state.get("themes", [])

    send_missiles = []

    for theme in themes:
        payload = {"topic": theme}

        missile = Send("executor", payload)
        send_missiles.append(missile)
    return send_missiles
# =====================================

def should_continue(state: IntelligenceState):
    if state.get("is_pass"):
        return END
    else:
        print("【全线打回】报告太水，清空草稿，通知 Executor 重新使用更刁钻的搜索关键词深挖原出处！")
        return "executor"

def compile_graph():
    workflow = StateGraph(IntelligenceState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("reviewer", reviewer_node)

    workflow.add_edge(START, "planner")

    # 🌟 你的任务 2：设置发射分发线！
    # Planner 干完活后，不要直接写死传给 Executor！
    # 请让这根线经过你刚才写的 "发包小喇叭" (distribute_topics) 函数处理，由它变成雨点洒给 Executor 阵列。
    # 提示：语法是 workflow.add_conditional_edges( "上游节点名", 发包函数名 )
    # 请写这行连线：
    workflow.add_conditional_edges("planner", distribute)

    # Executor 各自干完活后去哪？（由于目前还没写总编节点，我们先让图直接结束下班）
    workflow.add_edge("executor", "synthesizer")
    workflow.add_edge("synthesizer", "reviewer")

    workflow.add_conditional_edges("reviewer", should_continue)

    app = workflow.compile()
    return app

async def test_run():
    print("====== 欢迎来到《深源情报局》 (Deep Researcher) V2 动态分发联调终端 ======")
    print("====== 正在从全球科技前线获取 24h 实时情报... ======")

    # 1. 抓取真实数据
    gh_feeds = fetch_github_trending()
    hn_feeds = fetch_hackernews()
    mk_feeds = fetch_techmeme()
    re_feeds = fetch_reddit_ai()

    real_today_feeds = gh_feeds[:5] + hn_feeds[:5] + mk_feeds[:5] + re_feeds[:5]

    print(f"====== 成功抓取 {len(real_today_feeds)} 条原始情报，移交 Planner 提炼核心主题 ======")

    initial_state: IntelligenceState = {
        "raw_feeds": real_today_feeds,
        # 你不需要也没法初始化深挖大锅 deep_dives，这里为空留给矿工们慢慢倒金子
        "themes": [],
        "deep_dives": [],
        "draft": "",
        "feedback": "",
        "revision_count": 0,
        "is_pass": False
    }

    graph_app = compile_graph()

    result_state = await graph_app.ainvoke(initial_state)

    # print("\\n\\n=========================《 战 利 品 洗 锅 大 捡 查 》=========================\\n")
    # # 🌟 我们来检查矿工的大锅 deep_dives 里到底倒进去了什么东西
    # import json
    # print(json.dumps(result_state.get("deep_dives"), indent=2, ensure_ascii=False))

    print("\n\n====== 最终技术报告 ======\n")
    print(result_state.get("draft"))

if __name__ == "__main__":
    asyncio.run(test_run())
