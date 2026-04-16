"""
Kelvin's Agent
"""

import os
import math
import socket
import platform
import psutil


class HostTagProvider:
    def __init__(self):
        self._hostname = socket.gethostname()
        self._tags = self._collect_tags()

    def _collect_tags(self):
        tags = [
            f"os:{platform.system().lower()}",
            f"os_version:{platform.release()}",
            f"platform:{platform.machine()}",
            f"hostname:{self._hostname}",
            f"python_version:{platform.python_version()}",
            f"cpu_count:{psutil.cpu_count()}",
            f"total_memory_gb:{math.floor(psutil.virtual_memory().total / (1024 ** 3))}",
            f"env:{os.environ.get('DD_ENV', 'none')}",
        ]

        try:
            tags.append(f"user:{os.getlogin()}")
        except OSError:
            tags.append("user:unknown")

        return tags

    def get_tags(self):
        return list(self._tags)

    def get_hostname(self):
        return self._hostname
