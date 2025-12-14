from dotenv import load_dotenv
load_dotenv()
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from langchain_core.tools import BaseTool

try:
    ts = TavilySearch(max_results=2)
    print(f"Created TavilySearch: {ts}")
    print(f"Type: {type(ts)}")
    print(f"Is BaseTool: {isinstance(ts, BaseTool)}")
    
    print("Attempting ToolNode([ts])...")
    try:
        tn = ToolNode([ts])
        print("ToolNode([ts]) worked")
    except Exception as e:
        print(f"ToolNode([ts]) failed: {e}")
        import traceback
        traceback.print_exc()

    print("Attempting ToolNode(ts)...")
    try:
        tn = ToolNode(ts)
        print("ToolNode(ts) worked")
    except Exception as e:
        print(f"ToolNode(ts) failed: {e}")

except Exception as e:
    print(f"Setup failed: {e}")
