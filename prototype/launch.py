#!/usr/bin/python3
"""Open the fork with the original demo layout and separate demo settings."""
import os
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATE = HERE / '.state'
STATE.mkdir(exist_ok=True)
config = STATE / 'config'
if not config.exists():
    shutil.copyfile(HERE / 'config', config)

# Keep this convenience launcher for the original two-tab demo layout.
# Appearance now comes entirely from the app itself.
os.execv(sys.executable, [sys.executable, str(ROOT / 'terminator'),
                         '--no-dbus', '--config', str(config),
                         '--title', 'Termino — Demo', *sys.argv[1:]])
