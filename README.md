DebugHindsight

An AI-powered debugging agent with persistent memory.

DebugHindsight helps developers investigate software bugs using relevant debugging experience from the past instead of starting from scratch every time.

The system combines Groq for AI reasoning with Hindsight for persistent memory. When a bug is submitted, DebugHindsight searches previous debugging experiences, checks whether they are genuinely relevant, uses useful experience during the investigation, and stores the new debugging session for future use.

Why DebugHindsight?

Most debugging sessions are treated as isolated events. A developer may solve a problem today, but the useful reasoning, attempted approaches, and lessons from that incident are often difficult to reuse later.

DebugHindsight focuses on that missing layer: persistent debugging memory.

The core cycle is:

Bug Report
    ↓
Recall Previous Experience
    ↓
Check Technical Relevance
    ↓
AI Investigation
    ↓
Recommended Next Steps
    ↓
Store New Experience
    ↓
Future Bugs Benefit From It

The result is a debugging assistant that can build on previous incidents over time.

Key Features

Persistent debugging memory

DebugHindsight stores completed debugging experiences in Hindsight so that technically related incidents can be recalled later.

Relevance-aware recall

The agent does not automatically treat every retrieved memory as useful. Relevance is based on the technical problem, failure mechanism, debugging approach, or solution rather than simply matching a programming language or framework.

AI-assisted investigation

Groq is used to reason about the current bug together with relevant information retrieved from Hindsight.

Structured debugging guidance

Each investigation is presented through four clear sections:

Memory Check

Previous Experience

Current Investigation

Recommended Next Steps

Experience storage

After each debugging session, the result is converted into a reusable debugging experience and stored back in Hindsight.

Debugging history

The frontend maintains a history of previous debugging sessions so developers can review earlier investigations.

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
                              │     Bug Report       │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │    React Frontend    │
                              │      Web UI           │
                              └──────────┬───────────┘
                                         │ HTTP Request
                                         ▼
                              ┌──────────────────────┐
                              │     FastAPI Backend  │
                              │      /api/debug      │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Debugging Agent    │
                              │      Core Logic      │
                              └──────────┬───────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                         ▼                               ▼
                ┌────────────────┐              ┌────────────────┐
                │    Hindsight   │              │      Groq      │
                │ Persistent     │              │ AI Reasoning   │
                │ Memory         │              │                │
                ├────────────────┤              ├────────────────┤
                │ Recall past    │              │ Analyze current│
                │ experiences    │              │ bug            │
                │                │              │                │
                │ Store new      │              │ Use relevant   │
                │ experiences    │              │ context        │
                └───────┬────────┘              └───────┬────────┘
                        │                               │
                        └───────────────┬───────────────┘
                                        ▼
                              ┌──────────────────────┐
                              │ Debugging Result     │
                              ├──────────────────────┤
                              │ Memory Check         │
                              │ Previous Experience  │
                              │ Current Investigation│
                              │ Recommended Steps   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │ Store New Experience │
                              │     in Hindsight     │
                              └──────────┬───────────┘
                                         │
                                         └───────► Future
                                                   Bugs

Memory loop

The most important part of the architecture is the memory loop:

Current Bug
    ↓
Hindsight Recall
    ↓
Relevant Experience
    ↓
Groq Analysis
    ↓
Investigation + Next Steps
    ↓
New Debugging Experience
    ↓
Hindsight Retain
    ↓
Available for Future Bugs

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

The FastAPI backend sends the bug context to Hindsight and retrieves previous debugging experiences that may be relevant.

3. Check relevance

The retrieved memories are evaluated for meaningful technical relevance. Experiences that are unrelated to the actual problem should not be presented as solutions.

4. Investigate with AI

Groq analyzes the current bug together with the relevant debugging context and provides technical reasoning.

The result is organized into:

Memory Check — whether a relevant incident was found

Previous Experience — useful earlier approaches and outcomes

Current Investigation — how the current issue should be investigated

Recommended Next Steps — practical debugging actions

5. Store the new experience

The completed debugging session is saved back into Hindsight as a new memory.

6. Learn from future incidents

When a similar bug appears later, the newly stored experience can be recalled and used during the next investigation.

Example

A developer submits:

My FastAPI API starts timing out when around 50 concurrent users make database requests.

DebugHindsight can retrieve previous experiences involving FastAPI performance, database connection pooling, event-loop blocking, or request throttling when they are technically relevant.

The agent then presents the useful previous experience, investigates the current problem, recommends practical next steps, and stores the new debugging experience.

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

A simple demonstration is to test several bug reports in sequence.

Test 1 — new problem

Submit a bug for which there is no previous relevant experience.

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

These tests demonstrate that DebugHindsight can distinguish between a useful previous debugging experience and an unrelated memory.

Memory Management Utilities

The backend includes utility scripts for checking and cleaning the Hindsight memory bank.

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

Retrieve debugging history

GET

/docs

Open FastAPI Swagger documentation

Security Notes

API credentials are stored locally in backend/.env and excluded from Git through .gitignore.

Never commit API keys, passwords, or other secrets to the repository.

Current Scope

DebugHindsight is a working prototype focused on demonstrating persistent memory for software debugging.

The current implementation uses:

Hindsight as the persistent memory layer

Groq for AI reasoning

FastAPI for the backend API

React for the frontend interface

Future Improvements

Possible future extensions include:

Repository and GitHub integration

Source-code-aware debugging

Automated log and stack-trace collection

Deeper code analysis

More debugging tools and workflows

PostgreSQL-backed application data and analytics

Project Goal

Make debugging improve with experience.

Instead of treating every bug as a completely new problem, DebugHindsight gives an AI debugging agent a persistent memory of what happened before, which approaches were tried, and what was learned.

Author

Deepthi Reddy

GitHub: deepthireddy2488