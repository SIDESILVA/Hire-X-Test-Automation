import os
import time
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
DEMO_DELAY = float(os.getenv("DEMO_DELAY", 1.2))  # slightly smoother default


def slow_down(multiplier=1.0):
    """
    Controlled human-like delay for demo/smoke stability
    """
    if DEMO_MODE:
        time.sleep(DEMO_DELAY * multiplier)