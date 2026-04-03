from typing import Any, TypedDict, Annotated
import operator


class IntelligenceState(TypedDict):
    #存放今天抓取到的所有初始新闻短文本。
    raw_feeds: list[str]
    #lanner 从 raw_feeds 提炼出的核心主题。
    themes: list[str]
    #各个 Executor 矿工挖回来的深度笔记。
    deep_dives: Annotated[list[dict], operator.add]
    #主编最后生成的报告草稿
    draft: str
    #审查官打回时的批评意见
    feedback: str
    #审查官决定是否通过
    is_pass: bool
    #记录整个系统重试/打回的次数
    revision_count: Annotated[int, operator.add]

class ExecutorPayload(TypedDict):
    """专门用来包裹派发给单个 Executor 任务的数据结构"""
    topic: str