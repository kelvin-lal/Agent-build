"""
Kelvin's Agent
"""

import threading


class CustomTagStore:
    def __init__(self):
        self._tags = []
        self._lock = threading.Lock()

    def add(self, tag):
        if ":" not in tag:
            print(f"Invalid tag format: '{tag}'. Tags must be in key:value format.")
            return False
        with self._lock:
            if tag in self._tags:
                print(f"Tag '{tag}' already exists.")
                return False
            self._tags.append(tag)
        return True

    def remove(self, tag):
        with self._lock:
            if tag in self._tags:
                self._tags.remove(tag)
                return True
        print(f"Tag '{tag}' not found.")
        return False

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


custom_tag_store = CustomTagStore()
