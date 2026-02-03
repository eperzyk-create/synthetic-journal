import json
import os
import sqlite3
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from jsonschema import Draft202012Validator

# Konfiguracja ścieżek
DB_PATH = "tsj.db"
SCHEMA_PATH = "tsj_schema.json"

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS papers (id TEXT PRIMARY KEY, data TEXT)")
    conn.commit()
    conn.close()

def load_validator():
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)
        return Draft202012Validator(schema)

# Start aplikacji
ensure_db()
validator = load_validator()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

@app.post("/submit-paper")
async def submit(request: Request):
    payload = await request.json()
    errors = list(validator.iter_errors(payload))
    if errors:
        raise HTTPException(status_code=422, detail="Błąd schematu")
    
    paper_id = payload["paper"]["paper_id"]
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO papers VALUES (?, ?)", (paper_id, json.dumps(payload)))
    conn.commit()
    conn.close()
    return {"status": "accepted", "id": paper_id}

@app.get("/archive")
def archive():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT data FROM papers").fetchall()
    conn.close()
    return [json.loads(r[0]) for r in rows]
