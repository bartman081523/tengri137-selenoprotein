"""conftest.py — adds sibling category dirs and sources/ to sys.path.

Pytest collection loads each test as a top-level module, so absolute imports
like `from TORA_TURING_CORRECT import ...` (in `maschine/`) need the `maschine/`
directory on sys.path. This file ensures ALL category folders are reachable.
"""
import sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, PARENT)
# Add ALL sibling category folders
for sibling in os.listdir(PARENT):
    full = os.path.join(PARENT, sibling)
    if os.path.isdir(full) and sibling not in ('.git', '__pycache__'):
        sys.path.insert(0, full)
