# Documentation : Atlas Parent Matrix Tool

## 📖 Overview
The **Atlas Parent Matrix Tool** provides a **matrix-based parent constraint** implementation that replicates Maya’s native parent constraint using matrix operations.  

This approach offers:
- Greater flexibility  
- Compatibility with matrix-driven workflows  
- Non-destructive, scalable rigging setups
- Lighter usage than native constraint on large amount of constraint

---

## 🚀 How to use ?

Atlas Matrix Parent handle two way of use :

1. **Shelf and code framework management**
2. **With the plugin version**  

Before all, copy the icons in ```atlas-matrix/icons``` into ```~/Documents/maya/prefs/icons/atlas-matrix```

### Shelf and code usage :

1. **Copy the atlas-matrix folder into the following path : ```~/Documents/maya/scripts/atlas-matrix```**
2. **Open maya**

3. **Then you have two options :** 

Firstly :
- Drag and drop the install.py file into your viewport. A shelf should be created including Atlas Parent Matrix, Atlas Aim Matrix and Atlas Matrix Manager Tool

or, as a secondary option :

- Copy / Paste the code below

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

4. **Great ! Atlas Parent Matrix is now open !** 

### Plugin version usage :

1. **Copy the atlas-matrix folder into the following path : ```~/Documents/maya/scripts/atlas-matrix```**
2. **Open maya**
3. **Open your plugin manager**
4. **Browse and in the following path : ```~/Documents/maya/scripts/atlas-matrix/ui/plugin```, select atlasMatrixConstraint**
5. **Enjoy your plugin into the Constrain menu**

---

## ⚙️ Operation Information
The constraint logic is handled through a **`multMatrix` node** with this structure:

- **Input 1:** Offset matrix (identity if no offset specified)  
- **Input 2:** Driver world matrix  
- **Input 3:** Driven object’s inverse matrix  

---

## 🌟 Features

### Blend System
- Automatically sets up **blending** when:
  - The **Envelope option** is checked  
  - Multiple driver objects are selected  
- Creates `W{index}` attributes on the driven object for weight control  
- Supports **multiple drivers with independent weights**  

### Offset Handling
- Always reserves a free input slot for **offset matrices**  
- Works with both enabled and disabled offset options  
- Uses **identity matrix** if offset is disabled  

### Constraint Order
Operations are applied in the following order:
1. Offset matrix application  
2. World matrix transformation  
3. Inverse matrix calculation  

---

## 🔧 Technical Implementation

### Matrix Connection Flow
[Driver World Matrix] → [multMatrix] → [Driven offsetParentMatrix]
↑
[Offset Matrix] (optional)
↑
[Inverse Matrix] (calculated)


### Pre-existing Connections Handling
- Detects already connected `offsetParentMatrix`  
- Creates a **new matrix attribute** to store pre-constraint offset values  
- Preserves **existing transformations** while applying new constraints  

---

## 💡 Advantages Over Classic Constraints

### Benefits
- **Matrix-Based** → integrates seamlessly with matrix-driven systems  
- **Non-Destructive** → preserves transformations & connections  
- **Flexible** → supports custom offset preservation  
- **Scalable** → extendable for complex setups  

### Compatibility
- Matches behavior of Maya’s native parent constraints  
- Works alongside other constraint systems  
- Fully compatible with standard Maya deformation workflows  

---

## 🧩 Example Use Cases
- **Complex Rigging Systems** → advanced character rigs with matrix controls  
- **Animation Overrides** → keep offsets while constraining  
- **Modular Rigging** → reusable, lightweight constraint components  
- **Pipeline Tools** → consistent constraint behavior across assets  

---

## 📝 Notes
- Requires **at least one driver object**  
- Driven object must be **selected last**  
- Works with **single or multiple drivers**  
- Maintains **transformation offsets** via matrix operations  
