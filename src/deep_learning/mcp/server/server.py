# weather_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP_GENERAL")

@mcp.tool()
def substract(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def add(a: int, b: int) -> int:
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    return a / b

@mcp.tool()
async def get_weather(location: str) -> str:
    return f"The weather in {location} is mostly sunny."

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
