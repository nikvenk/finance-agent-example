# Financial Analyst Agent

An agentic financial research assistant powered by NVIDIA NIM and LangGraph. Given a stock ticker, it autonomously uses four research tools to produce a comprehensive investment brief.

## Overview

The agent uses a ReAct loop (LangGraph) to call four tools before writing its final brief:

- **`get_stock_financials`** — P/E, revenue growth, margins, debt, FCF via yfinance
- **`get_news_sentiment`** — Recent headlines and sentiment scoring via Tavily
- **`get_technical_indicators`** — RSI, MACD, SMA50/200, volume analysis
- **`get_analyst_ratings`** — Wall Street consensus and price targets

## Setup

See [`financial_analyst_agent/README.md`](financial_analyst_agent/README.md) for full setup instructions.
