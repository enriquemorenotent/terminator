# Demo layout

The fork now includes the new appearance by default. Run it normally from the
repository directory:

```sh
python3 terminator
```

The fork keeps settings in `~/.config/terminator2` (or
`$XDG_CONFIG_HOME/terminator2`). It does not read or overwrite your installed
Terminator settings. Existing fork profile choices take precedence over the new
defaults. New windows run independently of the installed Terminator process.

For the original two-tab, split-pane demo, you can still run:

```sh
./prototype/launch.py
```

This convenience launcher only selects the demo configuration and layout. It
contains no styling or runtime overrides. Demo preferences remain in
`prototype/.state/config`; delete that file with the demo closed to reset it.

The stylesheet is now `terminatorlib/appearance.css`, and profile defaults live
in `terminatorlib/config.py`. Compact pane headers, full-path tooltips, and
symbolic grouping icons are part of the app. Custom pane names are preserved.

This is a development fork, not an installed application.

Run checks with `python3 tools/test-isolated.py`. This uses a private X11
display, temporary XDG settings, an in-memory settings backend, and a private
D-Bus session. It refuses to run tests if the display isolation check fails.
The runner stops its process group after completion or a 90-second timeout.
Do not run GUI tests directly on your desktop session.
