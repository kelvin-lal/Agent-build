"""
Kelvin's Agent
"""

import threading
from agent.settings import settings


class CustomTagStore:
    def __init__(self):
        self._lock = threading.Lock()
        saved = settings.load()
        self._tags = list(saved.get("custom_tags", []))

    def add(self, tag):
        if ":" not in tag:
            print(f"Invalid tag format: '{tag}'. Tags must be in key:value format.")
            return False
        with self._lock:
            if tag in self._tags:
                print(f"Tag '{tag}' already exists.")
                return False
            self._tags.append(tag)
        self._persist()
        return True

    def remove(self, tag):
        with self._lock:
            if tag in self._tags:
                self._tags.remove(tag)
            else:
                print(f"Tag '{tag}' not found.")
                return False
        self._persist()
        return True

    def get_tags(self):
        with self._lock:
            return list(self._tags)

    def list_tags(self):
        with self._lock:
            if not self._tags:
                print("No custom tags configured.")
                return
            for i, tag in enumerate(self._tags, 1):
                print(f"  {i}. {tag}")

    def _persist(self):
        data = settings.load()
        with self._lock:
            data["custom_tags"] = list(self._tags)
        settings.save(data)


custom_tag_store = CustomTagStore()
