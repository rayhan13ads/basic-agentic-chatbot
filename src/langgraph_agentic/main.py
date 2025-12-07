from src.langgraph_agentic.ui.streamlit_ui.display_result import DisplayResultStreamlit
from src.langgraph_agentic.graph.graph_builder import GraphBuilder
from src.langgraph_agentic.LLMS.groqllm import GroqLLM
from src.langgraph_agentic.ui.streamlit_ui.loadui import LoadStreamlitUI
import streamlit as st

def load_app():

    ui=LoadStreamlitUI()
    user_controls=ui.load_streamlit_ui()

    if not user_controls:
        st.warning("Please select a LLM and a Use Case")
        return
    user_message = st.chat_input("Ask a question about your documents")

    if user_message:
        try:
            ## configure the LLM's
            obj_llm = GroqLLM(user_controls_input=user_controls)
            llm = obj_llm.get_llm_model()
            
            if not llm:
                st.error("LLM Not Configured")
                return
            # Initialize and set up the graph base on usecase
            usecase = user_controls["selected_usecase"]
            if not usecase:
                st.error("Please select a Use Case")
                return
            
            graph_builder = GraphBuilder(model=llm)
            try:
                graph = graph_builder.setup_graph(usecase=usecase)
                if not graph:
                    st.error("Graph Not Configured")
                    return

                display_result = DisplayResultStreamlit(usecase=usecase,graph=graph,user_message=user_message)
                display_result.display_result_on_ui()

                
            except Exception as e:
                st.error(f"Error Ocuured With Exception : {e}")
                return
            
            
        except Exception as e:
            st.error(f"Error Ocuured With Exception : {e}")
    
