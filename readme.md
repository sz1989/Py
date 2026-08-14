# Python AI & Automation Experiments

This folder contains a small set of Python scripts for experimenting with AI agents, web APIs, and financial data.

## Tech Stack

| Category | Technologies |
|----------|---------------|
| **Language** | Python 3.12 |
| **AI/LLM** | Google Generative AI, OpenAI, LangChain, LangGraph |
| **Web Framework** | FastAPI, Uvicorn, Starlette |
| **Data Processing** | Pandas, NumPy, yfinance |
| **HTTP & APIs** | requests, httpx, Google API Python Client |
| **Data Validation** | Pydantic |
| **Database/ORM** | Peewee |
| **Environment Management** | python-dotenv |
| **Development Tools** | Jupyter, JupyterLab, IPython, Jupyter Notebook |
| **Async Runtime** | asyncio, grpcio |

## Files Overview

- agent.py
  - A simple Gemini-powered agent demo that lists files in the current directory.
  - Technologies: Google GenAI, python-dotenv

- agentForOrder.py
  - A customer support-style agent that can check mock order status and escalate issues.
  - Technologies: Google GenAI, python-dotenv

- agentForStockPrice.py
  - An AI agent that answers stock-related questions using tools for price lookup and company summaries.
  - Technologies: LangChain, LangChain Google GenAI, yfinance, python-dotenv

- ai.py
  - A basic example that sends text to Gemini for summarization.
  - Technologies: Google Generative AI SDK, python-dotenv

- joke.py
  - Fetches a random dad joke from an online API.
  - Technologies: requests

- main.py
  - A FastAPI app that exposes an endpoint to ask the stock agent a question.
  - Technologies: FastAPI

- realtimeMutualFundNav.py
  - A live dashboard-style script that estimates a mutual fund NAV from real-time stock price changes.
  - Technologies: yfinance, datetime, decimal, time

## Overall Theme

These scripts are mostly learning projects focused on:
- AI agents and tool calling
- Gemini / LangChain integrations
- financial market data retrieval
- simple web service APIs
