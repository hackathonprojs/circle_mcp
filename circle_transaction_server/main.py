import os
import uuid
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from circle.web3 import developer_controlled_wallets
from circle.web3 import utils
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("CIRCLE_API_KEY")
entity_secret = os.getenv("CIRCLE_ENTITY_SECRET")
client = utils.init_developer_controlled_wallets_client(
  api_key=api_key,
  entity_secret=entity_secret
)

# Create FastAPI app
app = FastAPI()

# Serve static files from the root directory
app.mount("/static", StaticFiles(directory="static"), name="static")

code_to_callback = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/transaction")
async def transaction(
    amounts: float = Query(..., description="Amount to transfer"),
    destination_address: str = Query(..., description="Destination wallet address"),
    token_id: str = Query(..., description="Token ID for the transfer"),
    wallet_id: str = Query(..., description="Source wallet ID")
):
    code = str(uuid.uuid4())
    code_to_callback[code] = [amounts, destination_address, token_id, wallet_id]
    return {"link": f"http://127.0.0.1:8000/confirm?code={code}"}

def post_transaction(amounts, destination_address, token_id, wallet_id):
    client = utils.init_developer_controlled_wallets_client(api_key=api_key, entity_secret=entity_secret)
    api_instance = developer_controlled_wallets.TransactionsApi(client)
    request = developer_controlled_wallets.CreateTransferTransactionForDeveloperRequest.from_dict({
        "walletId": wallet_id,
        "tokenId": token_id,
        "destinationAddress": destination_address,
        "amounts": [str(amounts)],
        "feeLevel": 'MEDIUM'
        })
    response = api_instance.create_developer_transaction_transfer(request)
    return response

@app.get("/confirm")
async def confirm(code: str):
    callback = code_to_callback[code]
    post_transaction(callback[0], callback[1], callback[2], callback[3])
    del code_to_callback[code]
    return {"message": "Transaction confirmed"}
    

if __name__ == "__main__":
    print('hi')


