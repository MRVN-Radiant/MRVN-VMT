# MRVN-VMT
batch `.vmt` -> `.shader` converter for [MRVN-Radiant](https://github.com/MRVN-Radiant/MRVN-Radiant)  
Will not work for GtkRadiant OR NetRadiant! (unique `.shader` flags)

Gets textures from Titanfall 1 / Titanfall: Online into [MRVN-Radiant](https://github.com/MRVN-Radiant/MRVN-radiant)  
You don't need this to compile maps, but it sure helps you see what you're doing

See [MRVN-Resource-Pack](https://github.com/MRVN-Radiant/MRVN-Resource-Pack) for dev `textures/`, `shaders/` & `models/`

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
$ git clone https://github.com/MRVN-Radiant/MRVN-vmt.git
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
$ python3 batch.py ".../Titanfall VPK dump/materials" ".../Level Editors/MRVN-Radiant/TitanfallOnline"
$ deactivate
```

> NOTE: `deactivate` is to close the virtual environment (venv)

<!-- Guide for extracting Titanfall files, including decompiling `.bsp`s? -->


## TODOs
 * Convert specific mip / image size limit (for low filesizes & editor performance)
 * `.vmt` effects in `.shader`
   - BlendModulate
     MRVN-Radiant will need to support this in the viewport
   - Proxies & other procedural materials
   - Water
   - Normal & Specular maps
 * Titanfall2 / Apex Legends `.rpak` support
   - Physically Based Rendering in `.shader`
 * Image & `.shader` -> batch of `.vmt`s (R1:O Asset Bakery)
 * Convert `models/` textures
 * `.vtf` -> `.dds` -> `.rpak` (R2 Asset Bakery)
