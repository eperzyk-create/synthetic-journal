import json
import os
import sqlite3
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Generator, Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from jsonschema import Draft202012Validator

APP_TITLE = "The Synthetic Journal API"
DB_PATH = os.getenv("TSJ_DB_PATH", "tsj.db")
SCHEMA_PATH = os.getenv("TSJ_SCHEMA_PATH", "tsj_schema.json")

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def sha256_hex(data: str) -> str:
    h = hashlib.sha256()
    h.update(data.encode("utf-8"))
    return h.hexdigest()

def ensure_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
              paper_id TEXT PRIMARY KEY,
              submitted_at TEXT NOT NULL,
              payload_json TEXT NOT NULL,
              llm_record_json TEXT NOT NULL
            );
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_submitted_at ON papers(submitted_at);")
        conn.commit()
    finally:
        conn.close()

def load_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Inicjalizacja
ensure_db()
SCHEMA = load_schema()
VALIDATOR = Draft202012Validator(SCHEMA)

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "ts": utc_now_iso()}

@app.post("/submit-paper")
async def submit_paper(request: Request):
    try:
        payload = await request.json()
        errors = sorted(VALIDATOR.iter_errors(payload), key=lambda e: e.path)
        if errors:
            raise HTTPException(status_code=422, detail="Schema validation failed")
        
        paper_id = payload["paper"].get("paper_id", f"tsj.{uuid.uuid4().hex[:8]}")
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR REPLACE INTO papers(paper_id, submitted_at, payload_json, llm_record_json) VALUES (?, ?, ?, ?)",
            (paper_id, utc_now_iso(), json.dumps(payload), json.dumps(payload))
        )
        conn.commit()
        conn.close()
        return {"status": "accepted", "paper_id": paper_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/archive")
def archive():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT payload_json FROM papers ORDER BY submitted_at DESC").fetchall()
    conn.close()
    return [json.loads(row["payload_json"]) for row in rows]
