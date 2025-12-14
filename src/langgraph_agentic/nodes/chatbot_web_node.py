from src.langgraph_agentic.state.state import State

class ChatbotWebNode:
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state:State):
        """
        Process the input state and generate a response with tool integration.
        """
        # Get the user input from the state
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user","content":user_input}])

        tools_response = f"Tool integration for: '{user_input}'"
        return {"messages":[llm_response,tools_response]}
    
    def create_chatbot_web_node(self,tools):
        """
            returns a chatbot node function with tool integration.
        """
        llm_with_tools = self.llm.bind_tools(tools)
        def chatbot_node(state:State):
            """
            Process the input state and generate a response with tool integration.
            """
            llm_response = llm_with_tools.invoke(state["messages"])
            return {"messages":[llm_response]}
        
        return chatbot_node
        
        