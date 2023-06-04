# MRVN-vmt (c) by Bikkie / snake-biscuits [b!scuit#3659]
#
# MRVN-vmt is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
"""generate .vmt files from a folder of .vtf files"""
from __future__ import annotations
import fnmatch
import os
import re
from typing import Set

from PIL import Image
from VTFLibWrapper import VTFLib  # need appropriate compiled VTFLib
# see VTFLibWrapper/README.md for links to Linux version


__version__ = "1.1.0"
# NOTE: cannot be bothered to convert .vmt proxies
# TODO: Titanfall 2 rpak .json materials -> .shader


patterns = {"above_water": re.compile(r'\s"?$abovewater"? "?(0|1)"?'),
            "alpha_test": re.compile(r'\s"\$alphatest"\s1'),
            "base_texture": re.compile(r'\s"\$basetexture"\s"(.*)"'),
            "base_texture_2": re.compile(r'\s"\$basetexture2"\s"(.*)"'),
            "compile_nodraw": re.compile(r'\s"\%compilenodraw"\s1'),
            "decal": re.compile(r'\s"\$decal"\s1'),
            "shader": re.compile(r'"?([a-zA-Z_]+)"?'),
            "tool_texture": re.compile(r'\s%tooltexture\s"(.*)"'),
            "translucent": re.compile(r'\s"\$translucent"\s"1"')}

shader_vertex_type = {"Basic": "unlit",
                      "LightmappedGeneric": "litbump",
                      "Refract": "unlitts",
                      "UnlitTwoTexture": "unlit",
                      "VertexLitGeneric": "unlit",  # sometimes unlitts
                      "Water": "litflat"}
# NOTE: Water *_beneath ($abovewater 0) is unlit
# TODO: indentify conditions for unlitts VertexLitGeneric
# -- some $alphatest 1 model vmts are unlit
# -- some materials w/ no transparency flags are unlitts


class VMT:
    above_water: bool = True  # special case when False
    base_texture: str = ""
    base_texture_2: str = None  # *_bm only
    is_trans: bool = False
    shader_type: str = ""
    tool_texture: str = None
    compile_flags: Set[str]
    content_flags: Set[str]  # TODO: sets CM_UNIQUE_CONTENTS (same as source + some new ones)
    surface_flags: Set[str]  # TODO: sets TEXTURE_DATA.flags (sky & vertex only)

    def __init__(self):
        self.compile_flags = set()
        self.content_flags = set()
        self.surface_flags = set()

    @classmethod
    def from_file(cls, filename: str) -> VMT:
        out = cls()
        with open(filename) as vmt_file:
            for line in vmt_file:
                for check, pattern in patterns.items():
                    match = re.match(pattern, line)
                    if match is None:
                        continue
                    if check in ("alpha_test", "translucent"):
                        out.is_trans = True
                    elif check == "above_water":
                        out.above_water = bool(int(match.groups()[0]))
                    elif check == "base_texture":
                        out.base_texture = match.groups()[0].replace("\\", "/")
                    elif check == "base_texture_2":
                        out.base_texture_2 = match.groups()[0].replace("\\", "/")
                    elif check == "compile_nodraw":
                        out.compile_flags.add("nodraw")
                    elif check == "decal":
                        out.compile_flags.add("decal")
                    elif check == "shader":
                        out.shader_type = match.groups()[0]
                        out.shader = shader_vertex_type[out.shader_type]
                    elif check == "tool_texture":
                        out.tool_texture = match.groups()[0].replace("\\", "/")
                    else:
                        raise NotImplementedError(f"i forgor {check}")
        if out.is_trans:
            out.shader = "unlitts"
        if out.shader_type == "Water" and not out.above_water:
            out.shader = "unlit"
        return out


def vtf_to_tga(vtf_filename: str, tga_filename: str):
    vtf = VTFLib.VTFLib()
    vtf.image_load_from_buffer(open(vtf_filename, "rb").read())
    vtf_rgba32 = bytes(vtf.convert_to_rgba8888().contents)
    tga = Image.frombytes("RGBA", (vtf.width(), vtf.height()), vtf_rgba32, "raw")
    os.makedirs(os.path.dirname(tga_filename), exist_ok=True)
    tga.save(tga_filename)


def filename(folder: str, base: str, ext: str) -> str:
    return os.path.join(folder, f"{base}.{ext}").replace("\\", "/")


