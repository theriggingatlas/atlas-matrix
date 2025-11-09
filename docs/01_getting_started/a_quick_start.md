# 🚀 Quick Start - Atlas Matrix 1.0.0 - Maya

Welcome to **Atlas Matrix**, the open-source Maya matrix constraint tool designed for artists and riggers who want full control with a clean, PySide6-based interface.

---

## ⚙️ Installation

### 🧩 Automatic Setup (Recommended) 

1. **Download** or clone the `atlas_matrix` folder to any location on your computer (e.g., `D:/tools/atlas_matrix/`)
2. **Open Maya** (2020+)
3. **Drag and drop** the file `atlas_matrix/setup/install.py` directly into your Maya viewport
4. **Restart Maya** to valid the userSetup installation
5. **Click Yes** on the userSetup pop-up 
6. You'll now see a new shelf named **AtlasMatrix** in your Maya shelf bar

✅ *That's it! You're ready to use Atlas Matrix.*

> **Note:** The tool stays in its original location. The installer only adds it to Maya's Python path.

---

### 🪛 Manual Setup

1. **Copy** the entire `atlas_matrix/` folder into your Maya scripts directory:

    - **Windows**: `Documents\maya\<version>\scripts\`
    - **macOS**: `~/Library/Preferences/Autodesk/maya/<version>/scripts/`
    - **Linux**: `~/maya/<version>/scripts/`

2. **Copy icons folder** (atlas_matrix_icons): `atlas_matrix/setup/icons/` → `Documents/maya/<version>/prefs/icons/`
3. **Copy shelf** (shelf_AtlasMatrix.mel): `atlas_matrix/setup/shelves/` → `Documents/maya/<version>/prefs/shelves/`
4. **Restart Maya**
5. You'll now see the **AtlasMatrix** shelf in your Maya shelf bar

✅ *That's it! You're ready to use Atlas Matrix.*

---

### 💡 Pro tips

Launch Atlas Matrix Parent Constraint from Maya's Script Editor:
```python
from atlas_matrix.ui.parent_con import dialog
dialog.show()
```

 For development (with auto-reload):
```python
import importlib
from atlas_matrix.ui.parent_con import dialog
importlib.reload(dialog)
dialog.show()
```

---

## 🧭 Interface Overview

After launching, the main dialog of matrix parent constraint appears with one window:

| Tool              | Description                                                                  |
|-------------------|------------------------------------------------------------------------------|
| Parent Constraint | Configure full matrix parent constraints (translate, rotate, scale, shear)   |



