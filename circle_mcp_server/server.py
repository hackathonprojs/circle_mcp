import os
import requests
import uuid
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import weave

# Load environment variables
load_dotenv()

weave_client = weave.init("circle-mcp")

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

@mcp.tool()
async def get_balance(wallet_id: str) -> str:
    """Get the balance for a specific wallet.
    
    Args:
        wallet_id: The ID of the wallet to get the balance for
        
    Returns:
        The wallet balance information as a string
    """
    api_key = os.getenv("CIRCLE_API_KEY")
    
    if not api_key or not api_key.strip():
        return "Error: CIRCLE_API_KEY environment variable must be set"
    
    url = f"https://api.circle.com/v1/w3s/wallets/{wallet_id}/balances"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except requests.RequestException as e:
        return f"Exception when calling Circle API: {e}"

@mcp.tool()
async def get_wallet_ids() -> list[str]:
    """Get a list of wallet IDs from environment variables.
    
    Returns:
        A list of wallet IDs belong to this account.  
    """
    wallet_id = os.getenv("WALLET_ID")
    wallet_id2 = os.getenv("WALLET_ID2")
    
    wallet_ids = []
    
    if wallet_id:
        wallet_ids.append(wallet_id)
    
    if wallet_id2:
        wallet_ids.append(wallet_id2)
    
    return wallet_ids

@mcp.tool()
async def prepare_transfer(amounts: float, destination_address: str, token_id: str, wallet_id: str) -> str:
    """Prepare a transfer by generating a link to approve the transaction.
    The user goes to the link to approve the transaction.  
    We want the transactions to be subject to user approval.  
    
    Args:
        amounts: The amount to transfer (supports decimals)
        destination_address: The destination address for the transfer
        token_id: The ID of the token to transfer
        wallet_id: The ID of the wallet to transfer from
        
    Returns:
        A link to the approval page with the parameters as GET parameters
    """
    params = {
        'amounts': str(amounts),
        'destination_address': destination_address,
        'token_id': token_id,
        'wallet_id': wallet_id
    }

    url = "https://circle-transaction-server.fly.dev/transaction"
    params = {
        "wallet_id": wallet_id,
        "amounts": str(amounts),
        "destination_address": destination_address,
        "token_id": token_id
    }
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
