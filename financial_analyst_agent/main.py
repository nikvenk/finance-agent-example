import sys
from pathlib import Path

from dotenv import load_dotenv

# Must run before imports that load tools.py (TavilyClient reads env at import time).
load_dotenv(Path(__file__).resolve().parent / ".env")

from langchain_core.messages import HumanMessage

from graph import build_graph

def research_stock(ticker: str, stream: bool = True) -> str:
    """
    Run the financial research agent on a given ticker.
    Args:
        ticker: Stock symbol - e.g. "AAPL", "RELIANCE.NS", "VEDL.NS"
        stream: If True, prints the ReAct loop steps in real-time
    Returns:
        Final investment brief as a string
    """
    graph = build_graph()
    initial_state = {
        "messages": [
            HumanMessage(
                content=f"Please research {ticker.upper()} and produce a comprehensive "
                        f"investment brief using all available research tools."
            )
        ],
        "ticker": ticker.upper(),
        "financials": {},
        "news_sentiment": {},
        "technical_indicators": {},
        "analyst_ratings": {},
        "investment_brief": "",
    }
    final_brief = ""
    if stream:
        print(f"\n{'='*60}")
        print(f"  Financial Research Agent - {ticker.upper()}")
        print(f"{'='*60}\n")
        for event in graph.stream(initial_state, stream_mode="values"):
            messages = event.get("messages", [])
            if messages:
                last_msg = messages[-1]
                msg_type = type(last_msg).__name__
                if msg_type == "AIMessage":
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        for tc in last_msg.tool_calls:
                            print(f"🔧 Calling tool: {tc['name']}")
                            print(f"   Args: {tc['args']}\n")
                    elif last_msg.content:
                        print("📋 INVESTMENT BRIEF\n")
                        print(last_msg.content)
                        final_brief = last_msg.content
                elif msg_type == "ToolMessage":
                    print(f"✅ Tool result received: {last_msg.name}")
                    content_preview = last_msg.content[:200].replace('\n', ' ')
                    print(f"   Preview: {content_preview}...\n")
    else:
        result = graph.invoke(initial_state)
        final_brief = result["messages"][-1].content
    return final_brief

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("We did not receive a company!")
        sys.exit(1)
    ticker = sys.argv[1]
    research_stock(ticker, stream=True)