# MRVN-vmt
batch `.vmt` -> `.shader` converter for [MRVN-radiant](https://github.com/F1F7Y/MRVN-radiant)  
Should work for any GtkRadiant or NetRadiant

Gets textures from Titanfall 1 / Titanfall: Online into [MRVN-radiant](https://github.com/F1F7Y/MRVN-radiant)  
You don't need this to compile maps, but it sure helps you see what you're doing

Uses [VTFLibWrapper by Ganonmaster](https://github.com/Ganonmaster/VTFLibWrapper),
which provides python bindings for [Nem's VTFLib](https://web.archive.org/web/20191229074421/http://nemesis.thewavelength.net/index.php?p=40)  
(also used by the [SourceIO](https://github.com/REDxEYE/SourceIO/tree/master/source1/vtf/VTFWrapper) Blender addon)   
See also:
 * [VTFCmd](https://github.com/TitusStudiosMediaGroup/VTFcmd-Resources) another batch tool
 * [panzi/VTFLib](https://github.com/panzi/VTFLib) Linux VTFLib binaries
<!-- reVaMpT; community tool or proprietary? -->


## Installation
Clone this repo:  

```
$ git clone https://github.com/snake-biscuits/MRVN-vmt.git
```  

### Windows
Install dependencies with `pip`  

> NOTE: Don't use Cygwin or MSYS2!
> Need Windows python to target VTFLib binaries

```
$ py -3.9 -m venv venv
$ call venv/scripts/activate
$ python -m pip --upgrade pip
$ python -m pip install -r requirements.txt
```

### Linux
```
$ python3 -m venv venv
$ source venv/bin/activate
$ python -m pip --upgrade pip
$ python -m pip install -r requirements.txt
```
> TODO: Download & compile [panzi/VTFLib](https://github.com/panzi/VTFLib) Linux binaries

> TODO: Test


## Usage
Substitute your own folders here:
```
$ python3 batch.py ".../extracted Titanfall vpks/materials" ".../Level Editors/MRVN-radiant/titanfall2"
$ deactivate
```

> NOTE: `deactivate` is to close the virtual environment (venv)

Unzip `MRVN-radiant_dev_textures.zip` into your `titanfall2` folder for dev textures  
`scripts/common.shader` is hand-crafted so MRVN-radiant can hide triggers etc. in the viewport

`Northstar_example_mod.zip` extracts into `Titanfall2/R2Northstar/mods` & provides in-game textures  

`MRVN-radiant_editor_models.zip` extracts into `titanfall2` folder & provides models for spawnpoints

> NOTE: requires an experimental Northstar build that adds `.vmt` loading from disk
> -- you will need to put textures in either `.vpk` or `.rpak` files otherwise
> -- `.rpak` is recommended for public releases, you may find direct `.vmt` easier for development


<!-- Guide for extracting Titanfall files, including decompiling `.bsp`s? -->


## TODOs
 * Convert specific mip / image size limit (for low filesizes & editor performance)
 * `.vmt` effects in `.shader`
   - BlendModulate
     MRVN-radiant will need to support this in the viewport
   - Proxies & other procedural materials
   - Water
   - Normal & Specular maps
 * Titanfall2 / Apex Legends `.rpak` support
   - Physically Based Rendering in `.shader`
 * Image & `.shader` -> batch of `.vmt`s
 * Model textures
   Waiting on MRVN `.mdl` support
   You can still use other model formats (e.g. `.obj`), but shader paths get funky
