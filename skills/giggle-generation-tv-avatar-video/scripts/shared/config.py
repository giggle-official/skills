"""Load configuration for Giggle generation HTTP calls.

Environment:
- GIGGLE_API_KEY (required): Sidebar → API key on giggle.pro
- GIGGLE_API_BASE (optional): Defaults to https://giggle.pro—set http://localhost:8090 for local testing
"""

import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def load_config() -> dict:
    """Return api_key and normalized base URL."""
    api_key = os.environ.get("GIGGLE_API_KEY", "").strip()
    base_url = (
        os.environ.get("GIGGLE_API_BASE", "").strip().rstrip("/")
        or "https://giggle.pro"
    )

    if not api_key:
        print(
            "Error: GIGGLE_API_KEY is unset.\n\n"
            "Sign in at https://giggle.pro/, open \"API Key\" in the left sidebar, "
            "create a credential, then export it:\n\n"
            '  export GIGGLE_API_KEY="<your-key>"\n\n'
            "Optional gateway override (defaults to https://giggle.pro):\n"
            '  export GIGGLE_API_BASE="http://localhost:8090"\n',
            file=sys.stderr,
        )
        sys.exit(1)

    return {"api_key": api_key, "base_url": base_url}
