# Visual prototype

From the repository directory, run:

```sh
./prototype/launch.py
```

This opens a separate Terminator process with two tabs and a split workspace.
It uses the existing terminal engine, shortcuts, menus, and grouping controls.
Blue pane headers indicate the active pane; amber indicates a pane receiving
broadcast input. The terminal colors, spacing, tabs, and focus border are styled
through configuration and CSS. One upstream fix passes the correct widget to
GTK when removing a tab, allowing split layouts to open correctly.
A CSS class on the pane header lets the prototype add spacing without changing
the normal appearance when launched without the prototype stylesheet.
The launcher also enables compact pane headers: folder names with full paths
on hover, symbolic grouping icons with status tooltips, and host names retained
for remote path titles. Custom pane names remain editable and are preserved.

The launcher uses a process-local dark GTK theme and CSS. It copies the seed
configuration to `prototype/.state/config` on first launch. Preferences changed
inside this prototype are saved there, not to your regular Terminator settings.
Close all prototype windows and delete that copy to reset the prototype.

The source configuration is `prototype/config`; the stylesheet is
`prototype/style.css`. Restart the prototype after editing CSS. Changes to the
seed configuration require resetting the saved copy first.

This is a development prototype in the fork, not an installed application.
