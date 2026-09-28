import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY"),
    timeout=60.0
)

BANK_ID = "debughindsight"

results = hindsight.recall(
    bank_id=BANK_ID,
    query="FastAPI timeout database connection pool concurrent users"
)

print("\nRetrieved memories:\n")

for memory in results[:5]:
    print(memory)
    print("-" * 60)

hindsight.close()