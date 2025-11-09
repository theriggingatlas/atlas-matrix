# 🧭 User Guide  Matrix Remove Constraint

This section explains the **Matrix Remove Constraint** of **Atlas Matrix**.

---

## 🖥️ Overview

The **Matrix Parent Constraint** lets you remove matrix constraints.

### Example Usage

1. Select driven object you want to remove the constraint from.
2. Click on your shelf button or run ``from atlas_matrix.core.remove_con import remove_constraint; remove_constraint()`` in your python shell.

---

## 🧠 Functional Behavior

- **Node Cleaning:** Delete all matrix constraint related node on the selected constrained object.  
- **Attribute Cleaning:** Delete all matrix constraint related attribute on the selected constrained object.  
- **Previous Transform:** Restore previous transform of the selected constrained object.  
- **Previous Matrix Offset Parent Matrix:** Restore previous offset parent matrix of the selected constrained object.

---

## 💡 Pro tips

Use Atlas Matrix Remove Constraint from Maya's Script Editor:
```python
from atlas_matrix.core.remove_con import remove_constraint
remove_constraint()
```

 For development (with auto-reload):
```python
import importlib
from atlas_matrix.core.remove_con import remove_constraint
importlib.reload(remove_constraint)
remove_constraint()
```
