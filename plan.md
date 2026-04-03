## Plan: 基于 LangGraph 的前沿技术情报深度分析系统 (AI Daily Researcher)
将现有的线性“拉取+总结”日报脚手架，升级为一个具备**自主深度挖掘、并发调研与交叉验证**能力的多智能体情报系统。系统由 Planner 提取核心趋势，Executor 并发调度爬虫与检索工具深挖细节（例如阅读被提到 GitHub 仓库的 README 和高赞 HN 评论），最后由 Reflector 严防幻觉与“水文”，合成高浓度深度情报。


**🎯 当前项目进度 (Current Status)**
- ✅ **Phase 1-4 (基础与中枢)**: 成功跑通 Planner -> Send API 并发 -> Executor 的 Map-Reduce 机制；彻底解决 DeepSeek 结合 JSON Parser 的原生解析冲突。
- ✅ **Phase 5 (联调闭环)**: Executor 引入真实工具链（HackerNews等爬虫），Synthesizer 结合 Reviewer 完成反思打回图闭环。
- 🚀 **下一步走向**: 完成项目文档更新与开源代码库归档。

** 迭代实施路径 (Steps)**

**Phase 1: 基础设施构建 (Graph Foundation & Map-Reduce)**
- [x] 1. 定义带有 `Annotated` 与 `operator.add` 的全局归约状态 `IntelligenceState`。
- [x] 2. 搭建主图引擎，掌握 `Send API` 语法解决多 Agent 并发写入状态时的覆盖塌陷陷阱。

**Phase 2: Planner 大脑与格式约束 (Planner LLM Integration)**
- [x] 3. 成功套用 Pydantic 的 BaseModel 作为输出强校验锁扣。
- [x] 4. 施加物理级硬性约束规则（强制过滤，仅挑选 1-3 个主题），对下游并发流开辟源头限流。

**Phase 3: 工具挂载与深度矿工 (Executor Tool Calling)**
- [x] 5. 组建基于异步并发（Concurrent）的 Executor 节点。
- [x] 6. 为大模型装配外部触手（`.bind_tools`），并加入了防死循环的 Token 保护限流机制（最大搜索2次限制）。

**Phase 4: 图引擎流控与交叉审查 (Review & Graph Orchestration)**
- [x] 7. **Synthesizer (主编)**：结合并发汇总的 `deep_dives` 撰写结构化最终研报。
- [x] 8. **Reviewer (审查官)**：引入条件回路（Conditional Edges），实现严苛 Schema 打分审查；结合 Revision 指标实现防死锁（>=2次强制放行）。

**Phase 5: 最终联调与部署验证 (Final Run)** - [ 待启动]
- [x] 撤掉假新闻，喂入当日真实的 RSS 源，见证无幻觉的终极技术极简日报诞生！

**Relevant files**
- `app/core/state.py` — 核心状态字典定义，处理并发写入 `Deep Dives` 时的数据规约（reducer）。
- `app/mcp/feed_fetchers.py` — 读取热点的神秘妙妙工具。
- `app/mcp/intelligence_tools.py` — Github Repo 分析、HN 评论拉取以及 Web 搜索接口的封装。
- `app/agents/*.py` — 四大独立思考 Agent 的节点执行逻辑。
- `main_graph.py` — 核心图架构的注册与启动点（节点连线与条件边）。

**Verification**
1. **高并发状态测试**：拦截 3 个不同技术热词，触发 Executor 的多路并发拉取体验，验证 State 中 3 份笔记成功合并没有丢失。
2. **工具调用打孔测试**：给系统输入一个热门但只提名字的开源项目（如最新的大模型蒸馏仓库），检查 Executor 能否主动调用 GitHub 工具去读取它的 README。
3. **闭环拒绝测试**：人为向主编节点注入缺少实际细节的草稿，验证 Reflector 能否拦截，并回退到检索节点要求“补充该模型的具体显存占用要求”。

**Decisions**
- **架构升级**: 果断摒弃传统的线性生成模型，全面拥抱 Map-Reduce + 循环反思打回机制。
- **代价换质量**: 接受高内耗的图多轮并行网络推理耗时，换取零幻觉、带实证考据的重度专业报告（或三行诗日报）。


