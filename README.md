# 🎓 和Copilot一起完成的多智能体图网络项目

**项目名称**：AI Daily Researcher V2 (基于 LangGraph 的深源情报局)
**开发人员**：首席架构师（你） & 联合指导 Mentor（GitHub Copilot）
**阶段结业**：2026年4月

---

## 🌟 1. 项目概述 (Project Overview)
本项目是 Agent 架构进阶的核心实战。我们彻底摒弃了传统的“单脚本+单次调用”的线性爬虫流，重构出了一套具备**目标规划、扇出并发（Map-Reduce）、交叉审查、循环重试**能力的 LangGraph 多智能体图网络系统。系统不再是机械的搬运工，而是化身为一个拥有“主编-矿工-审查官”完整建制的虚拟新闻编辑部。

系统工程架构包含四大核心节点（Nodes）：
*   **🧠 Planner (规划师大脑)**：收口海量生肉数据（GitHub/HN/Techmeme），强制降维提炼 1-3 个最具颠覆性的技术主题。
*   **⛏️ Executor (深度矿工阵列)**：基于 `Send` API 实现动态并发路由。每个矿工认领一个主题，并挂载真实的网络爬虫工具（MCP/Tools）去全网深挖技术细节。
*   **✍️ Synthesizer (排版主编)**：将并发归约（Reducer）回来的多路调查笔记，深度融合成严格的技术报告。
*   **⚖️ Reviewer (苛刻审查官)**：充当质量网关。利用强校验 Schema 检查格式与“水文”浓度，若不达标则触发图引擎的**条件边（Conditional Edge）**打回重写，并带有防死循环熔断机制。

---
***目前的打回重写是直接返回到Executor节点进行重新获取信息然后再重写，或许我应该加一个判断逻辑？不管了，以后有时间再加***
### 当前需要改善的问题：
*   当前信息源过于贫瘠，仅靠tavily的搜索能力远远无法支撑起一个完整的情报网络。
*   对于爬取的信息，过于依赖llm的提炼总结，应当学习Perplexity那样直接一个一个点全面地列出来，想深入了解哪一点就点进去进行了解。
*   reviewer的打回重写应该有条件地连接**Executor**和**Synthesizer**，而非一股脑地重新读取。

## 🚀 2. 核心技术里程碑 (Key Milestones)

### ✅ Phase 1: 复杂图状态与归约器 (State & Reducer)
*   告别普通字典，采用 `typing.Annotated` 和 `operator.add` 构建全局 `IntelligenceState`。彻底解决了多 Agent 并发往同一个列表里写数据时的“覆盖塌陷（Overwrite）”灾难。

### ✅ Phase 2: Map-Reduce 动态并发路由 (Dynamic Fan-out)
*   **最大架构亮点**：突破了死板的定频链式调用。利用 LangGraph 的 `Send` API，实现了根据 Planner 输出的主题数量，动态决定发射多少个 Executor 矿工，并在结束时完美收束（Fan-in）。

### ✅ Phase 3: 强制结构化与格式对冲修复 (Structured Output)
*   在遇到深度推理模型（如 DeepSeek）与框架原生 `with_structured_output` 冲突报 400 错误时，果断降级切入底层，手写 `JsonOutputParser` 结合 System Prompt 强力注入，成功驯服模型输出稳定 JSON。

### ✅ Phase 4: 本地工具真实挂载 (Real Web Tools)
*   将旧版 `ai_daily.py` 的爬虫逻辑重构分离为 `feed_fetchers.py`，让系统具有了捕获当天真实互联网流量的肉体触手。

---

## 🔧 3. 技术栈汇总 (Tech Stack)
*   **核心图引擎**: LangGraph / LangChain Core
*   **大模型基座**: DeepSeek-Chat (V3)
*   **输出解析**: Pydantic / JsonOutputParser
*   **协议与工具**: HTTPX, Feedparser, Asyncio

---

## � 4. 快速启动教程 (Quick Start)

### 1. 环境准备
确保你已安装 Python 3.10 或更高版本。

```bash
# 克隆项目
git clone https://github.com/oldvater/LangGraph-daily-resarch.git
cd LangGraph-daily-resarch

# 创建并激活虚拟环境 (推荐)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
将根目录下的 `.env.example` 复制一份并重命名为 `.env`，然后填入你的 API 密钥：
```env
VECTOR_DB_URL="localhost"
DEEPSEEK_API_KEY="sk-哈基米南北掠夺" # 必填：你的 DeepSeek API Key
# Github token，没有这个会在爬github时被卡住
GITHUB_TOKEN="ghp_hajiminanbeiluduo"

