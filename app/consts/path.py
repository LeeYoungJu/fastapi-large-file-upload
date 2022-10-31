import os
from pathlib import Path


class Path:
    BASE_DIR = Path().resolve()
    APP_DIR = os.path.join(BASE_DIR, 'app')
