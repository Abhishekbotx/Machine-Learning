import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_ollama import ChatOllama  # Use the local Ollama class
from dotenv import load_dotenv

load_dotenv()

SERVER_CONFIGS={
    "weather":{
        "command": "python",
        "args": [r"C:\Users\Abhishek Raj\Desktop\Machine_Learning\src\deep_learning\mcp\server\weather_server.py"],
        "transport": "stdio",
    },
    "math":{
        "command": "python",
        "args": [r"C:\Users\Abhishek Raj\Desktop\Machine_Learning\src\deep_learning\mcp\server\weather_server.py"],
        "transport": "stdio",
    }
}
llm = ChatOllama(
                model="llama3.1", 
                temperature=0,
            )
async def run_agent():
    async with stdio_client(server_params) as(read,write):
        async with ClientSession(read,write) as session:
            client = MultiServerMCPClient(SERVER_CONFIGS)
            print("Initializing MCP session...")
            await client.initialize()

            # 4. Load tools and create the agent
            tools = await client.get_tools()
            agent = create_agent(llm, tools)

            # 5. Run the query locally
            print("Running agent with local Llama 3.1...")
            
            
            return response

