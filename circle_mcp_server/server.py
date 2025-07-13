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
        A list of wallet IDs from WALLET_ID and WALLET_ID2 environment variables
    """
    wallet_id = os.getenv("WALLET_ID")
    wallet_id2 = os.getenv("WALLET_ID2")
    
    wallet_ids = []
    
    if wallet_id:
        wallet_ids.append(wallet_id)
    
    if wallet_id2:
        wallet_ids.append(wallet_id2)
    
    return wallet_ids

# for security reason, this function is not part of the MCP server. 
# The actual transfer of money will require confirmation from user. 
# this function is therefore not easily accessible to the LLM.  
# @mcp.tool()
# async def initiate_transfer(amounts: float, destination_address: str, token_id: str, wallet_id: str) -> str:
#     """Initiate a transfer transaction.
    
#     Args:
#         amounts: The amount to transfer (supports decimals)
#         destination_address: The destination address for the transfer
#         token_id: The ID of the token to transfer
#         wallet_id: The ID of the wallet to transfer from
        
#     Returns:
#         The transfer transaction response as a string
#     """
#     api_key = os.getenv("CIRCLE_API_KEY")
#     entity_secret_cipher_text = os.getenv("ENTITY_SECRET_CIPHER_TEXT")
    
#     if not api_key or not api_key.strip():
#         return "Error: CIRCLE_API_KEY environment variable must be set"
    
#     if not entity_secret_cipher_text or not entity_secret_cipher_text.strip():
#         return "Error: ENTITY_SECRET_CIPHER_TEXT environment variable must be set"
    
#     url = "https://api.circle.com/v1/w3s/developer/transactions/transfer"
    
#     # Generate unique UUID for idempotency key
#     # tbd: this should be passed in by the client side.  but we don't know if llm knows how to handle this yet.  this is used to prevent duplicate transaction.  
#     idempotency_key = str(uuid.uuid4())
    
#     payload = {
#         "idempotencyKey": idempotency_key,
#         "entitySecretCipherText": entity_secret_cipher_text,
#         "amounts": [str(amounts)],
#         "feeLevel": "HIGH",
#         "destinationAddress": destination_address,
#         "tokenId": token_id,
#         "walletId": wallet_id
#     }
    
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }
    
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         return response.text
#     except requests.RequestException as e:
#         return f"Exception when calling Circle API: {e}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
