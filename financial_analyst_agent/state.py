from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
"""
The messages field uses add_messages as a reducer [1]. 
This means every time a node updates the state, it appends new messages 
rather than replacing the old ones
Preserves the full Thought → Action → Observation history across the entire loop. 
Without this reducer, each node would overwrite the previous conversation and 
the agent would lose all context of what it had already investigated.
"""


class AgentState(TypedDict):
    # The full message history - drives the ReAct loop
    # add_messages is a reducer: appends new messages rather than overwriting
    messages: Annotated[list[BaseMessage], add_messages]
    
    # The ticker being researched
    ticker: str
    
    # Structured research outputs (populated by tools)
    financials: dict
    news_sentiment: dict
    technical_indicators: dict
    analyst_ratings: dict
    
    # Final output
    investment_brief: str