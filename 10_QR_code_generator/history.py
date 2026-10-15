"""JSON-backed history manager."""
import json
from datetime import datetime, timezone
from pathlib import Path

class HistoryManager:
    def __init__(self, path="data/history.json", limit=100):
        self.path = Path(path)
        self.limit = limit
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def items(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def add(self, kind, payload):
        data = self.items()
        data.insert(0, {
            "kind": kind,
            "payload": payload,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        self.path.write_text(json.dumps(data[:self.limit], indent=2), encoding="utf-8")
