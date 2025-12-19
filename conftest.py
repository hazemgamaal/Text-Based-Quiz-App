import sys
from pathlib import Path


def pytest_configure(config):
    # Ensure project root is on sys.path so tests can import project modules
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
