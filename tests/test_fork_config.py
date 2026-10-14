"""Startup must respect explicit settings and ignore the original app's files."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.mark.parametrize('explicit', [False, True])
def test_startup_configuration_is_isolated(tmp_path, explicit):
    legacy = tmp_path / 'terminator'
    legacy.mkdir()
    legacy_config = '[profiles]\n  [[default]]\n    background_color = "#ff0000"\n'
    (legacy / 'config').write_text(legacy_config)
    fork = tmp_path / 'terminator2'
    fork.mkdir()
    (fork / 'config').touch()
    custom = tmp_path / 'custom-config'
    custom.write_text('[profiles]\n  [[default]]\n    background_color = "#123456"\n')
    script = '''
import json
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from terminatorlib import optionparse
from terminatorlib.config import Config
optionparse.parse_options()
config = Config()
print(json.dumps([config['background_color'], config.base.get_config_filename()]))
'''
    command = [sys.executable, '-c', script]
    if explicit:
        command += ['--config', str(custom)]
    result = subprocess.run(command, cwd=Path(__file__).resolve().parents[1],
                            env={**os.environ, 'XDG_CONFIG_HOME': str(tmp_path)},
                            text=True, capture_output=True, check=True, timeout=15)
    assert json.loads(result.stdout) == [
        '#123456' if explicit else '#171b24',
        str(custom if explicit else fork / 'config')]
    assert (legacy / 'config').read_text() == legacy_config
