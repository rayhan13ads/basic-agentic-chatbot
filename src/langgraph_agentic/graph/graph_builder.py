from src.langgraph_agentic.nodes.chatbot_web_node import ChatbotWebNode
from src.langgraph_agentic.tools.web_search import create_tool_node
from src.langgraph_agentic.tools.web_search import get_tools
from src.langgraph_agentic.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.graph import StateGraph,START,END
from src.langgraph_agentic.state.state import State
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraph_agentic.nodes.ai_news_node import AINewsNode
class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Build a basic chatbot graph using langgraph.
        this method initializes a chatbot node using the BasicChatbotNode class
        and integrates it into the graph. the chatbot node is set as both the
        entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def chatbot_with_web_search_build_graph(self):
        """
        Build an advanced chatbot with web search graph using langgraph with tool integration.
        this method initializes a chatbot graph that include both a chatbot node and a tool 
        node. It defines tools, initializes a chatbot with web search node, and integrates 
        the chatbot node into the graph. the chatbot node is set as both the entry and exit point of the graph.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        llm = self.llm

        chatbot_node_object = ChatbotWebNode(llm)
        chatbot_node = chatbot_node_object.create_chatbot_web_node(tools)

        #Nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        #Edge
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def ai_news_explorer_build_graph(self):
        """
        Build an AI News Explorer graph using langgraph with tool integration.
        This method initializes a chatbot graph that includes both a chatbot node and a tool 
        node specifically designed for exploring AI news. It defines tools, initializes the 
        chatbot node for AI news exploration, and integrates the chatbot node into the graph. 
        The chatbot node is set as both the entry and exit point of the graph.
        """
        
        ai_news_node = AINewsNode(self.llm)
        
        ## Add nodes and edges for AI News Explorer use case
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)
        
        ## Edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result",END)
    

    def setup_graph(self,usecase):
        """
        Setup the graph based on the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Web Search":
            self.chatbot_with_web_search_build_graph()
        if usecase == "AI News":
            self.ai_news_explorer_build_graph()
        
        return self.graph_builder.compile()