#!/usr/bin/python3
"""Run the visual prototype with its own settings and process-local CSS."""
import os
from pathlib import Path
import runpy
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATE = HERE / '.state'
STATE.mkdir(exist_ok=True)
config = STATE / 'config'
if not config.exists():
    shutil.copyfile(HERE / 'config', config)

# Only this process uses Adwaita; desktop preferences are never changed.
os.environ['GTK_THEME'] = 'Adwaita:dark'
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk

screen = Gdk.Screen.get_default()
if screen is None:
    sys.exit('Open this launcher from your desktop session.')
provider = Gtk.CssProvider()
provider.load_from_path(str(HERE / 'style.css'))
Gtk.StyleContext.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

sys.path.insert(0, str(ROOT))
# Some upstream plugins read settings during import, before --config is parsed.
# Redirect Terminator's own lookup as well, without altering child shells' XDG
# configuration directories or loading the user's regular plugins/settings.
from terminatorlib import util
util.get_config_dir = lambda: str(STATE)
from terminatorlib.titlebar import Titlebar
Titlebar.compact_header = True
sys.argv = [str(ROOT / 'terminator'), '--no-dbus', '--config', str(config),
            '--title', 'Terminator — Visual prototype', *sys.argv[1:]]
runpy.run_path(str(ROOT / 'terminator'), run_name='__main__')
