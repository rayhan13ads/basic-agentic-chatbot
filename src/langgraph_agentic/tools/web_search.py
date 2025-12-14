from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

def get_tools():
    """ 
    Retrun the list of tools to be used in the chatbot
    """
    tools = [TavilySearch(max_results=2)]
    return tools

def create_tool_node(tools):
    """
        creates and returns a tool node from the list of tools
    """
    tool_node = ToolNode(tools)
    return tool_node