import json
from pathlib import Path

MEMORY_DB_PATH = Path(__file__).parent / 'memory.json'

def load_memory():
    if not MEMORY_DB_PATH.exists():
        MEMORY_DB_PATH.write_text('[]')
    return json.loads(MEMORY_DB_PATH.read_text())

def save_memory(data):
    MEMORY_DB_PATH.write_text(json.dumps(data, indent=2))

def add_snippet(snippet):
    memory = load_memory()
    memory.append(snippet)
    save_memory(memory)

def get_recent_snippets(n=2):
    memory = load_memory()
    return memory[-n:]
