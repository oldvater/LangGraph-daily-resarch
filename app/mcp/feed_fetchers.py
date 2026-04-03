# LangGraph/app/mcp/feed_fetchers.py

import sys, os, requests, time, feedparser
from datetime import datetime, timedelta, timezone
from app.core.config import settings


GITHUB_TOKEN = settings.GITHUB_TOKEN                   # GitHub Token（可选，提升限额）
PUSH_TIME = "08:00"                                             # 每天推送时间


# ====== 维度一：Builders在干嘛 (GitHub Search API) ======

def fetch_github_trending():
    """广撒网：过去24h所有语言中星星涨最快的仓库（不做关键词过滤，交给LLM筛）"""
    items = []
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        r = requests.get("https://api.github.com/search/repositories", params={
            "q": f"pushed:>{yesterday} stars:>100", "sort": "stars", "order": "desc", "per_page": 25
        }, headers=headers, timeout=15)
        if r.status_code == 200:
            for repo in r.json().get("items", []):
                desc = repo.get("description") or ""
                topics = ", ".join(repo.get("topics", []))
                url = repo.get("html_url", "")
                items.append(f"⭐{repo['stargazers_count']} [{repo['full_name']}]({url}) "
                             f"[{topics}] — {desc}")
        else:
            print(f"[GitHub] API {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"[GitHub] 抓取失败: {e}")
    return items[:20]


# ====== 维度二：Thinkers在吵啥 (Hacker News + Reddit) ======

def fetch_hackernews():
    """HN 过去 24h 热帖 TOP30（不限关键词，全量抓取交给LLM筛）"""
    items = []
    try:
        url = "https://hn.algolia.com/api/v1/search"
        since = int(time.time()) - 86400
        r = requests.get(url, params={
            "tags": "story",
            "numericFilters": f"created_at_i>{since},points>50",
            "hitsPerPage": 30,
        }, timeout=10)
        for hit in r.json().get("hits", []):
            link = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
            items.append({
                "title": hit["title"],
                "points": hit.get("points", 0),
                "url": link,
            })
    except Exception as e:
        print(f"[HN] 抓取失败: {e}")
    items.sort(key=lambda x: x["points"], reverse=True)
    return [f"🔥{a['points']}分 | [{a['title']}]({a['url']})" for a in items[:20]]


def fetch_reddit_ai():
    """Reddit 科技/AI 相关 sub 热帖（广撒网，包含 technology 大 sub）"""
    items = []
    subs = ["artificial", "MachineLearning", "LocalLLaMA", "technology", "singularity"]
    for sub in subs:
        try:
            r = requests.get(
                f"https://www.reddit.com/r/{sub}/hot.json?limit=15",
                headers={"User-Agent": "AI-Daily-Bot/2.0"}, timeout=10)
            for post in r.json()["data"]["children"]:
                d = post["data"]
                if d.get("score", 0) > 50:
                    items.append({
                        "title": d["title"],
                        "score": d["score"],
                        "sub": sub,
                        "url": f"https://reddit.com{d.get('permalink', '')}",
                    })
        except Exception as e:
            print(f"[Reddit/{sub}] 抓取失败: {e}")
    items.sort(key=lambda x: x["score"], reverse=True)
    return [f"💬{i['score']}↑ r/{i['sub']} | [{i['title']}]({i['url']})" for i in items[:15]]


# ====== 维度三：Markets在吹啥 (Techmeme RSS) ======

def fetch_techmeme():
    """Techmeme RSS 全量头条（不做关键词过滤，交给LLM筛）"""
    items = []
    try:
        feed = feedparser.parse("https://www.techmeme.com/feed.xml")
        for entry in feed.entries[:30]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            items.append(f"📰 [{title}]({link})")
    except Exception as e:
        print(f"[Techmeme] 抓取失败: {e}")
    return items[:20]