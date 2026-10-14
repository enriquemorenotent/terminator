#!/usr/bin/python3
"""Run GTK checks on a private X server with disposable settings and D-Bus."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def inside(state, command):
    # Fail before importing tests if any isolation boundary is missing.
    state = Path(state).resolve()
    assert os.environ['GDK_BACKEND'] == 'x11'
    assert 'WAYLAND_DISPLAY' not in os.environ
    assert Path(os.environ['XDG_CONFIG_HOME']).parent == state
    assert os.environ.get('DBUS_SESSION_BUS_ADDRESS')
    assert os.environ['GSETTINGS_BACKEND'] == 'memory'
    import gi
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkX11', '3.0')
    from gi.repository import Gdk, GdkX11
    display = Gdk.Display.get_default()
    assert isinstance(display, GdkX11.X11Display), 'Private X11 display required'
    print('Isolation verified: private X11 display, temporary settings, private D-Bus.', flush=True)
    os.execv(command[0], command)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--inside':
        inside(sys.argv[2], sys.argv[3:])
        return
    command = sys.argv[1:]
    if command[:1] == ['--']:
        command = command[1:]
    if not command:
        command = ['/usr/bin/python3', '-m', 'pytest', 'tests']
    if not Path(command[0]).is_absolute():
        sys.exit('Use an absolute executable path for custom checks.')
    with tempfile.TemporaryDirectory(prefix='terminator2-tests-') as tmp:
        state = Path(tmp)
        # Deliberately do not inherit DISPLAY, Wayland, D-Bus, or GTK variables.
        env = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8',
               'GDK_BACKEND': 'x11', 'GSETTINGS_BACKEND': 'memory',
               'NO_AT_BRIDGE': '1', 'GTK_A11Y': 'none',
               'GIO_USE_VFS': 'local', 'GIO_USE_VOLUME_MONITOR': 'unix',
               'SHELL': '/bin/sh', 'HISTFILE': '/dev/null', 'TERM': 'xterm-256color'}
        for key, directory in [('XDG_CONFIG_HOME', 'config'),
                               ('XDG_CONFIG_DIRS', 'system-config'),
                               ('XDG_DATA_HOME', 'data'),
                               ('XDG_CACHE_HOME', 'cache'),
                               ('XDG_STATE_HOME', 'state'),
                               ('XDG_RUNTIME_DIR', 'runtime')]:
            path = state / directory
            path.mkdir(mode=0o700)
            env[key] = str(path)
        # Avoid missing-config diagnostics and any system config fallback.
        config = state / 'config' / 'terminator2'
        config.mkdir()
        (config / 'config').touch()
        args = ['/usr/bin/dbus-run-session', '--', '/usr/bin/xvfb-run', '-a',
                '-s', '-screen 0 1400x1000x24 -nolisten tcp',
                '/usr/bin/python3', str(Path(__file__).resolve()),
                '--inside', tmp, *command]
        process = subprocess.Popen(args, cwd=ROOT, env=env, start_new_session=True)
        try:
            code = process.wait(timeout=90)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            code = 124
            print('Stopping isolated checks.', flush=True)
        finally:
            # Also clean up dialogs, test shells, Xvfb and private bus on failure.
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
        return code


if __name__ == '__main__':
    sys.exit(main())
