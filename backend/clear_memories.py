import os
import requests
from dotenv import load_dotenv


load_dotenv()


HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = "debughindsight"

BASE_URL = "https://api.hindsight.vectorize.io"

URL = (
    f"{BASE_URL}/v1/default/banks/"
    f"{BANK_ID}/memories"
)


if not HINDSIGHT_API_KEY:
    print("ERROR: HINDSIGHT_API_KEY was not found in .env")
    exit()


print("DebugHindsight Memory Cleanup")
print("-----------------------------")
print(f"Bank: {BANK_ID}")
print()
print("This will permanently delete all memories")
print("inside this bank.")
print("The bank itself will NOT be deleted.")
print()


confirmation = input(
    "Type CLEAR to continue: "
)


if confirmation != "CLEAR":
    print("\nCleanup cancelled.")
    exit()


try:

    response = requests.delete(
        URL,
        headers={
            "Authorization": f"Bearer {HINDSIGHT_API_KEY}"
        },
        timeout=60
    )

    if response.status_code == 200:

        data = response.json()

        print("\nCleanup successful.")
        print(
            f"Deleted memories: "
            f"{data.get('deleted_count', 'unknown')}"
        )

    else:

        print("\nCleanup failed.")
        print(f"Status code: {response.status_code}")
        print(response.text)


except requests.RequestException as error:

    print("\nUnable to connect to Hindsight.")
    print(error)