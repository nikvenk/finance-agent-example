from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent import SYSTEM_PROMPT, create_agent
from state import AgentState
from tools import TOOLS

def agent_node(state: AgentState) -> dict:
    """
    Core reasoning node. Calls the LLM with the full message history.
    The LLM either:
    - Returns a tool call → routes to tools node
    - Returns a final text response → routes to END
    """
    llm_with_tools = create_agent()
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def build_graph() -> StateGraph:
    """
    Construct and compile the ReAct agent graph.
    Flow:
    START → agent_node → (tool call?) → tools_node → agent_node → ... → END
    """
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("agent", agent_node)
    graph_builder.add_node("tools", ToolNode(TOOLS))
    graph_builder.add_edge(START, "agent")
    # tools_condition checks if the last message has a tool_call.
    # If yes → "tools". If no → END.
    graph_builder.add_conditional_edges("agent", tools_condition)
    # After tools execute, always return to the agent for the next reasoning step
    graph_builder.add_edge("tools", "agent")
    return graph_builder.compile()