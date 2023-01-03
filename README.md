# SmartScope plugin for Ptolemy

This is a fork of SEMC Ptolemy to add some additional functionality to SmartScope. For more information about Ptolemy visit the [official repository](https://github.com/SMLC-NYSBC/ptolemy) and the [publication](https://arxiv.org/abs/2112.01534).

**For commercial users:** Please make note of the license below before using Ptolemy.

## Added functionality within SmartScope

### Hole location refinement at the medium mag

To ensure accurate targeting of the holes that are found at LM mags, it is important to use the medium Mag in low SA or M to refine the positions. This is crutial especially at large image-shift distance (> 4 um).

SmartScope uses Ptolemy's hole finder algorithm to register the holes at medium mag.

### New protocols

The default SmartScope protocol depends on generating a static hole reference image to realign to the target hole at medium Mag. This can become an issue when multiple hole sizes are used within a single screening session.

New protocol methods and protocols have been digned to generate a average hole template image from the holes found with Ptolemy. This avoids having to use and swap a reference image and provide a more robust template based on the current sample.


## Installation

**This plugin is compatible with SmartScope v0.8b4 and higher.** This version is available in the [dev branch](https://github.com/NIEHS/SmartScope/tree/dev) of the SmartScope repo.

This plugin is considered to be an external plugin for SmartScope. Visit officia documentation for more details about the [plugins](https://docs.smartscope.org/docs/dev/plugins/index.html) and [external plugins](https://docs.smartscope.org/docs/dev/external_plugins/index.html) interfaces.

All the dependencies for Ptolemy are already present after SmartScope installation. 

Installation steps:

```ShellSession
cd /path/to/Smartscope/external_plugins
git clone https://github.com/JoQCcoz/ptolemy-smartscope.git
echo 'ptolemy-smartscope' >> ../config/smartscope/plugins/external_plugins.txt
```

Optionally, we recommend changing the `SmartScope/config/smartscope/default_protocols.yaml` file to automatically take advantage of the new protocols. This will allow the new SPA-Ptolemy protocol to be automatically selected when creating a session.

```yaml
##Use this file to design rules for how to automatically set default protocol for a grid.
- conditions:
    - [holeType.name, NegativeStain]
    - [holeType.name, Lacey]
  mode: any
  protocol: NegativeStain
- conditions:
    - [params_id.bis_max_distance, 0]
  protocol: SPA
- conditions:
    - [holeType.hole_size, '!__None']
    - [params_id.bis_max_distance, '!__0']
    - [params_id.tilt_angle, 0]
  mode: all
  protocol: SPA-Ptolemy
```


## License
This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
