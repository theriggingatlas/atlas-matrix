# Atlas Matrix – Open Source Maya Constraint Tool

**Author**: Clement Daures
**Company**: The Rigging Atlas
**Website**: theriggingatlas.com
**Version**: 1.0.0  
**Compatible with**: Autodesk Maya 2025+ (PySide6)
**State**: Still in development

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
atlas_matrix_tool/
├── atlas_matrix_ui.py         # Auto-generated UI (compiled from .ui file via pyside6-uic)
├── atlas_matrix_window.py     # Main QMainWindow logic & UI integration
├── atlas_matrix_launcher.py   # Clean entry point for Maya integration
```

---

## 🚀 Installation

1. Copy the `atlas-matrix/` folder to your Maya scripts directory (e.g. `~/Documents/maya/scripts/`).
2. In Maya’s Script Editor, paste the following Python code:

```python
import sys
import os

# Add the path to your tool (adjust if needed)
tool_path = os.path.expanduser("~/Documents/maya/scripts/atlas-matrix")
if tool_path not in sys.path:
    sys.path.append(tool_path)

# Reload and launch
import launcher
import importlib
importlib.reload(launcher)

launcher.launch()
```

💡 **Pro Tip**: Assign this code to a custom Maya shelf button for quick access!

---

## 🖥️ Features

### ✅ Parent Constraint Tab
- Maintain offset
- Hold state toggle
- Axis control (Translate, Rotate, Scale)
- Axis weight sliders (LineEdit + Slider linked)
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

| Maya Version | Qt Version    | Compatible  |
|--------------|---------------|-------------|
| 2025+        | PySide6 / Qt6 | ✅ Yes       |
| 2020 - 2024  | PySide2 / Qt5 | ✅ Yes       |

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

--

## TO DO

add constraint remover
add initialTransform attribute creation
add initialMatrix attribute creation