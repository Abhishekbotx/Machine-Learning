# weather_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    return f"The weather in {location} is mostly sunny."


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
