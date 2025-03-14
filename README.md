# Composition Helper

> Note: has been moved on Codeberg
> 
> https://codeberg.org/Grum999/CompositionHelper

A plugin for [Krita](https://krita.org).


## What is Composition Helper?
*Composition Helper* is a Python plugin made for [Krita](https://krita.org) (free professional and open-source painting program).


It allows to easily create layers with most common composition helpers:
- Rule of third
- Golden section
- Golden spiral
- ...



## Screenshots

![Export file list](./screenshots/main.png)

## Functionalities

Here a list of some functionalities:
- Different models of composition helpers
- Choice of line style, color, width
- Preview

![Export file list](./screenshots/r1-2-0_main_example.png)

As *Composition Helper* plugin use native [Krita](https://krita.org) layers, many differents helpers can be added and then, easily managed (deletion, visiblity, opacity...)

> **Notes:**
> - Please be aware that *group layer* named `CH# Composition Helpers` is created by plugin and, if you delete or rename it, plugin will recreate it on next helper added :-)
> - If more than on *group layer* named `CH# Composition Helpers` is found, the first one is used


## Download, Install & Execute

### Download
+ **[ZIP ARCHIVE - v1.2.0](https://github.com/Grum999/CompositionHelper/releases/download/1.2.0/compositionhelper.zip)**
+ **[SOURCE](https://github.com/Grum999/CompositionHelper)**


### Installation

Plugin installation in [Krita](https://krita.org) is not intuitive and needs some manipulation:

1. Open [Krita](https://krita.org) and go to **Tools** -> **Scripts** -> **Import Python Plugins...** and select the **compositionhelper.zip** archive and let the software handle it.
2. Restart [Krita](https://krita.org)
3. To enable *Composition Helper* go to **Settings** -> **Configure Krita...** -> **Python Plugin Manager** and click the checkbox to the left of the field that says **Composition Helper**.
4. Restart [Krita](https://krita.org)


### Execute

When you want to execute *Composition Helper*, simply go to **Tools** and select **Composition Helper**.


### Tested platforms
Plugin has been tested with Krita 5.2.2 (Linux Appimage, Windows 10)


## Plugin's life

### What's new?
_[2024-04-14] Version 1.2.0_ *[Show detailed release content](./releases-notes/RELEASE-1.2.0.md)*
- Implement - *New Helpers*
- Implement - *Menu access*
- Implement - *Settings manager
- Fix bug - *Update preview*

_[2023-05-09] Version 1.1.3_
- Fix bug *Krita 5.2.0 Compatibility*
- Fix bug *First Vector layer not added in composition helper group*

_[2022-08-19] Version 1.1.2_ *[Show detailed release content](./releases-notes/RELEASE-1.1.2.md)*

- Fix bug for some Krita Linux installation (not using appimage)

_[2021-01-06] Version 1.1.1_

- Remove forgotten print() call

_[2021-01-06] Version 1.1.0_ *[Show detailed release content](./releases-notes/RELEASE-1.1.0.md)*

- Add option to add helpers as Vector layers instead of Paint layers

_[2020-11-16] Version 1.0.3_

- Plugin is now able to work with document for which color space is not RGBA 8bit/channels (don't crash Krita anymore)

_[2020-11-13] Version 1.0.2_

- Fix minor bug with line color selector

_[2020-11-13] Version 1.0.1_

- Fix invalid reference into Manual

_[2020-11-13] Version 1.0.0_ *[Show detailed release content](./releases-notes/RELEASE-1.0.0.md)*

- First implemented/released version!



### Bugs

Yes!
Currently, if you create a layer named `CH# Composition Helpers` that is not a *group layer*, you can't add helper...



### What’s next?

Currently, nothing :-)
Any idea are welcome.


## License

### *Composition Helper* is released under the GNU General Public License (version 3 or any later version).

*Composition Helper* is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

*Composition Helper* is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should receive a copy of the GNU General Public License along with *Composition Helper*. If not, see <https://www.gnu.org/licenses/>.


Long story short: you're free to download, modify as well as redistribute *Composition Helper* as long as this ability is preserved and you give contributors proper credit. This is the same license under which Krita is released, ensuring compatibility between the two.
