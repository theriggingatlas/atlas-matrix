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

1. Open Maya (2025+).
2. Drag and drop the file `atlas_matrix/setup/install.py` directly into your Maya viewport.
3. Restart Maya.
4. You’ll now see a new shelf named **AtlasMatrix** in your Maya shelf bar.

✅ *That’s it! You’re ready to use Atlas Matrix.*

FOR MANUAL INSTALLATION, PLEASE REFER TO `docs/01_getting_started/quick_start.md`

---

## 🖥️ Features

### ✅ Matrix Parent Constraint
- Maintain offset
- Hold state toggle
- Axis control (Translate, Rotate, Scale)
- Axis weight sliders (LineEdit + Slider linked)
- Axis selection control (X, Y, Z)

### 🚧 Matrix Aim Constraint
- Aim & Up vector configuration
- Target vectors with XYZ inputs
- World up type selection
- Hold and offset toggles

### ✅ Matrix Constraint Remover
- Delete constraint on selected object

### 🚧 Matrix Constraint Manager
- Placeholder for future constraint management tools

---

## 🛠️ How to use

- Refer to `docs/02_user_guide/`

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

## 📃 License

This tool is distributed as-is for non-commercial use.  
For commercial licensing or contributions, please contact the author directly.
