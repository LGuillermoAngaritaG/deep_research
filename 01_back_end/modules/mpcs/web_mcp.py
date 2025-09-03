from pydantic_ai.mcp import MCPServerStreamableHTTP

def tavily_mcp(tavily_api_key:str):
    "MCP server for the Tavily API"
    return MCPServerStreamableHTTP(
        url =f'https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}'
    )
