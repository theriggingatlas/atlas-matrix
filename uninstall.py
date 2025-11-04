import os
import sys
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


def remove_shelf(maya_prefs_dir: str) -> bool:
    """
    Remove the Atlas Matrix shelf from the UI and from disk.
    """
    dest_shelf_dir = os.path.join(maya_prefs_dir, "prefs", "shelves")
    shelves_prefs_file = os.path.join(maya_prefs_dir, "prefs", "shelvesPrefs.mel")

    print(f"Checking shelf directory: {dest_shelf_dir}")

    shelf_ui_names = ["AtlasMatrix", "Atlas"]
    for shelf_ui in shelf_ui_names:
        if cmds.shelfLayout(shelf_ui, exists=True):
            try:
                cmds.deleteUI(shelf_ui, layout=True)
                print(f"Shelf UI '{shelf_ui}' deleted from Maya session")
            except Exception as e:
                print(f"Failed to delete shelf UI '{shelf_ui}': {e}")

    if not os.path.exists(dest_shelf_dir):
        print(f"Shelf directory not found: {dest_shelf_dir}")
        return True

    shelf_files = os.listdir(dest_shelf_dir)
    shelf_prefixes = ["shelf_AtlasMatrix", "shelf_Atlas"]
    valid_extensions = [".mel", ".json"]
    removed_count = 0

    for shelf_file in shelf_files:
        if any(shelf_file.startswith(prefix) and shelf_file.endswith(ext)
               for prefix in shelf_prefixes for ext in valid_extensions):
            shelf_path = os.path.join(dest_shelf_dir, shelf_file)
            try:
                os.remove(shelf_path)
                print(f"Removed shelf file: {shelf_file}")
                removed_count += 1
            except Exception as e:
                print(f"Failed to remove {shelf_file}: {e}")

    if removed_count == 0:
        print("No matching Atlas Matrix shelf files found to remove")

    return True


def remove_from_usersetup(filepath: str, marker: str) -> bool:
    """Remove marked sections from userSetup files"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return True  # Nothing to remove

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()

        # Find and remove lines between marker and next non-related line
        new_lines = []
        skip_mode = False
        found_marker = False

        for line in lines:
            if marker in line:
                skip_mode = True
                found_marker = True
                continue

            if skip_mode:
                # Skip lines that are part of the Atlas Matrix setup
                if line.strip() == "" or line.strip().startswith("#"):
                    continue
                elif "ATLAS_MATRIX" in line or "atlas_matrix" in line.lower():
                    continue
                elif "putenv" in line or "sys.path.append" in line or "mel.eval" in line:
                    # Skip the actual setup lines
                    skip_mode = False
                    continue
                else:
                    skip_mode = False

            new_lines.append(line)

        if found_marker:
            # Write back the cleaned content
            with open(filepath, "w") as f:
                f.writelines(new_lines)
            print(f"Removed Atlas Matrix entries from {os.path.basename(filepath)}")
        else:
            print(f"No Atlas Matrix entries found in {os.path.basename(filepath)}")

        return True

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return False


def uninstall():
    user_platform = get_os()
    maya_version = get_maya_version()

    # Get Maya preferences directory
    maya_prefs_dir = get_maya_prefs_dir(maya_version, user_platform)
    maya_scripts_dir = os.path.join(maya_prefs_dir, "scripts").replace("\\", "/")

    success_count = 0
    total_tasks = 4

    # Remove from userSetup.mel
    mel_file = os.path.join(maya_scripts_dir, "userSetup.mel")
    if remove_from_usersetup(mel_file, "# ATLAS_MATRIX_SCRIPT_PATH"):
        success_count += 1

    # Remove from userSetup.py
    py_file = os.path.join(maya_scripts_dir, "userSetup.py")
    if remove_from_usersetup(py_file, "# ATLAS_MATRIX_SCRIPT_PATH"):
        success_count += 1

    # Remove icon paths from userSetup files
    if remove_from_usersetup(mel_file, "# ATLAS_MATRIX_ICON_PATH"):
        success_count += 1
    if remove_from_usersetup(py_file, "# ATLAS_MATRIX_ICON_PATH"):
        # Don't increment here since we already counted py_file
        pass

    # Remove shelf
    if remove_shelf(maya_prefs_dir):
        success_count += 1

    # Build result message
    message_parts = [
        f"Atlas Matrix Uninstallation Complete!",
        f"\nMaya Version: {maya_version}",
        f"Script directory: {maya_scripts_dir}",
    ]

    if success_count >= total_tasks - 1:
        message_parts.append("\n✓ Script paths removed from userSetup files")
        message_parts.append("✓ Icon paths removed")
        message_parts.append("✓ Shelf files removed")
        message_parts.append("\n⚠ Please restart Maya to complete uninstallation.")
        message_parts.append("\nNote: The Atlas Matrix tool files themselves were not deleted.")
        message_parts.append("You can safely delete the atlas_matrix folder manually if desired.")
    else:
        message_parts.append("\n⚠ Some steps encountered issues (check Script Editor)")

    cmds.confirmDialog(
        title="Uninstallation Complete",
        message="\n".join(message_parts),
        button=["OK"]
    )


# Required Maya drop function
def onMayaDroppedPythonFile(*args, **kwargs):
    """MANDATORY ENTRY POINT FOR MAYA DRAG-AND-DROP"""
    uninstall()


if __name__ == "__main__":
    uninstall()