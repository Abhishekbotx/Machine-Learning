# weather_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

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


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
