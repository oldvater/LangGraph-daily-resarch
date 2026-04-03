from langchain_core.tools import tool
import asyncio
import httpx
import base64
from app.core.config import settings
from asyncddgs import aDDGS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch


@tool
async def get_github_repo_readme(repo_name: str) -> str:
    """
    给出一个Github仓库名称(例如“langchain-ai/langchain”)，爬取其最新README或简介。
    """
    # ... 在这里编写你的具体获取逻辑 ...
    github_api_url = f"https://api.github.com/repos/{repo_name}/readme"
    headers = {"Accept": "application/vnd.github.v3+json"} # 标准规范

    github_token = settings.GITHUB_TOKEN
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    try:
        # TODO 1: 使用异步上下文管理器发起请求 (例如 async with httpx.AsyncClient() as client: )
        async with httpx.AsyncClient() as client:
            r = await client.get(github_api_url, headers=headers, timeout=15)
        # TODO 2: 获得响应后(response)，解析它的 JSON 格式，并提取 'content' 字段
        if r.status_code == 200:
            data = r.json()
            desc = data.get("content", "")
                
        # TODO 3: 引入 base64 库把拿到的 content 解码成可读的纯文本字符串，然后 return 出去。
            if desc:
                decoded_binary = base64.b64decode(desc)
                decoded_text = decoded_binary.decode('utf-8')
                return decoded_text
            else:
                return "未找到 README 内容"
        else:
            return f"获取失败，API 返回状态码: {r.status_code}"
    except Exception as e:
        return f"获取仓库 {repo_name} README 时发生错误: {str(e)}"

@tool
async def get_hn_discussion(key_word: str) -> str:
    """
    给出一个关键词，在Hacker News上爬取其相关的高赞评论。
    """
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": key_word,
        "tags": "comment",
        "hitsPerPage": 3
    }

    try:
        # TODO 1: 用 async with httpx.AsyncClient() as client 发起 GET 请求
        # 注意把 params=params 传进去，记得加上 timeout=10
        async with httpx.AsyncClient() as client:
            r = await client.get(url, params=params, timeout=10)
        # TODO 2: 判断 HTTP 状态码 200，并解析 r.json() 拿到 "hits" 列表
        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", [])
        # TODO 3: 循环遍历 hit，把 title, points, url 拼成一个漂亮的字符串返回
            if not hits:
                return "没读到帖子。"
            result_strs = []
            for hit in hits:
                comment_text = hit.get("comment_text", "")
                story_title = hit.get("story_title", "")
                Url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
                result_strs.append(f"【来自帖子】：{story_title}\n【网友评论】：{comment_text}\n【链接】：{Url}。")
            return "\n---\n".join(result_strs)
        else:
            return f"获取失败，API 返回状态码: {r.status_code}"
    except Exception as e:
        return f"获取 HackerNews 数据时出现异常：{str(e)}"


#"""草，ddgs反爬把我踢出去了，气哭了"""
# @tool
# async def get_web_search(query: str) -> str:
#     """
#     给出一个问题或者关键词，通过互联网搜索获取最新的新闻或文章摘要。
#     如果你需要查阅时事、新闻，请一定优先使用这个工具。
    
#     【重要警告】：搜索引擎不支持长句子！
#     请提取 1 到 3 个核心关键词作为 query 进行搜索。
#     例如：不要搜 "LangChain version 1.0 release 2024"，必须搜 "LangChain 1.0 release" 或 "LangChain 更新"。
#     """
#     try:
#         results = []
#         async with aDDGS() as ddgs:
#             text_results = await ddgs.text(
#                 keywords=query,
#                 max_results=3
#             )
#             for text_result in text_results:
#                 results.append(f"【标题】：{text_result['title']},【连接】：{text_result['href']},【摘要】：{text_result['body']}")
#             if not results:
#                 return f"未能搜索到与 '{query}' 相关的互联网结果。"
#             result = "\n----------\n".join(results)

#             return result
#     except Exception as e:
#         return f"执行网络搜索时遭遇错误：{str(e)}"

tavily_tool = TavilySearchResults(
    max_results=2, # 把每次查询的结果缩减到 2 条，减少 context size
    description="""给出一个问题或者关键词，通过Tavily搜索引擎获取最新的新闻或文章摘要。查找最新资讯首选工具。
    【重要警告】：搜索引擎不支持长句子！
    请提取 1 到 2 个核心关键词作为 query 进行搜索。
    """
)
    

def get_intelligence_tools() -> list:
    return [get_github_repo_readme,
            get_hn_discussion,
            tavily_tool]

if __name__ == "__main__":
    async def test():
        print(await get_hn_discussion.ainvoke({"key_word": "langchain"}))
    asyncio.run(test())