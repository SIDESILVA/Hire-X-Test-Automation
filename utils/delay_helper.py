import os
import time
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
DEMO_DELAY = float(os.getenv("DEMO_DELAY", "1.0"))


def slow_down(multiplier=1.0):
    """
    Global controlled delay for demo mode
    """
    if DEMO_MODE:
        time.sleep(DEMO_DELAY * multiplier)