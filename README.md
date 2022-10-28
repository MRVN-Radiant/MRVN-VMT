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
$ python3 batch.py ".../extracted Titanfall vpks/materials" ".../Level Editors/MRVN-radiant"
$ deactivate
```

> NOTE: deactivate is to close

Unzip `MRVN_dev_textures.zip` into your `MRVN-radiant/titanfallonline` folder for dev textures  
`scripts/common.shader` is hand-crafted so MRVN-radiant can hide triggers etc. in the viewport


<!-- Guide for extracting Titanfall files, including decompiling `.bsp`s? -->


## TODOs
 * TrenchBroom support
   - need to rename each `.tga` to match the targetted `.vmt`
     this would generate more textures than 1 per `.vtf` 
   - might be easier add Quake3 `.shader` support to TrenchBroom
   - or even `.vmt` & `.vtf` support
 * Convert specific `.mip` / image size limit (for filesizes & performance)
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
   waiting on MRVN `.mdl` support, which is waiting on mdlshit static props & source code release
