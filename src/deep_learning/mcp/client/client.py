import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_ollama import ChatOllama  # Use the local Ollama class
from dotenv import load_dotenv

load_dotenv()
server_params = StdioServerParameters(
                command="python",
                args=[r"C:\Users\Abhishek Raj\Desktop\Machine_Learning\src\deep_learning\mcp\server\server.py"],
)

llm = ChatOllama(
                model="llama3.1", 
                temperature=0,
            )
async def run_agent():
    async with stdio_client(server_params) as(read,write):
        async with ClientSession(read,write) as session:
            print("Initializing MCP session...")
            await session.initialize()

            # 4. Load tools and create the agent
            tools = await load_mcp_tools(session)
            agent = create_agent(llm, tools)

            # 5. Run the query locally
            print("Running agent with local Llama 3.1...")
            response = await agent.ainvoke({
                "messages": [
                    
                    # {"role": "user", "content": "What is 4 * 2"}
                    # {"role": "user", "content": "What is 4 / 2"}
                    {"role": "user", "content": "What is 4 - 2"}
                    # {"role": "user", "content": "what is the weather in mohali?"}
                ]
            })
            
            return response

if __name__ == "__main__":
    try:
        result = asyncio.run(run_agent())
        # print("results here::",result)
        print("\n--- Final Answer ---")
        # Agent results are returned as a list of messages
        print(result["messages"][-1].content) #ectracting the last index of the message key
    except Exception as e:
        print(f"Error: {e}")