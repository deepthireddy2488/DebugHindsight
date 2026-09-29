DebugHindsight

An AI-powered debugging agent with persistent memory that learns from previous debugging experiences.

DebugHindsight is an AI-assisted software debugging system designed to make debugging more context-aware, reusable, and experience-driven.

Instead of treating every bug as an isolated incident, DebugHindsight retrieves technically relevant debugging experiences from previous investigations, evaluates their relevance to the current problem, uses them as context for AI-powered analysis, and stores the new investigation for future use.

The result is a persistent debugging memory loop where every completed investigation can improve future debugging sessions.

✨ Why DebugHindsight?
Traditional AI debugging typically starts from the current bug and has no persistent knowledge of how similar problems were solved previously.

DebugHindsight introduces a memory layer into the debugging workflow.

Traditional Debugging
Bug Report
    ↓
AI Investigation
    ↓
Suggested Solution
    ↓
Session Ends

DebugHindsight

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/cc0219d9-f720-4c2e-bc67-e8f4968fa8b1"
    alt="DebugHindsight Memory Flow"
    width="400"
  />
</p>
The key idea is simple:

Every debugging session becomes potential knowledge for the next one.

🚀 Key Features
🧠 Persistent Debugging Memory
DebugHindsight stores completed debugging sessions in Hindsight, allowing future investigations to retrieve relevant experiences.

Stored experiences can include:

The original bug

Technical context

Investigation reasoning

Approaches attempted

Observed outcomes

Root-cause insights

Recommended debugging techniques

🎯 Relevance-Aware Recall
Retrieved memories are not automatically treated as solutions.

DebugHindsight evaluates whether previous experiences are technically relevant to the current problem.

Relevance can come from:

Similar failure mechanisms

Similar system behavior

Similar debugging approaches

Similar root causes

Similar architectural problems

Similar performance or runtime symptoms

A shared programming language or framework alone does not make an experience relevant.

For example:

Current Bug:
FastAPI requests are timing out under concurrent database load.

Potentially Relevant:
✓ Database connection pool exhaustion
✓ Blocking database operations
✓ Event-loop blocking
✓ Request concurrency issues
✓ Connection throttling

Potentially Irrelevant:
✗ React component rendering issue
✗ CSS layout problem
✗ Unrelated authentication bug

🤖 AI-Assisted Investigation
DebugHindsight uses Groq for AI reasoning.

The AI receives:

Current Bug
     +
Relevant Previous Experience
     +
Technical Context
     ↓
AI Investigation
     ↓
Debugging Guidance

This allows the agent to reason about the current problem while taking previous debugging knowledge into account.

📋 Structured Debugging Results
Every investigation is organized into four sections.

1. Memory Check
Determines whether a technically relevant previous debugging experience was found.

2. Previous Experience
Summarizes useful information from earlier debugging incidents.

3. Current Investigation
Analyzes the current bug using the available technical context.

4. Recommended Next Steps
Provides practical actions that can be taken to investigate or resolve the issue.

This structure makes the output easier to understand and act upon.

## 🏗️ System Architecture

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/ce7b1723-3629-4e5b-bf9c-4db031fe8546"
    alt="DebugHindsight System Architecture"
    width="600"
  />
</p>

The architecture creates a continuous learning cycle:

**Recall → Reason → Investigate → Learn → Retain → Recall**
🧩 Core Components
Component	Responsibility
React	User interface and debugging history
Tailwind CSS	Frontend styling
Vite	Frontend development and build tooling
FastAPI	Backend REST API
Debugging Agent	Investigation orchestration
Groq	AI-powered reasoning
Hindsight	Persistent debugging memory
Python	Backend implementation

🛠️ Tech Stack
Frontend
React
Tailwind CSS
Vite

Backend
Python
FastAPI

AI
Groq
Persistent Memory
Hindsight

Development
VS Code
Git
npm

## 📁 Project Structure

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/88b925f3-73b4-43fc-98ef-775accbdefc2"
    alt="DebugHindsight Project Structure"
    width="650"
  />
</p>

⚙️ How It Works
1. Submit a Bug
The developer describes the problem through the React interface.

Example:

My FastAPI API starts timing out when around
50 concurrent users make database requests.

2. Recall Previous Experiences
The backend sends the debugging context to Hindsight.

Hindsight searches the persistent memory for previous debugging experiences that may contain useful technical knowledge.

3. Evaluate Relevance
The agent determines whether retrieved experiences are actually applicable.

The system focuses on technical relationships, rather than simple keyword matching.

For example:

                    ┌──────────────────────┐
                    │    Current Problem   │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             FastAPI    Concurrent Requests  Database
                                             Timeouts
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Search Experience  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Relevance Check    │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌─────────────┐      ┌─────────────┐
             │   Relevant  │      │  Irrelevant │
             └──────┬──────┘      └──────┬──────┘
                    │                    │
                    ▼                    ▼
             Use as Context           Discard


