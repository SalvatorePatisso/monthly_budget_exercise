import os

def load_dotenv(dotenv_path=None):
    """Minimal implementation of load_dotenv.
    Reads key=value pairs from the file and sets them in os.environ if not already present."""
    if dotenv_path is None:
        return False
    try:
        with open(dotenv_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())
        return True
    except FileNotFoundError:
        return False
