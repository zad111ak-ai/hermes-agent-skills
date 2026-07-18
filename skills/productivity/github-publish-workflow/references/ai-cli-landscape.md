# AI CLI Tools Landscape (July 2026)

## Major Players (10K+ stars)

| Tool | Stars | What it does | Niche |
|------|-------|-------------|-------|
| gemini-cli | 106K | AI agent in terminal | General-purpose AI CLI |
| OpenHands | 80K | AI-driven development | Coding agent |
| caveman | 88K | Token-efficient prompting | "why use many token" |
| ponytail | 80K | Lazy senior dev persona | Code review |
| aider | 47K | AI pair programming | Code assistance |
| promptfoo | 23K | Testing/red-teaming prompts | Prompt eval |
| prompt-optimizer | 32K | Optimize prompts | Prompt engineering |
| headroom | 58K | Compress tool outputs/context | Context optimization |
| rtk | 70K | CLI proxy reducing token consumption | Token optimization |

## Adjacent Space (1-10K stars)

| Tool | Stars | Niche |
|------|-------|-------|
| langfuse | 31K | LLM engineering platform |
| opik | 21K | Debug, evaluate, monitor LLMs |
| mlflow | 27K | ML engineering platform |
| claude-skills | 22K | Claude Code skills/plugins |
| plany | 6.7K | AI-native proxy for routing/throttling |
| claude-tap | 2.5K | Claude Code traffic intercept/audit |

## Open Niches

### AI Workflow Pipeline Tools
- Single-step AI assistants (gemini-cli, aider)
- Evaluation/testing (promptfoo, langfuse)
- Agent frameworks (OpenHands, agents)
- Code assistance (Claude Code, oc)

**aiflow** — first attempt in this niche (YAML pipeline runner).

### Loop Collector / Agent Call Optimizer
**What's missing:** a tool that sits between agent and API, captures every LLM call, builds a graph of call chains, and detects correction/reflection loops automatically. No existing tool does this from the CLI with local-only storage.

**harmonia** — fills this gap (loop collector + optimizer, universal API).

## Naming Research

### Taken names (conflict risk):
- **aiflow** — conflicts with AIflow, airflow (196K)
- **ai-test** — too generic, 0 search uniqueness
- **promptflow** — Microsoft's PromptFlow
- **langflow** — low-code LangChain
- **agentflow** — several repos with this name
- **phoenix** — Arize Phoenix (observability), widely used metaphor

### Available:
- **harmonia** — no major conflicts (only music repos)
- **promptlane** — no major conflicts
- **llmforge** — no major conflicts
- **prompttrail** — no major conflicts
- **modelrunner** — generic but available
- **chaincraft** — no major conflicts

## Key Insight
The gap is at the intersection of **simplicity** (YAML, one command) and **multi-model orchestration** (chain, compare, route). Most tools are either too complex (agent frameworks) or too narrow (single model).

**Second insight:** loop detection (reflection cycles, correction loops, retry storms) is an untouched niche — no CLI tool visualizes what an agent actually does across a session.
