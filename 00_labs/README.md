# 00 Labs - Deep Research Agent Development

This collection of Jupyter notebooks demonstrates how to build sophisticated AI agent architectures using Pydantic AI, progressing from simple agents to complete multi-agent research systems.

## Overview

These labs showcase the development of a comprehensive deep research system through a series of progressively complex agent implementations. Each notebook builds upon the previous one, demonstrating key concepts in AI agent design and coordination.

## Lab Progression

### 01_simple_agent.ipynb
**Goal**: Demonstrate basic Pydantic AI agent creation  
**Key Concepts**:
- Simple LLM agents with custom instructions
- Structured output using Pydantic models
- Agent dependencies and state management
- Tool integration for complex tasks
- MCP (Model Context Protocol) server integration

### 02_planner_agent.ipynb  
**Goal**: Create a planning agent that generates structured research plans  
**Key Concepts**:
- Human-in-the-loop interaction
- Nested agent architectures
- Interactive planning processes
- Structured plan generation
- Agent specialization for planning tasks

### 03_researcher_agent.ipynb
**Goal**: Build a researcher agent that executes research plans  
**Key Concepts**:
- Web research automation using Tavily MCP
- Systematic information gathering
- Source tracking and citation management
- Plan-to-content pipeline execution
- Multi-source information synthesis

### 04_writer_agent.ipynb
**Goal**: Develop a writer agent that synthesizes research into reports  
**Key Concepts**:
- Multi-input content synthesis
- Research-to-report transformation
- Structured document generation
- Quality content creation
- Final pipeline integration

### 05_deep_research_architecture.ipynb
**Goal**: Integrate all agents into a complete deep research system  
**Key Concepts**:
- Multi-agent orchestration
- End-to-end research workflow
- Agent coordination and communication
- Complete pipeline automation
- Extensible architecture patterns

## Agent Architecture

The labs demonstrate a three-tier agent architecture:

```
User Query ’ Planner Agent ’ Researcher Agent ’ Writer Agent ’ Final Report
```

1. **Planner Agent**: Analyzes user requests and creates structured research plans
2. **Researcher Agent**: Executes research plans using web search and information gathering
3. **Writer Agent**: Synthesizes research findings into comprehensive, well-structured reports

## Key Technologies

- **Pydantic AI**: Core agent framework providing structured outputs and tool integration
- **MCP (Model Context Protocol)**: Standard for connecting agents to external services
- **Tavily**: Web search and research capabilities
- **Context7**: Code documentation and library search
- **Google Gemini**: Large language model for agent reasoning

## Getting Started

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables in `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   MODEL_NAME=gemini-2.5-flash
   CONTEXT7_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

3. Run the notebooks in order, starting with `01_simple_agent.ipynb`

## What You'll Learn

- How to create reliable AI agents with structured data validation
- Techniques for agent specialization and coordination
- Integration patterns for external services via MCP
- Best practices for multi-agent system design
- Practical approaches to automated research and content generation

Each lab includes detailed explanations, working code examples, and comprehensive conclusions that prepare you for the next level of complexity.