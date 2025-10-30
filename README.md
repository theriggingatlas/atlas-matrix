# Atlas Matrix – Open Source Maya Matrix Constraint Tool

- -*- coding: utf-8 -*-
- **Author**: Clement Daures
- **Company**: The Rigging Atlas
- **Website**: theriggingatlas.com

---

- **Version**: 1.0.0  
- **Compatible with**: Autodesk Maya 2025+ (PySide6)
- **State**: Still in development

---

## 📖 About  

**Atlas Matrix** is a powerful and user-friendly tool designed to simplify and streamline the process of creating and managing matrix-based constraints in Maya.

It features a clean, tabbed interface that supports:
- Parent constraints with fine control over axes and weights
- Aim constraints with full vector and up-vector configuration
- Manager panel (placeholder for future development)

Atlas Matrix is fully built with **PySide6** and supports Maya 2025’s native Qt6 backend. 

---

## 📁 File Structure

```
atlas_matrix/
├── core ├── matrix
         ├── parent_con
         ├── utils ├── attributes.py
                   ├── nodes.py
                   ├── transform.py
                   ├── verification.py

├── ui   ├── parent_con ├── main.py
                        ├── dialog.py
                        
├── docs ├── 01_getting_started ├── quick_start.md
         ├── 02_user_guide      ├── matrix_parent_constraint.md
         ├── 03_developer_guide ├── coding_guidelines.md
                                ├── naming_conventions.md
         ├── 04_troubleshooting ├── common_issue.md
```

---

## 🚀 Installation

**01-AUTOMATIC**

1. Drag and drop the ```install.py``` in `atlas_matrix/setup/` to your Maya viewport and restart maya
2. You should see a shelf named `AtlasMatrix` in your maya shelves

**02-MANUAL**

1. Copy the `atlas_matrix/` folder to your Maya scripts directory (e.g. `~/Documents/maya/scripts/`).
2. Copy the `atlas_matrix_parent.png` in `atlas_matrix/setup/` to your Maya icon directory (e.g `~/Documents/maya/prefs/icons/`)
3. In Maya’s Script Editor, paste the following Python code for Parent Constraint:

```python
import importlib
from atlas_matrix.ui.parent_con import dialog

importlib.reload(dialog)
dialog.show()
```

💡 **Pro Tip**: Assign this code to a custom Maya shelf button for quick access!

---

## 🖥️ Features

### ✅ Parent Constraint Tab
- Maintain offset
- Hold state toggle
- Axis control (Translate, Rotate, Scale)
- Axis weight sliders 
- Global weight slider 
- Axis selection control (X, Y, Z)

### 🚧 Aim Constraint Tab
- Aim & Up vector configuration
- Target vectors with XYZ inputs
- World up type selection
- Hold and offset toggles

### 🚧 Manager Tab
- Placeholder for future constraint management tools

---

## 💻 Development Notes

- Built using **Qt Designer** and compiled via `pyside6-uic`
- Uses `wrapInstance()` and `OpenMayaUI` for clean integration with Maya main window
- Avoids global variables through class-based singleton window handling

---

## 📌 Compatibility

| Maya Version | Qt Version    | Compatible |
|--------------|---------------|------------|
| 2025+        | PySide6 / Qt6 | ✅ Yes      |
| 2020 - 2024  | PySide2 / Qt5 | ❌ Coming   |

---

## 📬 Contact

**Author**: Clement Daures  
Email: [clementdaures.contact@gmail.com](mailto:clementdaures.contact@gmail.com)  
IG: [@theriggingatlas](https://instagram.com/theriggingatlas) or [@clementdaures](https://instagram.com/clementdaures)

---

## 🛠️ Future Plans

- Scene-wide constraint manager
- Constraint replacer

---

## 📃 License

This tool is distributed as-is for non-commercial use.  
For commercial licensing or contributions, please contact the author directly.
