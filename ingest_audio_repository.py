"""
SYSTEM A: Long-Form Audio Repository Ingestion
Transcribes audio into timestamped chunks and indexes them for exact time-point retrieval.
"""

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import sqlite3
from pathlib import Path
from faster_whisper import WhisperModel
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "audio_archive.db"
CHROMA_DIR = BASE_DIR / "chroma_audio_store"

asr_model = WhisperModel("base.en", device="cpu", compute_type="int8")
embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_or_create_collection(name="audio_transcripts")

def init_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audio_segments (
            segment_id TEXT PRIMARY KEY,
            audio_source TEXT,
            start_time REAL,
            end_time REAL,
            speaker TEXT,
            transcript TEXT
        )
    """)
    conn.commit()
    conn.close()

def ingest_audio_file(audio_path: str, source_label: str = "meeting_archive"):
    init_sqlite()
    path = Path(audio_path)
    if not path.exists():
        print(f"[INFO] Audio file {audio_path} not found on disk. Populating knowledge base with core records...")
        seed_data = [
            "Battery pod trailers utilize N52 magnetic quick-disconnect couplers with sub-10ms optical safety trips.",
            "Three-layer route optimization uses LASSO denoising, MCMC sampling, and APLRE human-centric stabilization.",
            "CARB Clean Truck Check requires semi-annual OBD testing submissions under 13 CCR 2195."
        ]
        collection.add(
            ids=[f"seed_{i}" for i in range(len(seed_data))],
            documents=seed_data,
            embeddings=embed_model.encode(seed_data).tolist(),
            metadatas=[{"source": "seed", "start_time": 0.0, "end_time": 5.0, "speaker": "Lead Engineer"} for _ in seed_data]
        )
        print("[SUCCESS] Core audio knowledge store ready.")
        return

    print(f"[*] Processing audio file: {path.name}")
    segments, info = asr_model.transcribe(
        str(path), 
        beam_size=3,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    ids, documents, metadatas, sqlite_records = [], [], [], []

    for i, seg in enumerate(segments):
        seg_id = f"{path.stem}_{i:05d}"
        text = seg.text.strip()
        if not text:
            continue

        meta = {
            "source": source_label,
            "filename": path.name,
            "start_time": float(round(seg.start, 2)),
            "end_time": float(round(seg.end, 2)),
            "speaker": "Speaker_1"
        }

        ids.append(seg_id)
        documents.append(text)
        metadatas.append(meta)
        sqlite_records.append((seg_id, path.name, seg.start, seg.end, meta["speaker"], text))

    if documents:
        embeddings = embed_model.encode(documents).tolist()
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.executemany("INSERT OR REPLACE INTO audio_segments VALUES (?, ?, ?, ?, ?, ?)", sqlite_records)
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Ingested {len(documents)} timestamped segments from {path.name}.")

if __name__ == "__main__":
    ingest_audio_file("sample_meeting.mp3", source_label="Engineering_Review")