```
import json
import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from flask import Flask, jsonify, request, render_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zoology-agents")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")

app = Flask(__name__, template_folder="templates", static_folder="static")


def load_knowledge_base(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


KB = load_knowledge_base(DATA_PATH)
INTERACTION_LOG: List[Dict[str, Any]] = []


@dataclass
class AgentResponse:
    agent: str
    answer: str
    sources: List[str]
    trace: List[str]


class BaseAgent:
    name: str

    def answer(self, question: str, kb: Dict[str, Any]) -> AgentResponse:
        raise NotImplementedError


class HabitatAnalystAgent(BaseAgent):
    name = "HabitatAnalyst"

    def answer(self, question: str, kb: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement richer habitat extraction and explanation
        matched = []
        for sp in kb["species"]:
            if "habitat" in question.lower() or sp["name"].lower() in question.lower():
                matched.append(f"{sp['name']}: {sp['habitat']}")
        if not matched:
            matched.append("No direct habitat match found; try specifying species.")
        return AgentResponse(agent=self.name, answer=" | ".join(matched), sources=["knowledge_base.json"], trace=["habitat-scan"])


class SpeciesClassifierAgent(BaseAgent):
    name = "SpeciesClassifier"

    def answer(self, question: str, kb: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement keyword/ML-based species intent detection
        matches = [sp for sp in kb["species"] if sp["name"].lower() in question.lower()]
        if not matches:
            answer = "No species match found; please include species name."
            trace = ["species-none"]
        else:
            details = []
            for sp in matches:
                details.append(f"{sp['name']} ({sp['taxonomy']}): Diet={sp['diet']}, Habitat={sp['habitat']}")
            answer = " | ".join(details)
            trace = ["species-match"]
        return AgentResponse(agent=self.name, answer=answer, sources=["knowledge_base.json"], trace=trace)


class BehaviorSummarizerAgent(BaseAgent):
    name = "BehaviorSummarizer"

    def answer(self, question: str, kb: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement behavior-focused summarization with KB context
        matches = [sp for sp in kb["species"] if sp["name"].lower() in question.lower()]
        if not matches:
            answer = "No behavior info found; specify a species."
            trace = ["behavior-none"]
        else:
            behaviors = [f"{sp['name']}: {sp['behavior']}" for sp in matches]
            answer = " | ".join(behaviors)
            trace = ["behavior-match"]
        return AgentResponse(agent=self.name, answer=answer, sources=["knowledge_base.json"], trace=trace)


AGENTS: Dict[str, BaseAgent] = {
    "habitat": HabitatAnalystAgent(),
    "species": SpeciesClassifierAgent(),
    "behavior": BehaviorSummarizerAgent(),
}


def route_question(question: str, agent_key: Optional[str]) -> AgentResponse:
    # TODO: Implement smarter routing (intent classification / keywords)
    if agent_key and agent_key in AGENTS:
        agent = AGENTS[agent_key]
    else:
        # Default simple rule: route by keyword
        lowered = question.lower()
        if "habitat" in lowered or "where" in lowered:
            agent = AGENTS["habitat"]
        elif "behavior" in lowered or "do they" in lowered:
            agent = AGENTS["behavior"]
        else:
            agent = AGENTS["species"]
    logger.info("Routing to agent=%s", agent.name)
    return agent.answer(question, KB)


@app.route("/")
def index():
    return render_template("index.html", agents=list(AGENTS.keys()))


@app.route("/api/ask", methods=["POST"])
def api_ask():
    payload = request.get_json() or {}
    question = payload.get("question", "")
    agent_key = payload.get("agent")
    resp = route_question(question, agent_key)
    record = {
        "question": question,
        "agent": resp.agent,
        "sources": resp.sources,
        "trace": resp.trace,
        "answer": resp.answer,
    }
    INTERACTION_LOG.append(record)
    logger.info("Interaction: %s", record)
    return jsonify(record)


@app.route("/api/logs", methods=["GET"])
def api_logs():
    return jsonify({"logs": INTERACTION_LOG[-20:]})


@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "ok", "agents": list(AGENTS.keys())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
