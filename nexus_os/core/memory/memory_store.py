import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any


class MemoryStore:

    def __init__(self, file_path: str = "memory.json"):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.write_text("[]")
    
    def save(self,record: Dict[str, Any]) -> None:
        """
        Salva um registro de memória no arquivo.
        """
        memory = json.loads(self.file_path.read_text())
        memory.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        })
        self.file_path.write_text(
            json.dumps(memory, indent=2, ensure_ascii=False)
            )
        
    def load_all(self):
        """
        Carrega todas as memórias do arquivo.
        """
        return json.loads(self.file_path.read_text())