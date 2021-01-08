Blender Gimel Studio Addon
==========================

Blender 2.8+ bridge addon allowing users to edit rendered images from Blender in <a href="https://github.com/Correct-Syntax/Gimel-Studio">Gimel Studio</a>.


# Download

v0.2.5 Alpha release can be found [here](https://github.com/Correct-Syntax/Blender-Gimel-Studio-Addon/releases).


# Status

**STILL WIP!** Currently, only basic, usable functionality is implemented.


# Planned Features

- Add multiple Image nodes to the Gimel Studio node graph via the addon (useful for layers).


# Installation & Setup

1. Install like a normal Blender addon and enable it.
2. Specify the path to the Gimel Studio application in the addon preferences.


# Usage

1. Make sure your blender file is saved to your hard-drive and render your image with keyboard shortcut ``F12``.
2. Click on the *Compositor* tab and check the *Use Nodes* checkbox.
3. Access the addon in the Blender compositor (right) panel, *Gimel Studio* tab.
4. Click the *Launch Gimel Studio* button and your render will appear in the launched Gimel Studio instance.

**Notes:**

 - Integrates with Gimel Studio v0.5.0 beta and onwards only.
 - Blender file must be saved.
 - Scene must be rendered.


# Contributing

PRs, feedback and great ideas are welcome!