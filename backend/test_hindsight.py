import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY"),
    timeout=60.0
)

results = client.recall(
    bank_id="debughindsight",
    query="FastAPI connection pool timeout when many users connect"
)

print("\nRetrieved memories:\n")

for memory in results:
    print(memory)
    print("-" * 60)

client.close()