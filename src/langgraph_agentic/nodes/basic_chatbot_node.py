

from src.langgraph_agentic.state.state import State
class BasicChatbotNode:
    """
    A basic chatbot node that takes a model as input and returns a chatbot node.
    """
    def __init__(self,model):
        self.llm = model
    
    def process(self,state:State)->dict:
        """
        Process the state and generate a chatbot response.
        """
        return {
            "messages":self.llm.invoke(state['messages'])
        }