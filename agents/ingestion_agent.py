import os
from pathlib import Path
from typing import Dict, Any, Optional

def _safe_path(user_path: Optional[str], base_dir: Optional[str] = None) -> str:
    """
    Resolve and validate a user-supplied path against the allowed base directory.
    Prevents path traversal and arbitrary file inclusion attacks (CWE-22 / M-2).
    Guaranteed to handle None values safely without Pylance type errors.
    """
    target_path = user_path or ""
    allowed_base = base_dir or str(Path(__file__).resolve().parent)
    
    real = os.path.realpath(os.path.abspath(target_path))
    allowed = os.path.realpath(os.path.abspath(allowed_base))
    
    if not real.startswith(allowed + os.sep) and real != allowed:
        raise ValueError(f"Path traversal or file inclusion attempt detected: {target_path!r}")
    return real

class IngestionAgent:
    """Handles secure document and corpus ingestion with strict path boundary enforcement."""
    
    def __init__(self, storage_directory: Optional[str] = None):
        self.base_dir = storage_directory or str(Path(__file__).resolve().parent)

    def ingest_document(self, file_path: str) -> Dict[str, Any]:
        """Safely opens and ingests a document after validating its physical path boundaries."""
        try:
            # Enforce strict traversal check before opening any file handle
            safe_target = _safe_path(file_path, self.base_dir)
            
            with open(safe_target, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return {
                "status": "success",
                "file_path": safe_target,
                "bytes_read": len(content),
                "message": "Document ingested securely under NIST SI-10 bounds."
            }
        except Exception as e:
            return {
                "status": "error",
                "detail": str(e)
            }

if __name__ == "__main__":
    agent = IngestionAgent()
    print("[INIT] IngestionAgent loaded with active path traversal mitigation.")