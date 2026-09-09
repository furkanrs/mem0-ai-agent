# Mem0 AI Agent

A practical implementation of **Mem0 memory for AI agents**, demonstrating both Mem0 Cloud and Mem0 Open Source with persistent long-term memory.

The project includes a local customer-support AI agent using **Mem0, Qdrant, Ollama, Qwen 2.5 3B, and Nomic Embed Text** to remember important customer information across conversations.

---

## Architecture

```text
Customer
   ↓
User Query
   ↓
Mem0.search()
   ↓
Relevant Memories
   ↓
User Query + Memories
   ↓
Qwen 2.5 3B
   ↓
AI Response
   ↓
Mem0.add()
   ↓
Memory Processing
   ↓
Nomic Embed Text
   ↓
Embeddings
   ↓
Qdrant
   ↓
Long-Term Memory
```

### Core Idea

**Qwen talks to the customer. Mem0 manages what the system remembers about the customer.**

---

## Project Structure

```text
mem0-ai-agent/
│
├── cloud/
│   └── email_example.py
│
├── docker/
│   └── docker-compose.yml
│
├── oss/
│   ├── config.py
│   ├── memory_demo.py
│   └── support_agent.py
│
├── 01-mem0-cloud-quickstart.py
├── 02-mem0-oss-quickstart.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Features

- Mem0 Cloud quickstart
- Mem0 Cloud email memory example
- Mem0 Open Source implementation
- Local Qdrant vector database
- Local Ollama LLM and embeddings
- Qwen 2.5 3B for response generation
- Nomic Embed Text for embeddings
- Customer-specific persistent memory
- Semantic memory retrieval

---

# Mem0 Cloud

The project includes two Mem0 Cloud examples.

### Cloud Quickstart

`01-mem0-cloud-quickstart.py`

Demonstrates:

```text
MemoryClient
     ↓
   add()
     ↓
  search()
     ↓
  get_all()
```

Run:

```powershell
python 01-mem0-cloud-quickstart.py
```

Requires a Mem0 Cloud API key.

### Email Memory Example

`cloud/email_example.py`

Demonstrates using Mem0 to store and retrieve useful information from email conversations.

Run:

```powershell
python cloud/email_example.py
```

Requires a Mem0 Cloud API key.

---

# Mem0 Open Source

The Open Source implementation runs locally using:

- Mem0
- Qdrant
- Ollama
- Qwen 2.5 3B
- Nomic Embed Text

Unlike the Cloud examples, the main Open Source implementation runs locally using Ollama for the LLM and embedding model.

---

# Qdrant + Docker

Qdrant is used as the **vector database** for storing and retrieving vector representations of memories.

Start Qdrant:

```powershell
docker compose -f docker/docker-compose.yml up -d
```

Check the container:

```powershell
docker ps
```

---

# Local Models

## Qwen 2.5 3B

Used as the local LLM for:

- Understanding the user's request
- Using retrieved memory as context
- Generating the response

```powershell
ollama pull qwen2.5:3b
```

## Nomic Embed Text

Used to convert memories and queries into vector representations for semantic search.

```powershell
ollama pull nomic-embed-text
```

Check installed models:

```powershell
ollama list
```

---

# Customer Support AI Agent

The main application is:

```text
oss/support_agent.py
```

The agent maintains long-term memory for individual customers.

Example:

```text
Customer:
My order number is 12345 and it hasn't arrived.
```

Later:

```text
Customer:
What is my order number?
```

The agent retrieves the relevant memory:

```text
Agent:
Your order number is 12345.
```

This allows the agent to remember useful information across conversations.

---

# Memory Flow

```text
User Query
    ↓
Mem0.search()
    ↓
Relevant Customer Memories
    ↓
Qwen 2.5 3B
    ↓
AI Response
    ↓
Mem0.add()
    ↓
Memory Processing
    ↓
Embedding
    ↓
