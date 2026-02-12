from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterable, Tuple

def connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL;")
    return con

def init_db(con: sqlite3.Connection) -> None:
    con.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')),
        n_samples INTEGER,
        model_name TEXT,
        notes TEXT
    );
    """)
    con.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        split TEXT,
        mae REAL,
        rmse REAL,
        r2 REAL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(run_id) REFERENCES runs(run_id)
    );
    """)
    con.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')),
        state TEXT,
        message TEXT
    );
    """)
    con.commit()

def log_event(con: sqlite3.Connection, state: str, message: str) -> None:
    con.execute("INSERT INTO events(state, message) VALUES(?, ?)", (state, message))
    con.commit()

def insert_run(con: sqlite3.Connection, n_samples: int, model_name: str, notes: str = "") -> int:
    cur = con.execute(
        "INSERT INTO runs(n_samples, model_name, notes) VALUES(?, ?, ?)",
        (n_samples, model_name, notes),
    )
    con.commit()
    return int(cur.lastrowid)

def insert_metrics(con: sqlite3.Connection, run_id: int, split: str, mae: float, rmse: float, r2: float) -> None:
    con.execute(
        "INSERT INTO metrics(run_id, split, mae, rmse, r2) VALUES(?, ?, ?, ?, ?)",
        (run_id, split, mae, rmse, r2),
    )
    con.commit()
