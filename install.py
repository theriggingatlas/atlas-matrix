import os
import sys
import shutil
import maya.cmds as cmds
import platform


def get_os() -> str:
    return platform.system()


def get_maya_version() -> str:
    """Get the current Maya version (e.g., '2024', '2025')"""
    return cmds.about(version=True)


def get_maya_prefs_dir(maya_version: str, user_platform: str) -> str:
    """Get Maya preferences directory based on platform and version"""
    if user_platform == "Windows":
        return os.path.join(
            os.environ["USERPROFILE"],
            "Documents",
            "maya",
            maya_version
        )
    elif user_platform == "Darwin":  # Mac
        return os.path.expanduser(
            f"~/Library/Preferences/Autodesk/maya/{maya_version}"
        )
    else:  # Linux
        return os.path.expanduser(f"~/maya/{maya_version}")


def install_shelf(tools_dir: str, maya_prefs_dir: str) -> bool:
    """Copy shelf files from atlas_matrix/setup/shelves to Maya prefs"""
    source_shelf_dir = os.path.join(tools_dir, "setup", "shelves")
    dest_shelf_dir = os.path.join(maya_prefs_dir, "prefs", "shelves")

    if not os.path.exists(source_shelf_dir):
        print(f"⚠ Shelf directory not found: {source_shelf_dir}")
        return False

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_shelf_dir):
        os.makedirs(dest_shelf_dir)

    # Copy all shelf files
    shelf_files = [f for f in os.listdir(source_shelf_dir) if f.startswith("shelf_")]

    if not shelf_files:
        print(f"⚠ No shelf files found in {source_shelf_dir}")
        return False

    for shelf_file in shelf_files:
        source_file = os.path.join(source_shelf_dir, shelf_file)
        dest_file = os.path.join(dest_shelf_dir, shelf_file)

        try:
            shutil.copy2(source_file, dest_file)
            print(f"✓ Copied shelf: {shelf_file}")
        except Exception as e:
            print(f"❌ Failed to copy {shelf_file}: {e}")
            return False

    return True


def setup_icon_path(tools_dir: str, maya_scripts_dir: str) -> None:
    """Add icon path to userSetup files"""
    icon_dir = os.path.join(tools_dir, "setup", "icons").replace("\\", "/")

    if not os.path.exists(icon_dir):
        print(f"⚠ Icon directory not found: {icon_dir}")
        return

    marker = "# ATLAS_MATRIX_ICON_PATH"

    # MEL setup
    mel_content = f'{marker}\nputenv("XBMLANGPATH", `getenv "XBMLANGPATH"` + ":/{icon_dir}");\n'
    mel_file = os.path.join(maya_scripts_dir, "userSetup.mel")

    # Python setup
    py_content = f'{marker}\nimport maya.mel as mel\nmel.eval(\'putenv("XBMLANGPATH", `getenv "XBMLANGPATH"` + ":/{icon_dir}")\')\n'
    py_file = os.path.join(maya_scripts_dir, "userSetup.py")

    # Add to MEL file
    existing_mel = ""
    if os.path.exists(mel_file):
        with open(mel_file, "r") as f:
            existing_mel = f.read()

    if marker not in existing_mel:
        with open(mel_file, "a") as f:
            if existing_mel and not existing_mel.endswith("\n"):
                f.write("\n")
            f.write("\n" + mel_content)
        print(f"✓ Added icon path to userSetup.mel")

    # Add to Python file
    existing_py = ""
    if os.path.exists(py_file):
        with open(py_file, "r") as f:
            existing_py = f.read()

    if marker not in existing_py:
        with open(py_file, "a") as f:
            if existing_py and not existing_py.endswith("\n"):
                f.write("\n")
            f.write("\n" + py_content)
        print(f"✓ Added icon path to userSetup.py")


def install():
    # --- Detect installer location ---
    this_file = os.path.abspath(__file__)
    tools_dir = os.path.dirname(this_file).replace("\\", "/")

    user_platform = get_os()
    maya_version = get_maya_version()
    separator = ";" if user_platform == "Windows" else ":"

    # Get Maya preferences directory
    maya_prefs_dir = get_maya_prefs_dir(maya_version, user_platform)
    maya_scripts_dir = os.path.join(maya_prefs_dir, "scripts").replace("\\", "/")

    if not os.path.exists(maya_scripts_dir):
        os.makedirs(maya_scripts_dir)

    # Prepare content to add for script path
    marker_mel = f"# ATLAS_MATRIX_SCRIPT_PATH"
    marker_py = f"# ATLAS_MATRIX_SCRIPT_PATH"

    userSetup_mel_content = f'{marker_mel}\nputenv("MAYA_SCRIPT_PATH", `getenv "MAYA_SCRIPT_PATH"` + "{separator}{tools_dir}");\n'
    userSetup_py_content = f'{marker_py}\nimport sys\nif "{tools_dir}" not in sys.path:\n    sys.path.append("{tools_dir}")\n'

    # Process userSetup files (append mode)
    for filename, new_content, marker in [
        ("userSetup.mel", userSetup_mel_content, marker_mel),
        ("userSetup.py", userSetup_py_content, marker_py)
    ]:
        filepath = os.path.join(maya_scripts_dir, filename)

        # Read existing content if file exists
        existing_content = ""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                existing_content = f.read()

        # Check if our setup already exists
        if marker in existing_content:
            print(f"⚠ {filename} already contains Atlas Matrix script path. Skipping...")
            continue

        # Append new content
        with open(filepath, "a") as f:
            if existing_content and not existing_content.endswith("\n"):
                f.write("\n")  # Add newline if file doesn't end with one
            f.write("\n" + new_content)

        print(f"✓ Added Atlas Matrix script path to {filename}")

    # Update environment immediately
    if tools_dir not in os.getenv("MAYA_SCRIPT_PATH", "").split(separator):
        os.environ["MAYA_SCRIPT_PATH"] += f"{separator}{tools_dir}"

    if tools_dir not in sys.path:
        sys.path.append(tools_dir)

    # Setup icon path
    setup_icon_path(tools_dir, maya_scripts_dir)

    # Install shelf
    shelf_success = install_shelf(tools_dir, maya_prefs_dir)

    # Build success message
    message_parts = [
        f"Atlas Matrix installed successfully!",
        f"\nMaya Version: {maya_version}",
        f"Path added to: {maya_scripts_dir}",
    ]

    if shelf_success:
        message_parts.append("\n✓ Shelf installed")
        message_parts.append("✓ Icon path configured")
        message_parts.append("\nPlease restart Maya to see the AtlasMatrix shelf.")
    else:
        message_parts.append("\n⚠ Shelf installation had issues (check Script Editor)")

    cmds.confirmDialog(
        title="Installation Complete",
        message="\n".join(message_parts),
        button=["OK"]
    )


# 1. Required Maya drop function
def onMayaDroppedPythonFile(*args, **kwargs):
    """MANDATORY ENTRY POINT FOR MAYA DRAG-AND-DROP"""
    install()


# 2. Remove old-style execution guard
if __name__ == "__main__":
    install()