HTTP_PROXY="dingdongjidingdongji"
# LangSmith 观测配置（选填，但建议）
LANGCHAIN_TRACING_V2=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=lsv2_pt_dagoudagoujiaojiaojiao
LANGCHAIN_PROJECT="AI_Daily_Researcher_V2" #你的仓库名
OPENAI_API_KEY= 如果你是富哥们直接使用openai，不然和之前的deepseekapi一致
# tavily api（没有这个你的agent上不了网）
TAVILY_API_KEY="哈基米牛逼劳动"
```

### 4. 运行系统

```bash
cd LangGraph-daily-resarch
python main_graph.py
```

终端打印实例(要是能做一个md前端最好，可惜我不会做，但是如果你配置了LangSmith的话，你在LangSmith里能看到markdown文件)
```bash
====== 欢迎来到《深源情报局》 (Deep Researcher) V2 动态分发联调终端 ======
====== 正在从全球科技前线获取 24h 实时情报... ======
====== 成功抓取 20 条原始情报，移交 Planner 提炼核心主题 ======
====== [NODE] Planner 开始工作 ======
====== [NODE] Executor 异步启动专列：主题 'Google releases Gemma 4 open models' ======
====== [NODE] Executor 异步启动专列：主题 'Anthropic acquires Coefficient Bio for AI-driven biotech tasks' ======
====== [NODE] Executor 异步启动专列：主题 'Lemonade by AMD: a fast and open source local LLM server using GPU and NPU' ======
[0] HumanMessage: 请尽你所能去搜索和挖掘关于 Anthropic acquires Coefficient Bio f...
[1] AIMessage: 我来搜索关于 Anthropic 收购 Coefficient Bio 的相关信息。...
[2] ToolMessage: [{"title": "Aris Theologis - CEO, Coefficient Bio"...
[3] AIMessage: 搜索结果没有直接显示收购信息。让我尝试更具体的搜索：...
[4] ToolMessage: [{"title": "Anthropic Acquires Biotech Startup Coe...
[5] AIMessage: 很好！我找到了关键信息。让我再搜索一下 Coefficient Bio 的具体背景信息：...
[6] ToolMessage: [{"title": "AI-Focused Biotech Unicorns Face Chill...
[7] AIMessage: 基于我收集到的信息，现在我可以提供关于 Anthropic 收购 Coefficient Bio 的...
====== [NODE] Executor 完成主题 'Anthropic acquires Coefficient Bio for AI-driven biotech tasks' ======
[0] HumanMessage: 请尽你所能去搜索和挖掘关于 Google releases Gemma 4 open models ...
[1] AIMessage: 我来搜索关于 Google 发布 Gemma 4 开源模型的最新信息。...
[2] ToolMessage: [{"title": "Gemma 4 model card | Google AI for Dev...
[3] AIMessage: 让我再搜索更多技术细节和相关信息：...
[4] ToolMessage: [{"title": "Welcome Gemma 4: Frontier multimodal i...
[5] AIMessage: 让我再查看一下Hacker News上的相关讨论：...
[6] ToolMessage: 【来自帖子】：Google releases Gemma 4 open models
【网友评论】：...
[7] AIMessage: 基于我收集到的信息，以下是关于 Google 发布 Gemma 4 开源模型的关键技术情报：

##...
====== [NODE] Executor 完成主题 'Google releases Gemma 4 open models' ======
[0] HumanMessage: 请尽你所能去搜索和挖掘关于 Lemonade by AMD: a fast and open sou...
[1] AIMessage: 我来搜索关于"Lemonade by AMD"这个技术的信息。让我先进行第一次搜索。...
[2] ToolMessage: [{"title": "Local LLM Server Concepts - Lemonade",...
[3] AIMessage: 很好！我找到了关于Lemonade Server的信息。让我再搜索一下相关的GitHub仓库或者更详...
[4] ToolMessage: [{"title": "Developer Getting Started - Lemonade S...
[5] AIMessage: 现在让我搜索一下Hacker News上关于这个技术的讨论，看看社区的反响如何。...
[6] ToolMessage: 【来自帖子】：Ask HN: Who uses open LLMs and coding assis...
[7] AIMessage: 基于我收集到的信息，现在我可以提供关于"Lemonade by AMD"的详细技术情报了。以下是我收...
====== [NODE] Executor 完成主题 'Lemonade by AMD: a fast and open source local LLM server using GPU and NPU' ======
====== [NODE] Synthesizer 主编开始整合所有深度报告... ======
====== [NODE] Reviewer 开始交叉审阅... ======
[Reviewer] 审阅结果：✅ 通过。反馈：报告结构清晰，深度整合了三个前沿事件，技术细节扎实（如Gemma 4的混合注意力、双RoPE、PLE等），战略分析透彻，体现了
对AI生态演进的深刻洞察。合格。

```
====== 最终技术报告 ======

# 技术前沿深度整合报告：开源模型、AI制药与本地化部署的新浪潮

## 引言

当前人工智能领域正沿着三条关键路径高速演进：**模型能力的开源化与普惠化**、**AI技术与垂直产业的深度融合**，以及**计算硬件的本地化与高效利用**。本报告 将整合近期三个标志性事件——Google发布Gemma 4开源模型家族、Anthropic收购生物科技公司Coefficient Bio，以及AMD推出开源本地LLM服务器Lemonade。这三者看似独立，实则共同勾勒出AI技术栈从云端到边缘、从通用到专用、从封闭到开放的清晰发展脉络。通过深度剖析其技术细节与战略意图，我们得以洞察下一代AI生态系统的构 建方向。

---

## 第一章：Google Gemma 4 —— 开源多模态模型的性能与成本新标杆

Google DeepMind近期发布的Gemma 4开源模型家族，标志着其在开源大模型领域的战略投入进入新阶段。该系列不仅追求性能的顶尖水平，更在架构创新、成本控制和部 署灵活性上设立了新的行业基准。

### 1.1 核心特性与模型家族

Gemma 4是一个**原生多模态**模型家族，支持文本和图像输入（部分小模型额外支持音频），并生成文本输出。其最引人注目的特性之一是**超长上下文窗口**，最高支持256K tokens，为处理长文档、复杂代码库或长篇对话提供了强大支持。此外，模型原生支持超过**140种语言**，具备真正的全球化潜力。

模型家族提供了多样化的规格选择，以满足不同场景的需求：

| 模型 | 参数规模 | 上下文窗口 | 检查点类型 | 设计目标 |
| :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E2B** | 2.3B有效参数，5.1B含嵌入 | 128K | 预训练(base)、指令调优(IT) | 极致轻量，边缘设备部署 |
| **Gemma 4 E4B** | 4.5B有效参数，8B含嵌入 | 128K | 预训练(base)、指令调优(IT) | 平衡性能与效率 |
| **Gemma 4 31B** | 31B密集模型 | 256K | 预训练(base)、指令调优(IT) | 高性能通用任务 |
| **Gemma 4 26B A4B** | MoE架构，4B激活/26B总参数 | 256K | 预训练(base)、指令调优(IT) | 高智商、高效率推理 |

这种从2B到31B的参数覆盖，结合密集与MoE（混合专家）架构，使开发者能够根据自身算力预算和应用复杂度精准选择模型。

### 1.2 突破性的技术架构创新

Gemma 4的性能提升源于一系列底层技术创新：

*   **混合注意力机制**：模型交替使用**局部滑动窗口注意力**和**全局全上下文注意力**。小模型使用512 tokens的滑动窗口，大模型使用1024 tokens。这种设计在保证长序列处理能力的同时，显著降低了计算复杂度。
*   **双RoPE配置**：为支持超长上下文，模型采用了两种旋转位置编码（RoPE）。标准RoPE用于滑动窗口层，而**比例RoPE**用于全局注意力层，有效缓解了外推时的 性能衰减问题。
*   **每层嵌入（PLE）**：引入第二个嵌入表，向每个解码器层提供小的残差信号。这增强了模型的信息流动和表征能力。
*   **共享KV缓存**：最后N层直接重用早期层的键值（KV）状态，**消除了冗余的KV投影计算**，大幅提升了推理速度并降低了内存占用。
*   **高效视觉编码器**：采用学习了2D位置和多维RoPE的编码器，能保持图像的原始宽高比信息。它支持从70到1120 tokens的多级视觉token预算，允许在视觉保真度 和计算成本之间进行灵活权衡。
*   **音频编码器**：沿用Gemma 3的USM风格Conformer架构，确保了强大的音频理解能力。

### 1.3 性能表现与市场定位

在性能基准测试中，Gemma 4表现卓越。31B密集模型在LMArena（仅文本）测试中达到约1452分。更令人印象深刻的是26B MoE模型，仅激活4B参数就取得了1441分的成绩 ，展现了极高的计算效率。在多模态任务的非正式测试中，其表现与纯文本生成性能相当。

Gemma 4的**核心市场优势在于其极致的性价比和部署友好性**：
*   **成本优势**：据报道，其使用成本相比Google自家的Gemini 3 Pro便宜**10倍**，而性能却非常接近。
*   **边缘计算友好**：轻量级模型（如E2B, E4B）经过优化，非常适合在移动设备和边缘侧部署。
*   **开发者友好**：采用**Apache 2.0开源许可证**，并已深度集成至Hugging Face平台和GitHub，提供了完整的文档和代码，极大降低了开发者的使用和定制门槛。 

### 1.4 战略意义与生态影响

Google发布Gemma 4绝非简单的技术迭代，其背后有深远的战略考量：
1.  **开源生态竞争**：直接与Meta的Llama等闭源或半闭源生态系统竞争，争夺开发者心智和生态主导权。
2.  **推动可组合AI堆栈**：通过提供高性能开源模型，与新兴的开放代理协议（如OpenAI的GPTs或自定义助手）结合，推动一个模块化、可互操作的AI未来。
3.  **技术民主化**：使初创公司和小型团队能够以极低的成本构建和生产级AI应用，降低了创新门槛。
4.  **避免供应商锁定**：企业可以基于Gemma 4针对自身特定用例进行微调，而不必完全依赖某一家云厂商的API服务。

**相关资源**：
*   官方模型卡：https://ai.google.dev/gemma/docs/core/model_card_4
*   Hugging Face技术博客：https://huggingface.co/blog/gemma4
*   性能对比：https://aibenchy.com/compare/google-gemma-4-31b-it-medium/google-gemini-3-pro-preview-medium/

---

## 第二章：Anthropic收购Coefficient Bio —— AI驱动生物制药的“自主发现”野心

当开源模型降低AI应用门槛时，领先的AI公司正将目光投向更具深度和价值的垂直产业。Anthropic以约**4亿美元**收购生物科技初创公司Coefficient Bio，正是其向AI驱动生命科学领域纵深迈进的关键一步。

### 2.1 收购的战略背景：逆转“Eroom定律”

传统药物发现流程以其高昂的成本、漫长的周期和高失败率而闻名，这被戏称为“Eroom定律”（Moore定律的反向词）。开发一款新药平均耗时超过10年，耗费超过20亿美 元，且临床试验失败率高达90%。Anthropic的目标正是利用AI**打破这一僵局**。

此前，Anthropic已通过“Claude for Life Sciences”提供与Benchling、BioRender、PubMed等科研平台的连接器，扮演“AI研究伙伴”的角色。然而，要真正实现“**AI作 为自主发现者**”，必须获得在硅内（in silico）进行生物建模、分子设计和虚拟筛选的原生能力。收购Coefficient Bio正是为了补全这一关键拼图。

### 2.2 对标行业与能力构建

此次收购的战略意图，可以通过对标业内成熟的AI制药公司来理解：
*   **Insilico Medicine**：其Pharma.AI套件提供了从靶点发现（PandaOmics）、分子生成（Chemistry42）到临床试验预测（InClinico）的端到端能力，已将临床前 候选药物开发时间缩短至11-18个月。
*   **Exscientia**：平台专注于小分子药物优化，据报道曾在不到一年内设计出可进入I期临床试验的强迫症候选药物。

Coefficient Bio的具体技术细节虽未完全公开，但可以推断，其核心价值在于为Anthropic带来了**专有的生物数据、分子模拟算法或实验验证管道**。这将使Claude模 型能够更深入、更可靠地理解生物实体的复杂相互作用，从而进行创造性的药物设计。

### 2.3 AI重塑生物技术的未来

这次收购是AI深度赋能硬科技的一个缩影。AI正在通过两种方式改变生物技术研发：
1.  **降本增效**：大幅降低发现成本，缩短开发时间，提高成功率。
2.  **能力突破**：AI原生平台能够探索人类专家难以想象的化学空间，生成具有全新作用机制的候选药物，其效果甚至可能优于现有市售疗法。

自主AI研究实验室与湿实验室（传统实验）的结合，正在加速从假设到验证的整个科学发现过程。这被认为是自人类基因组计划以来，制药开发领域最重大的创新范式转 移。

**相关资源**：
*   交易报道：The Information (2025年4月3日)
*   战略分析：https://www.healthcare.digital/single-post/acquisition-framework-for-anthropic-and-the-claude-ecosystem-strategic-consolidation-healthcare-ai

---

## 第三章：AMD Lemonade —— 本地化、开源LLM服务器的硬件协同实践

高性能模型和垂直应用最终需要落在具体的计算硬件上执行。AMD推出的开源项目 **Lemonade Server**，正是为了解决在本地环境（尤其是AMD硬件平台）上高效、便捷 部署和运行LLM的痛点。

### 3.1 项目定位与核心功能

Lemonade是一个**快速、开源的本地LLM服务器**，其核心目标是简化开发者在本地机器上利用GPU和NPU运行大模型的过程。它并非要替代llama.cpp或vLLM等底层推理引 擎，而是构建在它们之上的一层**抽象和集成**。

其主要功能特性包括：
*   **多模型支持**：可同时加载和管理多个LLM模型，并在它们之间快速切换。
*   **多模态推理**：除文本生成（基于llama.cpp）外，还集成了图像生成、语音识别（whisper.cpp）和文本转语音（TTS）能力，形成一个本地化的多模态AI服务枢纽。
*   **标准化API**：提供**完全兼容OpenAI API标准**的接口（如`/v1/chat/completions`）。这意味着任何为ChatGPT API编写的应用程序，只需更改API基础地址，即可无缝对接本地部署的模型。
*   **硬件加速优化**：深度支持AMD硬件栈，包括通过ROCm进行**GPU加速**，以及专门支持AMD Ryzen AI系列和Strix Halo平台中的**NPU（神经网络处理单元）**，实现能效最优的推理。

### 3.2 技术架构与部署优势

Lemonade采用经典的客户端-服务器架构，通过HTTP协议通信。其技术优势体现在：
1.  **简化集成**：为开发者隐藏了底层推理框架（llama.cpp）和设备（GPU/NPU驱动）的复杂细节，开发者只需关注业务逻辑。
2.  **资源共享**：以服务器形式运行，允许多个前端应用（如Open WebUI、continue.dev等）共享同一个已加载的模型，减少总体内存占用。
3.  **开箱即用**：提供.deb、.rpm包和macOS支持，安装过程简单。依赖项明确（如`libcurl4`, `ffmpeg`），降低了部署难度。
4.  **性能透明**：提供`/stats`端点返回性能指标，方便监控和调优。

### 3.3 应用场景与社区生态

Lemonade精准服务于以下几类用户：
*   **LLM爱好者与研究者**：希望在个人电脑上轻松体验和对比不同大模型，尤其是利用AMD NPU获得静音、低功耗的推理体验。
*   **应用开发者**：希望将LLM能力以标准化方式集成到自己的桌面或局域网应用中，避免依赖不稳定的云端API，并保障数据隐私。
*   **AI智能体（Agent）开发者**：可以基于本地部署的、API兼容的模型，快速开发“本地优先”的AI代理应用。

社区已有成功案例，例如用户在配备128GB内存的AMD Strix Halo开发板上部署Lemonade，成功运行Qwen3 Coder 30B等模型用于编程辅助，并通过WireGuard实现远程安全访问。

**相关资源**：
*   官方网站与文档：https://lemonade-server.ai/
*   API概念详解：https://lemonade-server.ai/server/concepts.html

---

## 总结与趋势展望

通过对Gemma 4、Anthropic收购案和Lemonade Server的整合分析，我们可以清晰地看到三条相互交织的AI发展主线：
、更深入（垂直AI）、更自主（本地计算）的AI生态系统正在加速形成。** 开发者、企业和研究者将拥有前所未有的工具选择权和数据控制权，这必将激发新一轮的创新浪潮。然而，挑战也随之而来：如何管理日益复杂的异构算力？如何确保垂直领域AI的安全性与可靠性？如何在开源生态中建立可持续的商业模型？这些问题将是下一阶段产业探索的重点。
```