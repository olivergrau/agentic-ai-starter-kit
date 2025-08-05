# Agentic AI Starter Kit – Polaris Outfitting Co.

Welcome to the **Agentic AI Starter Kit**, featuring a futuristic supply and logistics scenario at **Polaris Outfitting Co.** — a fictional contractor supporting lunar bases, orbital stations, and deep-space missions.

This project offers a **lightweight, hands-on demo** for developers who want to experiment with multi-agent orchestration using `smolagents`, LLM reasoning, and structured communication — without committing to a full-scale AI system.

---

## 🧭 What This Is

This is **not** a production-ready AI template.
It’s a **streamlined demo kit** designed to show how intelligent agents can collaborate, reason, and invoke tools — within a clean, modular, sci-fi-inspired scenario.

You’ll deploy a 5-agent system that processes natural language resupply requests and coordinates everything from inventory validation to procurement decisions and mission reporting.

---

## 🌌 Mission Context

You've been contracted as an AI systems engineer by **Polaris Outfitting Co.**, a key supplier for off-world infrastructure and mission-critical operations.
Polaris specializes in high-tech components and field equipment needed for extraterrestrial installations.

Your job: implement an intelligent multi-agent system that can:

* Parse free-text resupply requests from mission commanders
* Validate inventory and initiate automated restock requests
* Generate quotes with pricing tiers and historical context
* Finalize procurement orders and log transactions
* Provide financial summaries and operational insights

---

## 🤖 Agent Architecture

### 🧠 The 5-Agent System

1. **ParserAgent** – Interprets mission requests in natural language
2. **InventoryAgent** – Checks availability and simulates supplier restocks
3. **QuoteAgent** – Calculates pricing with bulk logic and quote history
4. **OrderAgent** – Logs approved resupply orders
5. **ReportingAgent** – Generates mission financial summaries

Each agent follows a **ReAct-style loop** and communicates via structured `pydantic` models for safe and modular coordination.

---

## 🔁 Agent Orchestration Flow

```
Mission Request → Parse → Inventory Check → Quote Generation → Order Processing → Reporting
```

The central orchestrator coordinates agent calls using a **finite state machine**, handling success, partial fulfillment, and fallback logic.

---

## 🛠 Technology Stack

| Component       | Tech Used                        |
| --------------- | -------------------------------- |
| Agent Framework | `smolagents`                     |
| LLM Integration | OpenAI-compatible APIs           |
| Type Safety     | `pydantic` models                |
| Database        | `SQLite` for transactional state |
| Data Processing | `pandas`                         |
| Workflow Logic  | Custom finite state machine      |

---

## ✨ Key Features

### 🎯 Agentic AI Workflow

* Natural language request parsing
* Bulk pricing tiers (10% for ≥100 units, 15% for ≥500 units)
* Historical quote awareness
* Partial fulfillment support with restock estimation
* ReAct-style reasoning per agent with tool use

### 🚀 Sci-Fi Inventory System

* Realistic space gear: *Ion charge kits*, *carbon mesh panels*, *cryogenic sealants*
* Simulated restocking based on supplier lead times
* Inventory tracking and quote-based procurement logic
* Logging of mission-critical transactions

### 🧪 Testing & Debugging

* Full integration test covering end-to-end mission flow
* Unit tests per agent
* Detailed logs for transparency and traceability

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* OpenAI API key (or compatible endpoint)

### Installation

```bash
git clone <repository-url>
cd polaris-outfitting
pip install -r requirements.txt
```

Create your `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

---

### Usage

**Process a mission quote request:**

```bash
python main.py --init-db --request "We need 150 carbon mesh panels and 80 cryo-sealant cartridges by August 15"
```

**Run from a file:**

```bash
python main.py --file mission_request.txt
```

**Test individual agents:**

```bash
python tests/test_inventory_agent.py
```

---

## 📁 Project Structure

```
polaris-outfitting/
├── main.py                      # CLI entry point
├── orchestrator.py              # Agent flow controller
├── agents/
│   ├── parser_agent.py
│   ├── inventory_agent.py
│   ├── quote_agent.py
│   ├── order_agent.py
│   ├── reporting_agent.py
│   └── message_protocol.py
├── framework/
│   └── state_machine.py
├── tools/
│   └── tools.py
├── data/
│   ├── mission_requests_sample.csv
│   └── quotes.csv
├── tests/
│   ├── test_inventory_agent.py
│   ├── test_quote_agent.py
│   └── test_integration.py
└── Project Notebook.ipynb
```

---

## 📦 Example Output

```bash
$ python main.py --request "200 ion charge kits and 500 carbon mesh panels for delivery next week"

✅ Quote generated:
→ Ion charge kits x200
→ Carbon mesh panels x500
→ Total: $4,125.00 (bulk discount applied)
→ Order confirmed (ID: ORD-1722441600)
→ Estimated delivery: August 15, 2025
```

---

## 📨 Message Protocol Example

```python
QuoteItem(name="carbon mesh panel", quantity=500, unit_price=5.00, discount_percent=15.0)

QuoteResult(
    total_price=2500.00,
    notes="Bulk pricing tier 2 (15%) applied",
    line_items=[...]
)
```

---

## 🧪 Testing

```bash
# Agent unit tests
python tests/test_inventory_agent.py
python tests/test_quote_agent.py

# Full system test
python tests/test_integration.py
```

---

## 🔍 Design Highlights

| Area                     | Detail                                          |
| ------------------------ | ----------------------------------------------- |
| **Modular Architecture** | Agents are cleanly separated and tool-invoking  |
| **FSM Orchestration**    | Workflow transitions via finite state logic     |
| **Structured Messaging** | Pydantic models enforce type safety             |
| **Reasoning Loops**      | ReAct-style agent design with explicit tool use |
| **Production Practices** | Logging, error handling, and full test coverage |

---

## 🌠 Future Extensions

* Add an EngineeringAgent for compatibility checks with existing modules
* Integrate with a simulated space supplier API
* Visualize quotes and delivery pipelines in a mission dashboard
* Embed contextual memory for agents using vector search

---

## 📄 License

This Agentic AI Starter Kit is provided for **educational and exploratory use**.
It is intended to showcase multi-agent orchestration patterns and serve as a springboard for building more advanced LLM-driven systems.

---

**Built with 🚀 curiosity and 🧠 code — powered by smolagents, Python, and black coffee** ☕