Qdrant
```

Mem0 manages the memory layer, while Qdrant stores the vector representations used for semantic retrieval.

---

# Customer-Specific Memory

Each customer is associated with a unique `user_id`.

```text
Customer 123
    ├── Order information
    ├── Delivery issues
    └── Previous support information

Customer 456
    ├── Different order information
    └── Different support information
```

This keeps memories associated with the correct customer.

---

# LLM vs Mem0

## Qwen

```text
Qwen
 ├── Understands the user's request
 ├── Uses provided context
 └── Generates the response
```

## Mem0

```text
Mem0
 ├── Searches existing memories
 ├── Retrieves relevant memories
 ├── Processes conversations for useful memories
 ├── Creates/updates memories
 └── Manages long-term memory
```

Simple way to remember it:

```text
Qwen = Brain that communicates

Mem0 = Memory system that remembers
```

---

# Embeddings and Semantic Search

Embeddings allow the system to find memories based on meaning rather than exact wording.

```text
Memory / Query
      ↓
Nomic Embed Text
      ↓
Vector
      ↓
Qdrant
      ↓
Semantic Similarity Search
      ↓
Relevant Memory
```

For example:

```text
Stored memory:
Customer's order number is 12345.

Query:
Which order did I place?
```

Even though the wording is different, semantic search can identify the related memory.

---

# Technologies

| Technology | Purpose |
|---|---|
| Python | Application |
| Mem0 | AI memory management |
| Qdrant | Vector database |
| Ollama | Local model runtime |
| Qwen 2.5 3B | Local LLM |
| Nomic Embed Text | Embeddings |
| Docker | Runs Qdrant |
| python-dotenv | Environment configuration |

---

# Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start Qdrant

```powershell
docker compose -f docker/docker-compose.yml up -d
```

### 4. Pull Ollama Models

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

---

# Running the Project

### Mem0 Cloud Quickstart

```powershell
python 01-mem0-cloud-quickstart.py
```

### Email Memory Example

```powershell
python cloud/email_example.py
```

### Mem0 OSS Quickstart

```powershell
python 02-mem0-oss-quickstart.py
```

### Memory Demo

```powershell
python oss/memory_demo.py
```

### Customer Support Agent

```powershell
python oss/support_agent.py
```

---

# Mem0 Cloud vs Open Source

```text
              Mem0
                │
       ┌────────┴────────┐
       ↓                 ↓
  Mem0 Cloud        Mem0 Open Source
       │                 │
       │          ┌──────┴──────┐
       │          ↓             ↓
       │       Ollama         Qdrant
       │          │
       │       Qwen + Nomic
       │
    Hosted            Local
```

**Mem0 Cloud** provides a hosted memory service through its API.

**Mem0 Open Source** allows the memory system to be run locally with components such as Qdrant and Ollama.

---

# What I Learned

This project helped me understand:

- AI agent memory
- Long-term memory
- Memory extraction and retrieval
- Embeddings
- Vector databases
- Semantic search
- Mem0 Cloud vs Open Source
- Local LLMs and embeddings
- Customer-specific memory
- Persistent memory across conversations

---

# Interview Explanation

> I built a local customer-support AI agent using Mem0 for long-term memory. Before generating a response, the agent searches Mem0 for relevant memories associated with the customer and provides them as context to a local Qwen LLM. After the interaction, Mem0 processes the conversation to identify useful information for future interactions. The memories are represented as embeddings and stored in Qdrant for semantic retrieval.

### Simple Explanation

> I built a customer-support AI agent with long-term memory. Qwen handles the conversation and generates responses, while Mem0 manages the memory layer. The system retrieves relevant customer memories using semantic search and provides them to the LLM as context. After the conversation, useful information is stored as persistent memory using embeddings and Qdrant.

---

# Key Concept

```text
Qwen
  ↓
Talks and responds

Mem0
  ↓
Manages memory

Nomic Embed Text
  ↓
Converts text into vectors

Qdrant
  ↓
Stores and retrieves vectors
```

**The goal of this project is to demonstrate how an AI agent can move beyond a stateless chatbot and maintain useful long-term memory for individual customers.**