4. Investigate with Groq
Groq analyzes:

Current Bug
     +
Relevant Debugging Experience
     +
Technical Context

The agent produces structured debugging guidance.

5. Present the Result
The frontend displays:

Memory Check
      ↓
Previous Experience
      ↓
Current Investigation
      ↓
Recommended Next Steps

6. Store the Experience
After the investigation is completed, the debugging session is converted into a reusable debugging experience.

That experience is stored in Hindsight.

7. Improve Future Investigations
When a similar bug occurs later, the new experience becomes part of the searchable debugging knowledge base.

This allows the system to progressively accumulate debugging knowledge.

🧪 Example
Initial Bug
My FastAPI API starts timing out when around
50 concurrent users make database requests.

The system may retrieve experiences involving:

Database connection pool exhaustion

Blocking database operations

Event-loop blocking

Request concurrency

Connection limits

Request throttling

The agent then combines relevant previous knowledge with the current bug and produces an investigation.

A future performance issue can potentially retrieve the newly stored experience and build upon it.

🧪 Testing the Memory Loop
DebugHindsight can be tested using a sequence of debugging scenarios.

Test 1 — New Problem
Submit a bug with no previous relevant experience.

Expected behavior:

No relevant previous incident
        ↓
New investigation
        ↓
Experience stored

Test 2 — Similar Problem
Submit a technically similar bug.

Expected behavior:

Relevant incident found
        ↓
Previous experience used
        ↓
New investigation
        ↓
New experience stored

Test 3 — Unrelated Problem
Submit a fundamentally different issue, such as a React rendering problem after a backend performance investigation.

Expected behavior:

No technically relevant incident
        ↓
Current bug investigated independently

These scenarios demonstrate the distinction between persistent memory and blindly reusing previous answers.

🔌 API
Method	Endpoint	Description
POST	/api/debug	Submit a bug for AI-powered debugging
GET	/api/history	Retrieve previous debugging sessions
GET	/docs	Open FastAPI Swagger documentation

🚀 Getting Started
Prerequisites
Install:
Python 3.10+
Node.js
npm
Git
You also need credentials/access for:
Groq
Hindsight

Clone the Repository
git clone https://github.com/deepthireddy2488/DebugHindsight.git
cd DebugHindsight

🔧 Backend Setup
Navigate to the backend:

cd backend

Create a virtual environment:

Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

macOS / Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure Environment Variables

Create:

backend/.env

Add:

GROQ_API_KEY=your_groq_api_key

HINDSIGHT_API_KEY=your_hindsight_api_key

Security: Never commit .env, API keys, passwords, or other secrets to GitHub.

Start the FastAPI server:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

💻 Frontend Setup

Open a second terminal.

Navigate to:

cd frontend

Install dependencies:

npm install

Start the Vite development server:

npm run dev

Open the local URL displayed by Vite, typically:

http://127.0.0.1:5173

🧠 Memory Management

DebugHindsight includes utilities for inspecting and managing stored debugging experiences.


View Stored Memories

cd backend

python check_memories.py

Clear Memories

python clear_memories.py

The cleanup utility asks for confirmation before deleting stored memories.


🔐 Security
DebugHindsight uses API credentials for external AI and memory services.

Follow these practices:

Store credentials in .env

Add .env to .gitignore

Never commit API keys

Never expose secrets in frontend code

Rotate credentials if they are accidentally exposed

Avoid logging sensitive credentials or private debugging information

📌 Current Scope
DebugHindsight is currently a working prototype focused on demonstrating persistent memory for software debugging.

The current implementation provides:

Persistent debugging experiences

Hindsight-based recall

Relevance-aware memory usage

Groq-powered reasoning

FastAPI backend

React frontend

Debugging history

Memory management utilities

🔮 Future Improvements
Potential extensions include:

Repository Integration
Connect debugging investigations directly to GitHub repositories and source code.

Source-Code-Aware Debugging
Allow the agent to inspect relevant files, functions, and dependencies.

Automated Logs & Stack Traces
Automatically collect and analyze:

Stack traces

Application logs

Runtime errors

Performance metrics

Deeper Code Analysis
Add automated static analysis and code-level investigation.

Advanced Debugging Workflows
Introduce specialized workflows for:

Performance debugging

API debugging

Database issues

Frontend errors

Distributed systems

Deployment failures

Analytics
Add PostgreSQL-backed analytics for:

Debugging frequency

Common failure patterns

Resolution rates

Frequently reused experiences

Investigation history

🎯 Project Goal
DebugHindsight aims to make debugging improve with experience.

Instead of treating every software bug as a completely new problem, the system maintains a persistent record of:

What happened
     ↓
What was investigated
     ↓
What approaches were tried
     ↓
What was learned
     ↓
What can be reused

Over time, these experiences become a reusable debugging knowledge base.

Debug once. Remember the experience. Debug better next time.

👩‍💻 Author

Deepthi Reddy

GitHub: deepthireddy2488
