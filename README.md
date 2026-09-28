DebugHindsight

An AI-powered debugging agent with persistent memory.

DebugHindsight helps developers investigate software bugs using previous debugging experience instead of starting from scratch every time.

The system combines Groq for AI reasoning with Hindsight for persistent memory. When a bug is submitted, DebugHindsight searches past debugging experiences, identifies genuinely relevant incidents, uses those experiences during the investigation, and stores the new debugging session for future use.

Why DebugHindsight?

Traditional AI debugging tools can analyze the current error, but each debugging session may begin with little or no knowledge of what was tried before.

DebugHindsight focuses on the missing piece: long-term debugging memory.

For every bug, the agent follows a simple cycle:

Bug Report
    ↓
Recall Previous Experience
    ↓
Check Relevance
    ↓
AI Investigation
    ↓
Recommended Next Steps
    ↓
Store New Experience
    ↓
Future Bugs Benefit From It

This allows the debugging process to improve through accumulated experience.

Key Features

Persistent debugging memory

DebugHindsight stores completed debugging experiences in Hindsight so they can be recalled when a future problem is technically related.

Relevance-aware recall

The agent does not treat every retrieved memory as useful. A previous experience is considered relevant based on the technical problem, failure mechanism, debugging approach, or solution rather than simply sharing the same programming language or framework.

AI-assisted investigation

Groq is used to analyze the current bug together with the retrieved debugging experience and provide technical reasoning.

Practical next steps

The system generates a structured investigation and a clear set of debugging actions instead of returning only a general explanation.

Experience storage

After each debugging session, the investigation is converted into a reusable debugging experience and stored back in Hindsight.

Debugging history

The frontend keeps a history of previous debugging sessions so developers can review earlier investigations.

Tech Stack

Layer

Technology

Frontend

React, Tailwind CSS

Backend

Python, FastAPI

AI reasoning

Groq

Persistent memory

Hindsight

Frontend tooling

Vite

Development

VS Code

System Architecture

                         ┌──────────────────────┐
                         │      Developer       │
                         │   Enters Bug Report  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      React UI        │
                         │   DebugHindsight     │
                         └──────────┬───────────┘
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │    /api/debug        │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌────────────────┐           ┌────────────────┐
             │    Hindsight   │           │      Groq      │
             │ Recall Memory  │           │ AI Reasoning   │
             └───────┬────────┘           └───────┬────────┘
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Debugging Result   │
                         │ • Memory Check       │
                         │ • Previous Experience│
                         │ • Investigation      │
                         │ • Next Steps         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Store New Experience│
                         │    in Hindsight      │
                         └──────────────────────┘

Project Structure

DebugHindsight/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── check_memories.py
│   ├── clear_memories.py
│   ├── test_hindsight.py
│   ├── test_recall.py
│   ├── requirements.txt
│   ├── history.json
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── .gitignore
│
└── README.md

How It Works

1. Submit a bug

The developer describes the problem through the React interface.

2. Recall previous experience

The FastAPI backend sends the bug context to Hindsight and retrieves previous debugging experiences related to the issue.

3. Check relevance

Retrieved memories are evaluated for meaningful technical relevance. Unrelated experiences are not presented as useful solutions.

4. Investigate with AI

Groq analyzes the current bug and the relevant previous experience. The result is organized into:

Memory Check

Previous Experience

Current Investigation

Recommended Next Steps

5. Store the new experience

The completed debugging session is saved back into Hindsight as a new memory.

6. Learn from future incidents

When a similar bug appears later, the newly stored experience can be retrieved and used as part of the next investigation.

Example

Suppose a developer reports:

My FastAPI API starts timing out when around 50 concurrent users make database requests.

DebugHindsight can recall earlier experiences involving FastAPI performance, database connection pooling, event-loop blocking, or request throttling when they are technically relevant.

The agent then presents the previous approaches, investigates the current problem, recommends next debugging actions, and stores the new experience.

A later performance issue can therefore benefit from what was learned during the earlier session.

Getting Started

Prerequisites

Make sure the following are installed:

Python 3.10+

Node.js and npm

Git

You also need access to:

Groq

Hindsight

1. Clone the repository

git clone https://github.com/deepthireddy2488/DebugHindsight.git
cd DebugHindsight

2. Set up the backend

Open a terminal in the project root and run:

cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a file named .env inside backend/:

GROQ_API_KEY=your_groq_api_key
HINDSIGHT_API_KEY=your_hindsight_api_key

Do not commit .env to GitHub.

Start the FastAPI server:

uvicorn main:app --reload

The backend will be available at:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

3. Set up the frontend

Open a second terminal:

cd frontend
npm install
npm run dev

Open the local Vite URL shown in the terminal, normally:

http://127.0.0.1:5173

Testing the Memory Loop

A simple demonstration is to test the same type of problem more than once.

Test 1 — new problem

Submit a bug that has no previous relevant experience.

Expected behavior:

No related incident
Experience saved

Test 2 — similar problem

Submit a technically similar bug again.

Expected behavior:

Related incident found
Previous debugging experience was used
Experience saved

Test 3 — unrelated problem

Submit a different type of bug, such as a React rendering issue after testing a backend performance problem.

Expected behavior:

No related incident

This demonstrates that DebugHindsight is not simply matching keywords or returning every memory as relevant.

Memory Management Utilities

The backend includes small utility scripts for checking and cleaning the Hindsight memory bank.

Check stored memories:

python check_memories.py

Clear the memory bank:

python clear_memories.py

The cleanup script asks for confirmation before deleting memories.

API Endpoints

Method

Endpoint

Purpose

POST

/api/debug

Submit a bug for AI-powered debugging

GET

/api/history

Retrieve recent debugging history

GET

/docs

Open FastAPI Swagger documentation

Security Notes

API credentials are stored locally in backend/.env and are excluded from Git through .gitignore.

Never commit API keys, passwords, or other secrets to the repository.

Current Scope

DebugHindsight is a working prototype focused on demonstrating persistent memory for software debugging. The current implementation uses Hindsight as the memory layer, Groq for reasoning, FastAPI for the backend, and React for the user interface.

Future versions can extend the system with richer debugging tools, source-code analysis, repository integration, automated log collection, and additional developer workflows.

Project Goal

The goal of DebugHindsight is simple:

Make debugging improve with experience.

Instead of treating every bug as a completely new problem, the system gives an AI debugging agent a persistent memory of what happened before, what approaches were tried, and what was learned.

Author

Deepthi Reddy
GitHub: deepthireddy2488