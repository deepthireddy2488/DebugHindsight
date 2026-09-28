from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

from agent import debug_bug


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False
        )


class DebugRequest(BaseModel):
    bug: str


@app.get("/")
def home():
    return {
        "message": "DebugHindsight backend is running"
    }


@app.post("/api/debug")
def debug(request: DebugRequest):

    result = debug_bug(request.bug)

    history = load_history()

    new_history = {
        "bug": request.bug,
        "response": result["answer"],
        "memories": result["memories"],
        "memory_found": result["memory_found"],
        "memory_saved": result["memory_saved"],
    }

    history.insert(0, new_history)

    save_history(history)

    return {
        "bug": request.bug,
        "response": result["answer"],
        "memories": result["memories"],
        "memory_found": result["memory_found"],
        "memory_saved": result["memory_saved"],
    }


@app.get("/api/history")
def get_history():

    history = load_history()

    return {
        "history": history
    }