# MRVN-Radiant
# see: https://github.com/MRVN-Radiant/MRVN-Radiant/blob/main/tools/remap/source/games.cpp
def convert_folder(materials_dir: str, titanfall_dir: str, subfolder: str = "", recurse=False, verbose=False):
    # e.g. "../titanfall1_extracted_textures", "C:/MRVN-radiant/titanfallonline"
    materials_dir = os.path.realpath(materials_dir)  # src
    titanfall_dir = os.path.realpath(titanfall_dir)  # dest
    shaders_dir = os.path.join(titanfall_dir, "shaders")
    textures_dir = os.path.join(titanfall_dir, "textures")
    top_folder = os.path.join(materials_dir, subfolder)
    for folder in os.listdir(top_folder):
        vmt_folder = os.path.join(top_folder, folder)
        if not os.path.isdir(vmt_folder):
            continue
        shader_prefix = subfolder.replace("\\", "/").replace("/", "_") + "_" if subfolder != "" else ""
        if verbose:
            print(f"*** {shader_prefix}{folder}.shader")
        shader_file = open(os.path.join(shaders_dir, f"{shader_prefix}{folder}.shader"), "w")
        shader_file.write("// Generated by MRVN-VMT\n")
        count = 0
        for vmt_filename in fnmatch.filter(os.listdir(vmt_folder), "*.vmt"):
            # .vmt
            vmt = VMT.from_file(os.path.join(vmt_folder, vmt_filename))
            if vmt.base_texture == "" and vmt.tool_texture is None:
                if verbose:
                    print(f"!!! {vmt_filename} has no texture !!!")
                continue
            # TODO: convert as much of the shader as possible
            shader_name = os.path.join("textures", subfolder, folder, vmt_filename[:-4])
            shader_file.write(f"\n{shader_name}\n" + "{\n")
            texture = vmt.base_texture if vmt.tool_texture is None else vmt.tool_texture
            # TODO: add more shaders to MRVN-Radiant/tools/remap/source/games.cpp
            # shader_file.write(f'\t"$shadertype" "{vmt.shader_type}"\n')
            bt_path = os.path.join("textures", texture).replace("\\", "/")
            shader_file.write(f"\t$basetexture {bt_path}.tga\n")
            if vmt.base_texture_2 is not None:
                bt2_path = os.path.join("textures", vmt.base_texture_2).replace("\\", "/")
                shader_file.write(f"\t$basetexture_2 {bt2_path}.tga\n")
            if vmt.is_trans:
                shader_file.write("\t%trans 1.00\n")  # use texture alpha
            shader_file.write("}\n")
            # .vtf
            vtf_filename = filename(materials_dir, texture, "vtf")
            if not os.path.exists(vtf_filename):
                if verbose:
                    print(f"!!! {vmt_filename} texture {texture} not found !!!")
                continue
            # vtf_to_tga(vtf_filename, filename(os.path.join(MRVN_dir, MRVN_game), shader_name, "tga"))
            # ^ rename vtf to shader_name, good for trenchbroom
            if vmt.base_texture != "":
                vtf_to_tga(vtf_filename, filename(textures_dir, vmt.base_texture, "tga"))
            if vmt.base_texture_2 != "":
                vtf_to_tga(vtf_filename, filename(textures_dir, vmt.base_texture_2, "tga"))
            if vmt.tool_texture is not None:
                vtf_to_tga(vtf_filename, filename(textures_dir, vmt.tool_texture, "tga"))
            count += 1
        shader_file.close()
        if verbose:
            print(f"--- {count} materials converted")
        if count == 0:
            os.remove(os.path.realpath(shader_file.name))
        if recurse:
            convert_folder(materials_dir, titanfall_dir, os.path.join(subfolder, folder), True, verbose=verbose)


# TrenchBroom
def convert_folder_trenchbroom(materials_dir: str, tga_dir: str, subfolder: str = "", recurse=False, verbose=False):
    # e.g. "../titanfall1_extracted_textures", ".../TrenchBroom maps/Titanfall/textures"
    # NOTE: subfolder should be a subfolder of materials
    # NOTE: no .shader; straight to 1 .tga per material name
    materials_dir = os.path.realpath(materials_dir)  # src
    tga_dir = os.path.realpath(tga_dir)  # dest
    top_folder = os.path.join(materials_dir, subfolder)
    for folder in os.listdir(top_folder):
        vmt_folder = os.path.join(top_folder, folder)
        if not os.path.isdir(vmt_folder):
            continue
        count = 0
        for vmt_filename in fnmatch.filter(os.listdir(vmt_folder), "*.vmt"):
            # .vmt
            vmt = VMT.from_file(os.path.join(vmt_folder, vmt_filename))
            if vmt.base_texture == "" and vmt.tool_texture is None:
                if verbose:
                    print(f"!!! {vmt_filename} has no texture !!!")
                continue
            shader_name = os.path.join("textures", "world", subfolder, folder, vmt_filename[:-4])
            texture = vmt.base_texture if vmt.tool_texture is None else vmt.tool_texture
            # .vtf
            vtf_filename = filename(materials_dir, texture, "vtf")
            if not os.path.exists(vtf_filename):
                if verbose:
                    print(f"!!! {vmt_filename} texture {texture} not found !!!")
                continue
            vtf_to_tga(vtf_filename, filename(tga_dir, shader_name, "tga"))
            count += 1
        if verbose:
            print(f"--- {count} materials converted")
        if recurse:
            convert_folder_trenchbroom(materials_dir, tga_dir, True, os.path.join(subfolder, folder), verbose=verbose)


if __name__ == "__main__":
    import sys

    # materials_dir = "E:/Mod/TitanfallOnline/TitanFallOnline/assets_dump/materials"
    # titanfall_dir = "E:/Mod/_tools/Source Engine - Respawn/MRVN-Radiant/TitanfallOnline"
    if len(sys.argv) == 3:
        materials_dir, titanfall_dir = sys.argv[1:]
    # elif len(sys.argv) == 1:
    #     pass  # use defaults
    else:
        print(f'Usage: {sys.argv[0]} "Titanfall materials dir" "MRVN-Radiant TitanfallOnline dir"')
        print('\tif you can\'t find your "Titanfall/materials" folder, extract it from the .vpks')
        sys.exit()

    sys.stdout.reconfigure(line_buffering=True)  # for piping print to logfile
    convert_folder(materials_dir, titanfall_dir, subfolder="dev", recurse=True, verbose=True)
    convert_folder(materials_dir, titanfall_dir, subfolder="world", recurse=True, verbose=True)
    # TODO: concatenate .shader files together into a top-level .shader for each world/ folder
    # TODO: generate shadertags .xml for easier navigation
