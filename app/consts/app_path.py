import os
from pathlib import Path


class AppPath:
    BASE_DIR = Path().resolve()
    APP_DIR = os.path.join(BASE_DIR, 'app')
