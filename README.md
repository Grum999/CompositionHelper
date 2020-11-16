# Composition Helper

An plugin for [Krita](https://krita.org).


## What is Composition Helper?
*Composition Helper* is a Python plugin made for [Krita](https://krita.org) (free professional and open-source painting program).


It allows to easily create layers with most common composition helpers:
- Rule of third
- Golden section
- Golden spiral
- ...



## Screenshots

![Export file list](https://github.com/Grum999/CompositionHelper/raw/main/screenshots/main.png)


## Functionalities

Here a list of some functionalities:
- Different models of composition helpers
- Choice of line style, color, width
- Preview

![Export file list](https://github.com/Grum999/CompositionHelper/raw/main/screenshots/r1-0-0_main_example.png)

As *Composition Helper* plugin use native [Krita](https://krita.org) layers, many differents helpers can be added and then, easily managed (deletion, visiblity, opacity...)

> **Notes:**
> - Please be aware that *group layer* named `CH# Composition Helpers` is created by plugin and, if you delete or rename it, plugin will recreate it on next helper added :-)
> - If more than on *group layer* named `CH# Composition Helpers` is found, the first one is used


## Download, Install & Execute

### Download
+ **[ZIP ARCHIVE - v1.0.3](https://github.com/Grum999/CompositionHelper/releases/download/1.0.3/compositionhelper.zip)**
+ **[SOURCE](https://github.com/Grum999/CompositionHelper)**


### Installation

Plugin installation in [Krita](https://krita.org) is not intuitive and needs some manipulation:

1. Open [Krita](https://krita.org) and go to **Tools** -> **Scripts** -> **Import Python Plugins...** and select the **compositionhelper.zip** archive and let the software handle it.
2. Restart [Krita](https://krita.org)
3. To enable *Composition Helper* go to **Settings** -> **Configure Krita...** -> **Python Plugin Manager** and click the checkbox to the left of the field that says **Composition Helper**.
4. Restart [Krita](https://krita.org)


### Execute

When you want to execute *Composition Helper*, simply go to **Tools** -> **Scripts** and select **Composition Helper**.


### Tested platforms
Plugin has been tested with Krita 4.4.1 (appimage) on Linux Debian 10

Currently don't kwow if plugin works on Windows and MacOs, but as plugin don't use specific OS functionalities and/resources, it should be ok.



## Plugin's life

### What's new?

_[2020-11-16] Version 1.0.3_

- Plugin is now able to work with document for which color space is not RGBA 8bit/channels (don't crash Krita anymore)

_[2020-11-13] Version 1.0.2_

- Fix minor bug with line color selector

_[2020-11-13] Version 1.0.1_

- Fix invalid reference into Manual

_[2020-11-13] Version 1.0.0_ *[Show detailed release content](https://github.com/Grum999/CompositionHelper/blob/main/releases-notes/RELEASE-1.0.0.md)*

- First implemented/released version!



### Bugs

Yes!
Currently, if you create a layer named `CH# Composition Helpers` that is not a *group layer*, you can't add helper...



### What’s next?

Currently, maybe than using paint layer to build helper, use of vector layer could be an option.
I keep it for the boring days :)


## License

### *Composition Helper* is released under the GNU General Public License (version 3 or any later version).

*Composition Helper* is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

*Composition Helper* is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should receive a copy of the GNU General Public License along with *Buli Commander*. If not, see <https://www.gnu.org/licenses/>.


Long story short: you're free to download, modify as well as redistribute *Composition Helper* as long as this ability is preserved and you give contributors proper credit. This is the same license under which Krita is released, ensuring compatibility between the two.
