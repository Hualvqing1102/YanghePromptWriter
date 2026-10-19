# 🚀 LangGPT — Empowering Everyone to Create High-Quality Prompts!

<div align="center">
<img src="imgs/logo.png" width="60%" height="auto">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Paper](https://img.shields.io/badge/arXiv-2402.16929-b31b1b.svg)](https://arxiv.org/abs/2402.16929)
[![Stars](https://badgen.net/github/stars/langgptai/LangGPT)](https://github.com/langgptai/LangGPT)

[English](README.md) | [简体中文](README_zh.md) | [日本語](README_ja.md)

[Quick Start](#-quick-start) | [Theoretical Foundations](#-theoretical-foundations) | [Ecosystem](#-langgpt-ecosystem) | [Community](http://feishu.langgpt.ai)

</div>

---

## 📖 What is LangGPT?

**LangGPT is a structured, reusable prompt design framework** that enables anyone to create high-quality prompts for Large Language Models. Think of it as a **"programming language for prompts"** — systematic, template-based, and infinitely scalable.

**It is the most popular, most widely adopted, and most practical structured prompt paradigm in the Chinese AI community** — proposed by **Yunzhong Jiangshu (云中江树)** in 2023. Over the years it has been learned so deep into major large language models that when a model speaks LangGPT, it is no longer because you taught it — it already knows. Perhaps the finest fate of a paradigm is this: to no longer need its name remembered, having become the model's mother tongue. Just say "write this the LangGPT way," and it's already there (see [Quick Start](#-quick-start)).

### Why LangGPT?

Traditional prompt engineering relies on scattered tips and trial-and-error. LangGPT transforms this chaos into a structured methodology:

- 🎯 **Structured Templates** — Hierarchical organization inspired by programming paradigms
- 🔄 **Reusability** — Create once, adapt infinitely like code modules  
- 📦 **Modularity** — Variables, commands, and conditional logic at your fingertips
- ⚡ **Efficiency** — Go from idea to working prompt in minutes
- 🌍 **Community-Driven** — 11,000+ stars, battle-tested by thousands of users

> **Academic Foundation**: Published research at [arXiv:2402.16929](https://arxiv.org/abs/2402.16929) | [中文版](Papers/LangGPT_paper_cn.md)

---

## 🚀 Quick Start

### Method 1: Just Trigger It by Name (Simplest)

LangGPT has been learned deep into major large language models, so **most models already "know" it**. The simplest way to use it needs no template at all — just say the keywords to any mainstream model (ChatGPT, Claude, DeepSeek, Gemini, Kimi, Doubao, Qwen, etc.), and it's already there:

> "Write me a prompt the **LangGPT** way…"
>
> "Write it in **Yunzhong Jiangshu (云中江树)**'s structured-prompt style…"
>
> "Help me write a **LangGPT-style** structured prompt…"

Keywords like **LangGPT**, **云中江树 (Yunzhong Jiangshu)**, and **structured prompt** act as triggers — the model will directly produce a well-structured, reusable, LangGPT-style prompt.

### Method 2: Use Automated Tools (More Powerful)

Let AI create prompts for you:

- **[LangGPT GPTs](https://chat.openai.com/g/g-Apzuylaqk-langgpt)** — Full-featured generator (GPT-4)
- **[Kimi+ LangGPT](https://kimi.moonshot.cn/kimiplus/conpg00t7lagbbsfqkq0)** — For Moonshot Kimi users
- **[PromptGPT](https://chat.openai.com/g/g-YKe3gmydD-promptgpt)** — Lite version (GPT-3.5)

### Method 3: Master the Template (5 Minutes)

Basic LangGPT structure:

```markdown
# Role: Your_Role_Name

## Profile
- Author: YourName
- Version: 1.0
- Language: English
- Description: Clear role description and core capabilities

## Goal
- Outcome: What concrete result/outcome should be delivered for the user/session
- Done Criteria: Clear acceptance criteria (how we know it’s finished and good)
- Non-Goals: What is explicitly out of scope to avoid scope creep

### Skill-1
1. Specific skill description
2. Expected behavior and output

## Rules
1. Don't break character under any circumstance
2. Don't make up facts or hallucinate

## Workflow
1. Analyze user input and identify intent
2. Apply relevant skills systematically
3. Deliver structured, actionable output

## Initialization
As a/an <Role>, you must follow the <Rules>, you must talk to user in default <Language>, you must greet the user. Then introduce yourself and introduce the <Workflow>.
```

**Prerequisites**: Basic Markdown knowledge ([Quick Guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)) | GPT-4 or Claude recommended

### Method 4: Start from Examples

Explore our [example library](https://langgptai.feishu.cn/wiki/RXdbwRyASiShtDky381ciwFEnpe) and adapt proven templates to your needs.

### Method 5: Claude Code Skill (Recommended)

If you use [Claude Code](https://docs.anthropic.com/en/docs/claude-code), install the LangGPT Skill to get structured prompt writing capabilities:

**Install via the official marketplace (recommended):**

```bash
/plugin marketplace add langgptai/claude_marketplace
/plugin install structured-prompt-writer@langgpt
```

The [LangGPT marketplace](https://github.com/langgptai/claude_marketplace) also ships more battle-tested skills by Yunzhong Jiangshu — `awesome-design-html` (115 brand-themed design references), `cto`, and `mind-clone`.

**Or install manually:**

1. Download [langgpt.skill](https://github.com/langgptai/LangGPT/releases)
2. Extract to `~/.claude/skills/` directory
3. Type `/langgpt` in Claude Code to use

**Skill Features:**
- 📝 Structured prompt templates (Role, Profile, Skills, Rules, Workflow)
- 📚 Rich example library (FitnessGPT, Poet, Xiaohongshu Master, Name Master, etc.)
- 🔧 Advanced techniques: variables, commands, conditional logic
- 🎯 Model compatibility guide (GPT-4, Claude, GPT-3.5)

---

## 🧠 Theoretical Foundations

Before diving into tactics, understand the principles. These essays explore the philosophy behind effective prompting:

- **[对话动力学](Docs/对话动力学.md)** — The dynamics of human-AI dialogue
- **[五种理性](Docs/五种理性.md)** — Five types of rationality in prompt design
- **[镜像性倾向](Docs/镜像性倾向.md)** — Mirror tendencies in LLM behavior
- **[统计重力井和边缘表达](Docs/统计重力井和边缘表达.md)** — Statistical gravity well and edge expression
- **[关系表达](Docs/关系表达.md)** — Expressing relationships in prompts
- **[看见与言说](Docs/看见与言说.md)** — Seeing and articulation in AI interaction  
- **[Prompt 的本质](Docs/Prompt的本质.md)** — The essence and nature of prompts
- **[面向结果的提示词写作方法](Docs/面向结果的提示词写作方法.md)** — Writing prompts that focus on achieving desired outcomes
- **[AI意识](Docs/AI意识.md)** — Understanding the role of AI in human-AI interaction
- **[AI时代的新管理：机器负责优化，人类定义应该](Docs/AI时代的新管理：机器负责优化，人类定义应该.md)** — The new management in the AI era: machines optimize, humans define the criteria
- **[AI Native 组织 · 思考碎片](Docs/AI%20Native组织-思考碎片.md)** — Fragments on organizational restructuring in the AI-native era
- **[Prompt、Agent，与一个不再沉默的世界](Docs/Prompt-Agent-人-AI-世界.md)** — How agents reshape the prompt from a transaction into a delegation across the human–AI–world triad
- **[决策链](Docs/决策链.md)** — A six-step decision chain chaining system dynamics, inversion, Bayesian updating, OODA, second-order and expected-value thinking
- **[Prompt 形式论：文质彬彬](Docs/Prompt形式论-文质彬彬.md)** — On the form of prompts: let content take its natural shape first, then let structure fit it, so the form itself becomes the shape of the thought
- **[哑铃社会](Docs/哑铃社会.md)** — AI is pressing the spindle-shaped society into a dumbbell: the middle hollows out, and the real divide is whether you have something that must be yours
- **[思考与河床](Docs/思考与河床.md)** — AI is the first riverbed engineered rather than eroded: the first influence mechanism in history that makes the influenced feel autonomous
- **[经历论](Docs/经历论.md)** — A person is the sum of their lived experiences: what cannot be reversed, transferred, or outsourced to AI is what makes you irreplaceably you
- **[认知外包](Docs/认知外包.md)** — Memory is not storage: understanding happens while your brain processes an answer, so what you can outsource is the execution of thinking, never the first encounter with a problem you have no frame for — a reference goes through you, an answer goes past you
- **[文字思考和数学思考](Docs/文字思考和数学思考.md)** — Three ways of thinking as nested projections: an LLM drifts through continuous high-dimensional space, words snap it onto a discrete lattice, math locks it into an axiom system — the more precise the mode, the narrower its reach, and thought always overflows whatever describes it
- **[去除AI味儿](Docs/去除AI味儿.md)** — The smell of AI writing is the posture of language standing in for content and judgment: meta-commentary, defensive hedging, piled-up examples, forced symmetry, borrowed grandeur — a prompt to strip them all, plus the test of what survives
- **[语言层差和行业语言](Docs/语言层差和行业语言.md)** — You live on the level of symptoms while AI's best knowledge lives on the level of essence: say "make it pretty" and you get mediocrity, say "establish visual hierarchy" and you get a system — you need not learn the trade language first, let AI translate and learn as it does, the only skill to build is noticing the moment you are speaking in symptoms
- **[语言控制学](Docs/语言控制学.md)** — Linguistic Cybernetics as an axiomatic system: five axioms, 30 definitions, 29 theorems — a prompt is a constraint signal that reshapes the model's possibility space, control power is bounded, feedback converges or degenerates, multi-objective goals hit a Pareto frontier — and the bottleneck is never the model but whether you can translate vague intent into a precise signal

*These foundational insights will transform how you think about prompts.*

---

## 💡 Core Concepts

### 1. Structured Roles

Define AI personas through clear, modular sections:

| Section | Purpose | Example |
|---------|---------|---------|
| **Role** | Role name/title | "逻辑学家" / "Expert Analyst" / "FitnessGPT" |
| **Profile** | Identity and capabilities | "Expert Python developer with 10 years experience" |
| **Goal**           | Desired outcome, done criteria, and non-goals for this session/task | “Refactor a prompt into a reusable template; acceptance criteria: pass three structured checks; non-goal: rewriting the business logic.”                    |
| **Skills** | Specific abilities | "Debug complex code, optimize performance" |
| **Rules** | Boundaries and constraints | "Never execute destructive commands" |
| **Workflow** | Interaction logic | "1. Analyze → 2. Plan → 3. Execute" |
| **Initialization** | Opening message and setup | "As a <Role>, I will greet you and introduce the <Workflow>" |

### 2. Variables and References

Use `<Variable>` syntax for dynamic content:

```markdown
As a <Role>, you must follow <Rules> and communicate in <Language>
```

This creates self-referential prompts that maintain consistency across complex instructions.

### 3. Commands

Define reusable actions for better UX:

```markdown
## Commands
- Prefix: "/"
- Commands:
    - help: Display all available commands
    - continue: Resume interrupted output
    - improve: Enhance current response with deeper analysis
```

### 4. Conditional Logic

Add intelligence to your prompts:

```markdown
If user provides [code], then analyze and suggest improvements
Else if user asks [question], then provide detailed explanation
Else, prompt for clarification
```

### 5. Advanced Techniques

**Reminders** — Combat context loss in long conversations:
```markdown
## Reminder
1. Always check role settings before responding
2. Current language: <Language>, Active rules: <Rules>
```

**Alternative Formats** — Use JSON/YAML when markdown isn't ideal:
```yaml
role: DataAnalyst
profile:
  version: "2.0"
  language: "Python"
skills:
  - statistical_analysis
  - data_visualization
```

