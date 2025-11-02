# 🧩 Common Issues & Troubleshooting — Atlas Matrix

This page lists common setup and runtime issues you might encounter while using **Atlas Matrix**, along with simple steps to fix them.

---

## ⚙️ Installation & Launch Issues

### 🟥 Issue: *“Atlas Matrix doesn’t show up in Maya.”*

**Possible causes:**
- The `atlas_matrix` folder isn’t inside Maya’s `scripts` directory or your sys path inside userSetup.py isn't set correctly.
- Maya wasn’t restarted after installation.
- You’re running an older Maya version (requires Maya 2020+).

**✅ Solution:**
1. Confirm your folder path:
Documents/maya/<version>/scripts/atlas_matrix/
2. Restart Maya.
3. In Maya’s Python tab, try running:
```python
import importlib
from atlas_matrix.ui.parent_con import dialog
importlib.reload(dialog)
dialog.show()
```
If it still doesn’t appear, open Script Editor → History tab, check for import errors.

### 🟥 Issue: “ModuleNotFoundError: No module named atlas_matrix”

**Cause:** Maya can’t find the package in its Python path.

**✅ Solution:**

Ensure atlas_matrix is placed directly in Documents/maya/scripts/.

Check the Python path inside Maya:

```python
import sys
for path in sys.path:
    print(path)
```

Confirm your scripts folder appears in that list.

### 🟥 Issue: “UI opens but appears blank or distorted.”

**Cause:** Qt version mismatch — Atlas Matrix uses Pyside2 / Qt5 and PySide6 / Qt6, supported only in Maya 2017+.

** ✅ Solution: **

Make sure you are running Maya 2020 or newer.

If necessary, delete your Maya preferences: `Documents/maya/<version>/prefs/`

## 🧱 Constraint Behavior Issues

### 🟥 Issue: “Maintain Offset doesn’t seem to work.”

**Cause:** The driven object already has frozen transforms or non-zero parent space.

**✅ Solution:**

Try enabling Maintain Offset before creating the constraint.

If it’s already constrained:

1. Delete the constraint.
2. Recreate it with Maintain Offset checked.

## 🧩 UI & Interaction Issues

### 🟥 Issue: “Some checkboxes or sliders are greyed out.”

**Cause:** The ‘All’ toggle for that section is active.

**✅ Solution:**

Uncheck “All” to enable the individual X/Y/Z controls.

### 🟥 Issue: “The UI window keeps duplicating when reopened.”

**Cause:** Maya doesn’t automatically close old instances.

**✅ Solution:**

Close all Atlas Matrix windows before reopening.

Or, add a safety snippet in your launcher:

```python
from maya import cmds
if cmds.window('atlas_matrix_parent', exists=True):
    cmds.deleteUI('atlas_matrix_parent')
```

## 🧠 Advanced Debugging

If the UI fails silently:

1. Open Script Editor → History tab.
2. Check for lines containing: `atlas_matrix.ui.parent_con`
3. Copy any error messages and contact support (see `README.md`).

## 🧰 Resetting Atlas Matrix

If you experience persistent crashes or UI corruption:

1. Delete preferences: `Documents/maya/<version>/prefs/`
2. Reinstall `Atlas Matrix`. 
3. Restart Maya.
