from src.langgraph_agentic.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.graph import StateGraph,START,END
from src.langgraph_agentic.state.state import State

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
    

    def setup_graph(self,usecase):
        """
        Setup the graph based on the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        else:
            st.error("Invalid Use Case")
            return
        
        return self.graph_builder.compile()