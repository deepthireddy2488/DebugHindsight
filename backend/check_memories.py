import os
import requests
from dotenv import load_dotenv

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = "debughindsight"
BASE_URL = "https://api.hindsight.vectorize.io"

URL = f"{BASE_URL}/v1/default/banks/{BANK_ID}/memories/list"

if not HINDSIGHT_API_KEY:
    print("ERROR: HINDSIGHT_API_KEY was not found in .env")
    exit()

try:
    response = requests.get(
        URL,
        headers={
            "Authorization": f"Bearer {HINDSIGHT_API_KEY}"
        },
        timeout=60
    )

    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        print("\nHindsight Memory Check")
        print("----------------------")

        items = data.get("items", [])

        print(f"Memories found: {len(items)}")

        if not items:
            print("\nBank is empty.")
        else:
            print("\nCurrent memories:\n")

            for index, memory in enumerate(items, start=1):
                print(f"{index}.")
                print(f"   ID: {memory.get('id')}")
                print(f"   Type: {memory.get('fact_type', memory.get('type'))}")
                print(f"   State: {memory.get('state')}")
                print(f"   Text: {memory.get('text')}")
                print()

    else:
        print("\nFailed to retrieve memories.")
        print(response.text)

except requests.RequestException as error:
    print("\nUnable to connect to Hindsight.")
    print(error)