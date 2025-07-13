import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("circle-developer-controlled-wallet")

@mcp.tool()
async def get_public_key() -> str:
    """Get the public key for the circle api key.
    
    Returns:
        The public key as a string
    """
    api_key = os.getenv("CIRCLE_API_KEY")
    
    if not api_key or not api_key.strip():
        return "Error: CIRCLE_API_KEY environment variable must be set"
    
    url = "https://api.circle.com/v1/w3s/config/entity/publicKey"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except requests.RequestException as e:
        return f"Exception when calling Circle API: {e}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
