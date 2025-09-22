# pip install fastapi uvicorn requests
# uvicorn ai_service:app --host 0.0.0.0 --port 8081 for running api, --selftest for troubleshooting

import os, json, requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
 
# logging and CLI for acknowledgements :
import sys
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
 
app = FastAPI()
 
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")     #default port for ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b")             #Best possible model, modelmaxxed, yet to promptmax
SUBJECT_MAX = int(os.getenv("SUBJECT_MAX", "72"))
TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "60"))
 
class EmailIn(BaseModel):
    subject: str
    body: str
    user_priority_overrides: Optional[dict] = Field(default=None)
    user_preferred_tags: Optional[List[str]] = Field(default=None)
 
class EmailOut(BaseModel):
    priority: int
    tags: List[str]
    summary: str
    subject_truncated: str
 
PROMPT_TMPL = """You are a mail triage assistant. Given an email subject, body, and optional user preferences:
- Assign priority as an integer 1 (urgent) to 5 (lowest).
- Produce tags as a JSON array of strings. If user preferred tags are relevant, include them and prefix user-specific ones with '#'.
- Produce a concise summary between 3 and 20 words.
- Return a subject_truncated suitable for dashboards.
 
Constraints:
- Output valid JSON only with keys: priority, tags, summary, subject_truncated.
- priority must be an integer 1..5.
- tags must be a JSON array of strings, e.g. ["registration","#deadlines"].
- summary must be 3 to 20 words.
- subject_truncated must be <= {subject_max} characters (truncate with ellipsis when needed).
- If user overrides exist and clearly match, they take precedence.
 
Inputs:
- subject: {subject}
- body: {body}
- user_priority_overrides: {overrides_json}
- user_preferred_tags: {preferred_tags_json}
 
Priority rules (decide strictly):
- 1 (urgent): Time/venue change or deadlines happening soon. Keywords like: "today", "tomorrow", specific times (e.g., "9am"), "urgent", "immediately", "deadline", "last date", "due", "closes", "rescheduled", "venue change", "time change", "class cancelled", "exam schedule". Treat class venue/time changes or registration deadlines as 1. 
- 2 (high): Action required within a few days (3–7 days), official notices requiring prompt attention.
- 3 (normal): General information or FYI without immediate action. If important information, then 2
- 4 (low): Routine updates with no action or time pressure.
- 5 (lowest): Promotions/ads/marketing.
 
Subject truncation:
- <= {subject_max} characters; if longer, cut and add an ellipsis.
 
If user overrides exist and clearly match, they take precedence.
Return ONLY JSON. No extra text.
 
Examples (for guidance, do not copy text):
- Subject: "Class venue change: 9am today" -> priority: 1
- Subject: "Registration deadline tomorrow 6 PM" -> priority: 1
- Subject: "Exam rescheduled to Monday 2 PM" -> priority: 1
"""
 
def build_prompt(subject: str, body: str, overrides: Optional[dict], preferred: Optional[list]) -> str:
    return PROMPT_TMPL.format(
        subject_max=SUBJECT_MAX,
        subject=json.dumps(subject),
        body=json.dumps(body),
        overrides_json=json.dumps(overrides or {}),
        preferred_tags_json=json.dumps(preferred or []),
    )
 
def call_ollama(prompt: str) -> dict:

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {                                        #added in v0.0.3 for consistient, professional responses, default is 1
        "temperature": 0.2
    }
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=TIMEOUT)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Ollama error: {r.text}")
    data = r.json()
    return json.loads(data.get("response", "{}"))
 
def deterministic_truncate(s: str, max_len: int) -> str:
    s = (s or "").strip()
    if len(s) <= max_len:
        return s
    if max_len <= 1:
        return s[:max_len]
    return s[: max_len - 1].rstrip() + "…"
 
def analyze(inp: EmailIn) -> EmailOut:
    prompt = build_prompt(inp.subject, inp.body, inp.user_priority_overrides, inp.user_preferred_tags)
    m = call_ollama(prompt)
    priority = int(m.get("priority", 3))
    tags = [str(t) for t in (m.get("tags") or [])]
    summary = (m.get("summary") or "").strip()
    subject_truncated = (m.get("subject_truncated") or "").strip()
    if not subject_truncated:
        subject_truncated = deterministic_truncate(inp.subject, SUBJECT_MAX)
    else:
        subject_truncated = deterministic_truncate(subject_truncated, SUBJECT_MAX)
    return EmailOut(priority=priority, tags=tags, summary=summary, subject_truncated=subject_truncated)
 
@app.get("/")
def root():
    return {"status": "ok", "model": OLLAMA_MODEL}
 
@app.get("/ping")
def ping():
    return {"message": "pong"}
 
# endpoint
@app.post("/process_email", response_model=EmailOut)
def process_email(inp: EmailIn):
    return analyze(inp)


 
# v0.0.3 sample endpoint to trigger a demo from the browser/curl
@app.get("/sample", response_model=EmailOut)
def sample():
    demo = EmailIn(
        subject="Class venue change: 9am today",
        body="Class moved to room A-203 at 9:00 AM today. Please arrive 5 minutes early.",
    )
    out = analyze(demo)
    logging.info("Sample output -> priority=%s tags=%s summary=%s subj='%s'",
                 out.priority, out.tags, out.summary, out.subject_truncated)
    return out
 
# v0.0.3 startup check to confirm Ollama is reachable and model is ready
@app.on_event("startup")
def on_startup():
    try:
        # list tags to confirm server is up
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        logging.info("Ollama reachable (%s) -> /api/tags status=%s", OLLAMA_URL, r.status_code)
    except Exception as e:
        logging.warning("Ollama not reachable at startup: %s", e)
 
# testing using cli command python ai_service.py --selftest (temporary change added in v0.0.2)
def self_test():
    demo = EmailIn(
        subject="Registration deadline tomorrow 6 PM",
        body="Complete course registration by 6 PM tomorrow to avoid late fees.",
    )
    out = analyze(demo)
    print("\n-- Self-test result---")
    print(json.dumps(out.model_dump(), indent=2, ensure_ascii=False))
    print("---\n")
 
# temporary change added in v0.0.2
if __name__ == "__main__":
    if "--selftest" in sys.argv:
        self_test()
    else:
        print("Run the API with: uvicorn ai_service:app --host 0.0.0.0 --port 8081")
