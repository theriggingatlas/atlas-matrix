# 🚀 Quick Start - Atlas Matrix 1.0.0 - Maya

Welcome to **Atlas Matrix**, the open-source Maya matrix constraint tool designed for artists and riggers who want full control with a clean, PySide6-based interface.

---

## ⚙️ Installation

### 🧩 Automatic Setup (Recommended)

1. Open Maya (2025+).
2. Drag and drop the file `atlas_matrix/setup/install.py` directly into your Maya viewport.
3. Restart Maya.
4. You’ll now see a new shelf named **AtlasMatrix** in your Maya shelf bar.

✅ *That’s it! You’re ready to use Atlas Matrix.*

---

### 🪛 Manual Setup

1. Copy the `atlas_matrix/` folder into your Maya scripts directory:

    - **Windows** : `~\Documents\maya\<version>\scripts\`
    - **macOS** : `~/Library/Preferences/Autodesk/maya/<version>/scripts/`
    - **Linux** : `~/Library/Preferences/Autodesk/maya/<version>/scripts/`

2. Copy the icon file `atlas_matrix/setup/atlas_matrix_parent.png` into: `Documents/maya/prefs/icons/`

3. Open Maya’s **Script Editor** → **Python Tab** and paste the following:

```python
import importlib
from atlas_matrix.ui.parent_con import dialog

importlib.reload(dialog)
dialog.show()
```

4. (Optional) Assign this code to a custom shelf button for 1-click acces.

💡 Pro Tip: Rename the button “Atlas Matrix” and assign the same icon (atlas_matrix_parent.png) for a clean look.

---

## 🧭 Interface Overview

After launching, the main dialog of matrix parent constraint appears with one tab:

| Tool              | Description                                                                  |
|-------------------|------------------------------------------------------------------------------|
| Parent Constraint | Configure full matrix parent constraints (translate, rotate, scale, shear)   |



