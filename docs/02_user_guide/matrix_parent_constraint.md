# 🧭 User Guide  Matrix Parent Constraint

This section explains the **Matrix Parent Constraint** of **Atlas Matrix**.  
It’s designed to provide fine-grained control over matrix-based constraints directly in Maya.

---

## 🖥️ Overview

The **Matrix Parent Constraint** window lets you create parent matrix constraints with complete axis and weight control - powered by Maya’s matrix nodes.

The **Matrix Parent Constraint** tab provides:

- Maintain Offset: Keeps original transform difference between driver and driven.
- Hold State: Temporarily holds the constraint state (disabled by default).
- Enveloppe: Enables/disables the overall constraint influence.
- Axis Control: Independent toggles for Translate, Rotate, Scale, and Shear.
- Weight Sliders: Per-axis and global control for blending constraints.

### Example Usage

1. Launch Atlas Matrix (`dialog.show()`).
2. Adjust axis and weights as desired.
3. Select driver(s) then driven object in Maya.
4. Click Apply to create your parent matrix constraint.

---

## 🧩 Interface Breakdown

### 🎛️ Main Options

| Label               | Widget                      | Description                                        |
|---------------------|-----------------------------|----------------------------------------------------|
| **Maintain Offset** | `checkbox_parent_offset`    | Keeps the driven object’s original offset.         |
| **Keep Hold**       | `checkbox_parent_hold`      | Placeholder for future hold functionality.         |
| **Enveloppe**       | `checkbox_parent_enveloppe` | Enables or disables the overall constraint effect. |

---

### ⚙️ Axis Groups

Each transform type (Translate, Rotate, Scale, Shear) includes:

1. **All / X / Y / Z toggles** – Axis enablement  
2. **Weight input and slider** – Control per-axis influence

| Transform     | Checkboxes                      | Weight Field                         | Slider                                     |
|---------------|---------------------------------|--------------------------------------|--------------------------------------------|
| **Translate** | `checkbox_parent_translate_*`   | `lineedit_parent_translate_weight`   | `horizontalslider_parent_translate_weight` |
| **Rotate**    | `checkbox_parent_rotate_*`      | `lineedit_parent_rotate_weight`      | `horizontalslider_parent_rotate_weight`    |
| **Scale**     | `checkbox_parent_scale_*`       | `lineedit_parent_scale_weight`       | `horizontalslider_parent_scale_weight`     |
| **Shear**     | `checkbox_parent_shear_*`       | `lineedit_parent_scale_shear_weight` | `horizontalslider_parent_shear_weight`     |

---

### 🌐 Global Weight

| Control    | ObjectName                              | Function                                     |
|------------|-----------------------------------------|----------------------------------------------|
| Text Field | `lineedit_parent_global_weight`         | Displays and edits global constraint weight. |
| Slider     | `horizontalslider_parent_global_weight` | Adjusts all axes uniformly.                  |

---

### 🔘 Action Buttons

| Button    | ObjectName            | Description                                                     |
|-----------|-----------------------|-----------------------------------------------------------------|
| **Add**   | `button_parent_add`   | Creates a new parent matrix constraint.                         |
| **Apply** | `button_parent_apply` | Creates a new parent matrix constraint and close the dialog     |
| **Close** | `button_parent_close` | Closes the dialog.                                              |

---

## 🧠 Functional Behavior

- **“All” Toggle:** Locks or unlocks individual X/Y/Z controls.  
- **Weights:** Float values between `0.000` and `1.000`, editable via text or slider.  
- **Maintain Offset:** Generates a transform offset matrix node.  
- **Hold:** (Disabled in v1.0.0, reserved for future release.)  
- **Global Weight:** Multiplies all axis weights for unified constraint blending.


