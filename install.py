# -*- coding: utf-8 -*-
import os
import sys
import shutil
import platform
import traceback
import maya.cmds as cmds
import maya.mel as mel

# ----------------------------
# Helpers
# ----------------------------
def _norm(p: str) -> str:
    return os.path.abspath(p).replace("\\", "/")

def get_os() -> str:
    return platform.system()

def get_maya_version() -> str:
    """Get the current Maya version (e.g., '2024', '2025')"""
    return cmds.about(version=True)

def get_maya_prefs_dir(maya_version: str, user_platform: str) -> str:
    """Get Maya preferences directory based on platform and version"""
    if user_platform == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Documents", "maya", maya_version)
    elif user_platform == "Darwin":  # Mac
        return os.path.expanduser(f"~/Library/Preferences/Autodesk/maya/{maya_version}")
    else:  # Linux
        return os.path.expanduser(f"~/maya/{maya_version}")

# ----------------------------
# UserSetup writers (idempotent)
# ----------------------------
SCRIPT_MARKER = "# ATLAS_MATRIX_SCRIPT_PATH"
ICON_MARKER   = "# ATLAS_MATRIX_ICON_PATH"

def _append_once(filepath: str, marker: str, content: str) -> None:
    existing = ""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing = f.read()

    if marker in existing:
        print(f"{os.path.basename(filepath)} already contains marker {marker}, skipping")
        return

    # ensure file ends with a newline
    with open(filepath, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write("\n" + content)
    print(f"Appended block to {os.path.basename(filepath)}")

def write_usersetup_blocks(tools_dir: str, maya_scripts_dir: str) -> None:
    """
    Writes minimal, correct userSetup blocks:
    - Adds the **parent** of atlas_matrix to sys.path so `import atlas_matrix` works
    - Appends icon path to XBMLANGPATH (:/path)
    """
    atlas_dir = _norm(tools_dir)                         # .../atlas_matrix
    parent_dir = _norm(os.path.dirname(atlas_dir))       # parent of atlas_matrix (correct for imports)
    icon_dir = _norm(os.path.join(atlas_dir, "setup", "icons"))

    user_py = os.path.join(maya_scripts_dir, "userSetup.py")
    user_mel = os.path.join(maya_scripts_dir, "userSetup.mel")

    py_block = (
        f"{SCRIPT_MARKER}\n"
        f"import sys\n"
        f"atlas_parent = r\"{parent_dir}\"\n"
        f"if atlas_parent not in sys.path:\n"
        f"    sys.path.append(atlas_parent)\n"
    )

    icon_py_block = (
        f"{ICON_MARKER}\n"
        f"import maya.mel as mel\n"
        f"icon_path = r\"{icon_dir}\"\n"
        f"current_xbm = mel.eval('getenv \"XBMLANGPATH\"')\n"
        f"if icon_path not in current_xbm:\n"
        f"    mel.eval(f'putenv \"XBMLANGPATH\" \"{{current_xbm}}:/{{icon_path}}\"')\n"
    )

    mel_separator = ";" if get_os() == "Windows" else ":"
    mel_block = (
        f"{SCRIPT_MARKER}\n"
        f"putenv(\"MAYA_SCRIPT_PATH\", `getenv \"MAYA_SCRIPT_PATH\"` + \"{mel_separator}{parent_dir}\");\n"
    )

    icon_mel_block = (
        f"{ICON_MARKER}\n"
        f"putenv(\"XBMLANGPATH\", `getenv \"XBMLANGPATH\"` + \":/{icon_dir}\");\n"
    )

    os.makedirs(maya_scripts_dir, exist_ok=True)

    # Write Python userSetup
    _append_once(user_py, SCRIPT_MARKER, py_block)
    _append_once(user_py, ICON_MARKER, icon_py_block)

    # Write MEL userSetup (kept minimal)
    _append_once(user_mel, SCRIPT_MARKER, mel_block)
    _append_once(user_mel, ICON_MARKER, icon_mel_block)

# ----------------------------
# Shelf install & live-load
# ----------------------------
def install_shelf(tools_dir: str, maya_prefs_dir: str) -> bool:
    """Copy shelf files from atlas_matrix/setup/shelves to Maya prefs and return True on success."""
    source_shelf_dir = os.path.join(tools_dir, "setup", "shelves")
    dest_shelf_dir = os.path.join(maya_prefs_dir, "prefs", "shelves")

    source_shelf_dir = _norm(source_shelf_dir)
    dest_shelf_dir = _norm(dest_shelf_dir)

    if not os.path.exists(source_shelf_dir):
        print(f"Shelf source not found: {source_shelf_dir}")
        return False

    os.makedirs(dest_shelf_dir, exist_ok=True)

    shelf_files = [f for f in os.listdir(source_shelf_dir) if f.startswith("shelf_")]
    if not shelf_files:
        print(f"No shelf files found in {source_shelf_dir}")
        return False

    for shelf_file in shelf_files:
        src = os.path.join(source_shelf_dir, shelf_file)
        dst = os.path.join(dest_shelf_dir, shelf_file)
        try:
            shutil.copy2(src, dst)
            print(f"Copied shelf: {shelf_file}")
        except Exception as e:
            print(f"Failed to copy {shelf_file}: {e}")
            return False

    return True

def _inject_runtime_paths_now(tools_dir: str) -> None:
    """Make the current Maya session ready immediately (no restart)."""
    atlas_dir = _norm(tools_dir)
    parent_dir = _norm(os.path.dirname(atlas_dir))
    icon_dir = _norm(os.path.join(atlas_dir, "setup", "icons"))

    # Python import path (parent of atlas_matrix)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
        print(f"✓ Added to sys.path (runtime): {parent_dir}")

    # MEL script path (optional, but nice)
    sep = ";" if get_os() == "Windows" else ":"
    ms_path = os.environ.get("MAYA_SCRIPT_PATH", "")
    if parent_dir not in ms_path.split(sep):
        os.environ["MAYA_SCRIPT_PATH"] = (ms_path + (sep if ms_path else "") + parent_dir)

    # XBMLANGPATH (icons)
    try:
        current_xbm = mel.eval('getenv "XBMLANGPATH"')
        if icon_dir not in current_xbm:
            mel.eval(f'putenv "XBMLANGPATH" "{current_xbm}:/{icon_dir}"')
            print("Icon path added to current session")
    except Exception:
        print("Could not update XBMLANGPATH in current session")
        traceback.print_exc()

def _load_shelf_now(shelf_name: str = "AtlasMatrix") -> None:
    """
    Load the shelf into the current session immediately (if possible).
    Expects a file named shelf_<shelf_name>.mel in prefs/shelves.
    """
    try:
        # loadNewShelf expects the base shelf filename without extension
        mel.eval(f'loadNewShelf "shelf_{shelf_name}"')
        # Optional: select it
        mel.eval('global string $gShelfTopLevel;')
        mel.eval(f'shelfTabLayout -e -selectTab "{shelf_name}" $gShelfTopLevel;')
        print(f"Shelf '{shelf_name}' loaded in current session")
    except Exception:
        print("Could not load shelf immediately (it will appear next launch).")
        traceback.print_exc()

# ----------------------------
# Main install
# ----------------------------
def install():
    # Location of this installer (inside the atlas_matrix package directory)
    this_file = _norm(__file__)
    atlas_dir = _norm(os.path.dirname(this_file))          # .../atlas_matrix
    parent_dir = _norm(os.path.dirname(atlas_dir))         # parent directory (must be on sys.path)
    user_platform = get_os()
    maya_version = get_maya_version()

    maya_prefs_dir = _norm(get_maya_prefs_dir(maya_version, user_platform))
    maya_scripts_dir = _norm(os.path.join(maya_prefs_dir, "scripts"))

    os.makedirs(maya_scripts_dir, exist_ok=True)

    # 1) Write idempotent userSetup blocks
    write_usersetup_blocks(atlas_dir, maya_scripts_dir)

    # 2) Apply paths to the current session (no restart required)
    _inject_runtime_paths_now(atlas_dir)

    # 3) Install shelf files
    shelf_ok = install_shelf(atlas_dir, maya_prefs_dir)

    # 4) Try to load the shelf right now
    if shelf_ok:
        _load_shelf_now("AtlasMatrix")

    # 5) Final dialog
    parts = [
        "Atlas Matrix installed successfully!",
        f"\nMaya Version: {maya_version}",
        f"Scripts path: {maya_scripts_dir}",
        f"Package dir (import root): {parent_dir}",
        "\n✓ Script path configured",
        "✓ Icon path configured",
    ]
    if shelf_ok:
        parts.append("✓ Shelf files copied & loaded")
    else:
        parts.append("⚠ Shelf installation had issues (check Script Editor).")

    cmds.confirmDialog(title="Installation Complete", message="\n".join(parts), button=["OK"])

# Drag-and-drop entry
def onMayaDroppedPythonFile(*args, **kwargs):
    install()

# Optional direct run
if __name__ == "__main__":
    install()
