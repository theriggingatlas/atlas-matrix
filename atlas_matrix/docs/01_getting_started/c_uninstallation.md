# ⚙️ Uninstallation - Atlas Matrix 1.0.0 - Maya

This section explains how to install **Atlas Matrix**.

---
### 🧩 Automatic Setup (Recommended) 

1. **Go to** the `atlas_matrix` folder on your computer (e.g., `D:/tools/atlas_matrix/`)
2. **Open Maya** (2020+)
3. **Drag and drop** the file `atlas_matrix/uninstall.py` directly into your Maya viewport
4. **Restart Maya** to valid the userSetup installation
5. **Click Yes** on the userSetup pop-up

✅ *That's it! Atlas Matrix should be uninstalled.*

> **Note:** The tool stays in its original location. The installer only remove it from Maya's Python path.

---

### 🪛 Manual Setup

1.  - **Option A** : Delete the entire `atlas_matrix/` folder into your Maya scripts directory
    - **Option B** : Remove related **Atlas Matrix** lines from userSetup.py and userSetup.mel files: 
         
        - **Windows**: `Documents\maya\<version>\scripts\`
        - **macOS**: `~/Library/Preferences/Autodesk/maya/<version>/scripts/`
        - **Linux**: `~/maya/<version>/scripts/`

    

2. **Delete icons folder** (atlas_matrix_icons): `Documents/maya/<version>/prefs/icons/`
3. **Delete shelf** (shelf_AtlasMatrix.mel): `Documents/maya/<version>/prefs/shelves/`
4. **Restart Maya**

✅ *That's it! Atlas Matrix should be uninstalled.*

