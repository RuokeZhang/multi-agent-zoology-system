# Zoology Multi-Agent Starter

A Flask-based multi-agent demo for zoology Q&A. Three core agents (HabitatAnalyst, SpeciesClassifier, BehaviorSummarizer) collaborate over a shared species knowledge base (10–20 entries) to answer habitat, taxonomy, diet, and behavior questions. Includes simple routing, logging, and a tabbed web UI.

## Quick Start
```bash
# clone repo
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
export FLASK_APP=app.py
flask run  # serves at http://localhost:5000
```

## Features / Endpoints
- `/` — Flask web UI with tabs per agent; submit single-turn questions and see labeled responses.
- `/api/query` (POST JSON: `{ "agent": "habitat|species|behavior", "question": "..." }`) — routes to selected agent; returns answer plus logging metadata.
- Orchestration layer — simple rule-based router to pick agent(s) by intent keywords.
- Knowledge base — curated JSON/SQLite with 10–20 species (taxonomy, habitat, diet, behaviors) shared by all agents.
- Logging — records which agent answered and which data source was used for quick debugging.

## TODO
- [MUST] Implement the three specialized zoology agents and shared data access.
- [MUST] Finish the Flask UI tabs and single-turn question flow per agent.
- [MUST] Populate the curated zoology knowledge base (10–20 species, taxonomy/habitat/diet/behavior).
- [MUST] Complete orchestration/routing logic and ensure responses are labeled.
- [MUST] Add basic evaluation/logging of agent interactions (agent used, data source).
- [OPTIONAL] Add a JournalHistorian-style search agent over a small zoology corpus with citations.
- [OPTIONAL] Generate simple visualizations (habitat distribution, trophic levels) and embed in UI.
- [OPTIONAL] Add a ConservationAdvisorAgent for status-based suggestions.
- [OPTIONAL] Support multi-turn sessions per agent.
- [OPTIONAL] Build a developer console page showing recent multi-agent traces.
