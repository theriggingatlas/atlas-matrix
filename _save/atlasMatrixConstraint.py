# -*- coding: utf-8 -*-
# Constrain > Matrix Constraints
#   Parent   [□] -> action + options propres
#   Aim      [□] -> action + options propres
#   Manager  [□] -> action + options propres

from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import os, json
import maya.OpenMayaUI as omui
try:
    from PySide6 import QtWidgets, QtCore   # Maya 2025+
    from shiboken6 import wrapInstance
except Exception:
    from PySide2 import QtWidgets, QtCore   # Maya 2024 or earlier
    from shiboken2 import wrapInstance

from matrix_parent_con_ui import AtlasMatrixParentUi

PLUGIN_NAME = "atlasMatrixConstraint"
PLUGIN_VERSION = "1.4.0"
K_CMD = "atlasMatrixConstraint"

# Définition des items (clé, label, icon, window_title fallback Maya)
ITEMS = [
    ("parent",  "Parent",  "parentConstraint.png", "Matrix Parent Constraint"),
    ("aim",     "Aim",     "aimConstraint.png", "Matrix Aim Constraint"),
    ("manager", "Manager", "out_container.png", "Matrix Manager"),
]

_PARENT_DEFAULTS = {
    "offset": False, "hold": False, "envelope": True,
    "t":  {"all": True, "x": True, "y": True, "z": True, "w": 0.5},
    "r":  {"all": True, "x": True, "y": True, "z": True, "w": 0.5},
    "s":  {"all": True, "x": True, "y": True, "z": True, "w": 0.5},
    "sh": {"all": True, "x": True, "y": True, "z": True, "w": 0.5},
}
_current_parent_panel = {"w": None}


_ORIGINAL_PMC = None
_MENU_NAME = None

# ----------------- helpers génériques -----------------

def _ids(key):
    return {
        "item": f"atlasMC_{key}Item",
        "opt":  f"atlasMC_{key}Option",
        "win":  f"atlasMC_{key}OptionsWin",
        "ov":   f"atlasMC_{key}_optsJSON",   # optionVar (JSON)
    }

def _ensure_options(key, defaults):
    """Crée l'optionVar JSON avec les valeurs par défaut si nécessaire."""
    ov = _ids(key)["ov"]
    if not cmds.optionVar(exists=ov):
        cmds.optionVar(sv=(ov, json.dumps(defaults)))

def _get_options(key, defaults):
    ov = _ids(key)["ov"]
    _ensure_options(key, defaults)
    try:
        return json.loads(cmds.optionVar(q=ov))
    except Exception:
        cmds.optionVar(sv=(ov, json.dumps(defaults)))
        return dict(defaults)

def _set_options(key, data):
    ov = _ids(key)["ov"]
    cmds.optionVar(sv=(ov, json.dumps(data)))

def _find_constrain_menu():
    try:
        menus = cmds.window('MayaWindow', q=True, menuArray=True) or []
        for m in menus:
            lbl = (cmds.menu(m, q=True, label=True) or "").strip().lower()
            if lbl in ("constrain", "constraints", "contraindre"):
                return m
    except Exception:
        pass
    return None

def _find_matrix_constraints_divider(menu_name):
    for it in (cmds.menu(menu_name, q=True, ia=True) or []):
        if cmds.menuItem(it, q=True, exists=True) and cmds.menuItem(it, q=True, divider=True):
            lbl = (cmds.menuItem(it, q=True, label=True) or "").strip().lower()
            if lbl == "matrix constraints":
                return it
    return None

def _delete_ui():
    for key, _, _ in ITEMS:
        i = _ids(key)
        for mid in (i["item"], i["opt"]):
            if cmds.menuItem(mid, exists=True):
                cmds.deleteUI(mid)
        if cmds.window(i["win"], exists=True):
            cmds.deleteUI(i["win"])

def _plugin_icons_dir():
    try:
        icon_path = "/home/clementdaures/maya/2025/prefs"
        #return os.path.join(os.path.dirname(__file__), "icons")
        return os.path.join(icon_path, "icons")
    except Exception:
        return None

def _icon_for(key, maya_fallback):
    icons_dir = _plugin_icons_dir()
    if icons_dir and os.path.isdir(icons_dir):
        for name in (f"{key}.png", f"{key}.xpm", f"{key}.svg"):
            p = os.path.join(icons_dir, name)
            if os.path.exists(p):
                return p
    return maya_fallback

# ----------------- ACTIONS SPÉCIFIQUES -----------------
# Remplace l'intérieur de ces fonctions par ta logique réelle (contraintes, etc.)

def action_parent(opts):
    # Example: just log a few values for now
    t_w = ((opts.get("t") or {}).get("w", 0.5))
    env = opts.get("envelope", True)
    off = opts.get("offset", False)
    om.MGlobal.displayInfo(f"[Parent] offset={off} envelope={env} translateWeight={t_w:.3f}")


def action_aim(opts):
    """
    Exécute l'action Aim.
    opts = {"axis": "X"|"Y"|"Z"}
    """
    axis = opts.get("axis", "X")
    om.MGlobal.displayInfo(f"[Aim] Target axis = {axis}")
    print(f"[Aim] Target axis = {axis}")

def action_manager(opts):
    """
    Exécute l'action Manager.
    opts = {"mode": "log"|"window", "name": "<str>"}
    """
    mode = opts.get("mode", "log")
    name = opts.get("name", "Atlas")
    if mode == "window":
        win = "atlasMC_managerRunWin"
        if cmds.window(win, exists=True):
            cmds.deleteUI(win)
        w = cmds.window(win, title=f"Manager: {name}", sizeable=False)
        cmds.columnLayout(adj=True, rs=6, cw=260)
        cmds.text(l=f"Manager Panel for: {name}")
        cmds.button(l="OK", c=lambda *_: cmds.deleteUI(w))
        cmds.showWindow(w)
    else:
        om.MGlobal.displayInfo(f"[Manager] Running for {name}")
        print(f"[Manager] Running for {name}")

# Map clé -> fonction d'action
ACTIONS = {
    "parent":  action_parent,
    "aim":     action_aim,
    "manager": action_manager,
}

# ----------------- OPTIONS UI SPÉCIFIQUES -----------------

# --- Native Option Box helpers ----------------------------------------------

def _ui_available():
    """Return True if a GUI is available (not batch, Maya main window exists)."""
    try:
        if cmds.about(batch=True):
            return False
        return cmds.control('MayaWindow', q=True, exists=True)
    except Exception:
        return False

def _get_option_box_parent_widget():
    mel.eval('source "getOptionBox.mel";')
    try:
        layout_name = mel.eval('getOptionBox()')
    except Exception:
        mel.eval('showOptionBox; hideOptionBox;')
        layout_name = mel.eval('getOptionBox()')

    ptr = omui.MQtUtil.findLayout(layout_name)
    if not ptr:
        om.MGlobal.displayWarning("Option Box layout not found.")
        return None

    host = wrapInstance(int(ptr), QtWidgets.QWidget)
    lay = host.layout()
    if lay is None:
        lay = QtWidgets.QVBoxLayout(host)
        lay.setContentsMargins(6, 6, 6, 6)
    else:
        # clear children (widgets / sub-layouts / spacers)
        def _clear(l):
            while l.count():
                it = l.takeAt(0)
                w = it.widget()
                if w:
                    w.setParent(None)
                sub = it.layout()
                if sub:
                    _clear(sub)
                # spacerItem() drops automatically
        _clear(lay)
    return host



def _open_option_box_with_qt(title, make_widget_fn, on_apply, on_reset):
    if not _ui_available():
        om.MGlobal.displayWarning("No UI available; cannot open Option Box.")
        return

    host = _get_option_box_parent_widget()
    if host is None:
        return

    mel.eval('setOptionBoxTitle("{0}");'.format(title.replace('"', '\\"')))

    widget = make_widget_fn(host)            # parent your widget to host
    host.layout().addWidget(widget)

    cmds.button(mel.eval('getOptionBoxApplyBtn()'), e=True, c=lambda *_: on_apply())
    cmds.button(mel.eval('getOptionBoxApplyAndCloseBtn()'), e=True,
                c=lambda *_: (on_apply(), mel.eval('hideOptionBox;')))
    cmds.button(mel.eval('getOptionBoxResetBtn()'), e=True, c=lambda *_: on_reset())
    mel.eval('showOptionBox;')


def _open_native_option_box(title, build_controls, on_apply, on_reset):
    # If no UI (batch/headless), just bail gracefully.
    if not _ui_available():
        om.MGlobal.displayWarning("No UI available; cannot open Option Box.")
        return

    # Ensure the MEL helpers are available
    try:
        mel.eval('source "getOptionBox.mel";')
    except Exception:
        pass

    # Ensure the Option Box exists before querying it
    try:
        parent_layout = mel.eval('getOptionBox()')
    except Exception:
        mel.eval('showOptionBox; hideOptionBox;')
        parent_layout = mel.eval('getOptionBox()')

    # Title & parenting
    mel.eval('setOptionBoxTitle("{0}");'.format(title.replace('"', '\\"')))
    cmds.setParent(parent_layout)

    # Clear any previous UI in the Option Box body
    try:
        children = cmds.layout(parent_layout, q=True, ca=True) or []
        for ch in children:
            if cmds.control(ch, exists=True):
                cmds.deleteUI(ch)
    except Exception:
        pass

    # Build your controls and accessors
    ui = build_controls()  # -> {'collect': fn, 'reset_ui': fn}

    # Wire native buttons
    apply_btn = mel.eval('getOptionBoxApplyBtn()')
    cmds.button(apply_btn, e=True, label="Apply",
                c=lambda *_: on_apply(ui["collect"]()))

    apply_close_btn = mel.eval('getOptionBoxApplyAndCloseBtn()')
    cmds.button(apply_close_btn, e=True, label="Apply and Close",
                c=lambda *_: (on_apply(ui["collect"]()), mel.eval('hideOptionBox;')))

    reset_btn = mel.eval('getOptionBoxResetBtn()')
    cmds.button(reset_btn, e=True, c=lambda *_: on_reset(ui))

    # Show the native Option Box
    mel.eval('showOptionBox;')

def _fnum(text, default=0.5):
    try:
        return float(text.replace(',', '.'))
    except Exception:
        return default

class ParentPanel(QtWidgets.QWidget):
    """Wraps AtlasMatrixParentUi and provides collect/set_from_opts."""
    def __init__(self, parent=None, opts=None):
        super(ParentPanel, self).__init__(parent)
        self.ui = AtlasMatrixParentUi()
        self.ui.setupUi(self)
        self._wire_logic()
        if opts:
            self.set_from_opts(opts)

    def _wire_logic(self):
        u = self.ui
        # “All” toggles gate individual axis widgets and keep them checked
        for prefix in ("translate", "rotate", "scale"):
            all_cb = getattr(u, f"checkbox_parent_{prefix}_all")
            for axis in "xyz":
                axis_cb = getattr(u, f"checkbox_parent_{prefix}_{axis}")
                all_cb.toggled.connect(axis_cb.setDisabled)
                all_cb.toggled.connect(axis_cb.setChecked)
        u.checkbox_parent_offset.toggled.connect(u.checkbox_parent_hold.setEnabled)
        u.checkbox_parent_offset.toggled.connect(u.checkbox_parent_hold.setChecked)

    def collect(self):
        u = self.ui
        return {
            "offset":   bool(u.checkbox_parent_offset.isChecked()),
            "hold":     bool(u.checkbox_parent_hold.isChecked()),
            "envelope": bool(u.checkbox_parent_enveloppe.isChecked()),
            "t":  {"all": u.checkbox_parent_translate_all.isChecked(),
                   "x": u.checkbox_parent_translate_x.isChecked(),
                   "y": u.checkbox_parent_translate_y.isChecked(),
                   "z": u.checkbox_parent_translate_z.isChecked(),
                   "w": _fnum(u.lineedit_parent_translate_weight.text(), 0.5)},
            "r":  {"all": u.checkbox_parent_rotate_all.isChecked(),
                   "x": u.checkbox_parent_rotate_x.isChecked(),
                   "y": u.checkbox_parent_rotate_y.isChecked(),
                   "z": u.checkbox_parent_rotate_z.isChecked(),
                   "w": _fnum(u.lineedit_parent_rotate_weight.text(), 0.5)},
            "s":  {"all": u.checkbox_parent_scale_all.isChecked(),
                   "x": u.checkbox_parent_scale_x.isChecked(),
                   "y": u.checkbox_parent_scale_y.isChecked(),
                   "z": u.checkbox_parent_scale_z.isChecked(),
                   "w": _fnum(u.lineedit_parent_scale_weight.text(), 0.5)},
            "sh": {"all": u.checkbox_parent_shear_all.isChecked(),
                   "x": u.checkbox_parent_shear_x.isChecked(),
                   "y": u.checkbox_parent_shear_y.isChecked(),
                   "z": u.checkbox_parent_shear_z.isChecked(),
                   "w": _fnum(u.lineedit_parent_scale_shear_weight.text(), 0.5)},
        }

    def set_from_opts(self, o):
        u = self.ui
        u.checkbox_parent_offset.setChecked(o.get("offset", False))
        u.checkbox_parent_hold.setChecked(o.get("hold", False))
        u.checkbox_parent_enveloppe.setChecked(o.get("envelope", True))

        def apply_axis(group, prefix, line_name):
            g = o.get(group, {})
            getattr(u, f"checkbox_parent_{prefix}_all").setChecked(g.get("all", True))
            getattr(u, f"checkbox_parent_{prefix}_x").setChecked(g.get("x", True))
            getattr(u, f"checkbox_parent_{prefix}_y").setChecked(g.get("y", True))
            getattr(u, f"checkbox_parent_{prefix}_z").setChecked(g.get("z", True))
            getattr(u, line_name).setText("{:.3f}".format(float(g.get("w", 0.5))))
        apply_axis("t", "translate", "lineedit_parent_translate_weight")
        apply_axis("r", "rotate",    "lineedit_parent_rotate_weight")
        apply_axis("s", "scale",     "lineedit_parent_scale_weight")
        apply_axis("sh","shear",     "lineedit_parent_scale_shear_weight")


# --- Parent / Aim / Manager Option UIs (native) ------------------------------

def options_ui_parent(key, window_title):
    opts = _get_options(key, _PARENT_DEFAULTS)

    def make_widget(parent):
        w = ParentPanel(parent=parent, opts=opts)
        _current_parent_panel["w"] = w
        return w

    def on_apply():
        w = _current_parent_panel["w"]
        if not w:
            return
        new_opts = w.collect()
        _set_options(key, new_opts)
        ACTIONS[key](new_opts)  # run your tool with these values

    def on_reset():
        w = _current_parent_panel["w"]
        if not w:
            return
        _set_options(key, dict(_PARENT_DEFAULTS))
        w.set_from_opts(_PARENT_DEFAULTS)

    _open_option_box_with_qt(f"{window_title} Options", make_widget, on_apply, on_reset)



def options_ui_aim(key, window_title):
    """Axis chooser in Maya's native Option Box."""
    defaults = {"axis": "X"}
    opts = _get_options(key, defaults)

    def build_controls():
        cmds.columnLayout(adj=True, rs=8, cw=260)
        omenu = cmds.optionMenu(label="Target Axis :")
        for a in ("X", "Y", "Z"):
            cmds.menuItem(l=a)
        cmds.optionMenu(omenu, e=True, v=opts["axis"])

        def collect():
            return {"axis": cmds.optionMenu(omenu, q=True, v=True)}

        def reset_ui():
            cmds.optionMenu(omenu, e=True, v=defaults["axis"])

        return {"collect": collect, "reset_ui": reset_ui}

    def on_apply(values):
        _set_options(key, values)
        ACTIONS[key](values)

    def on_reset(ui):
        _set_options(key, dict(defaults))
        ui["reset_ui"]()

    _open_native_option_box(f"{window_title} Options", build_controls, on_apply, on_reset)


def options_ui_manager(key, window_title):
    """Mode + name in Maya's native Option Box."""
    defaults = {"mode": "log", "name": "Atlas"}
    opts = _get_options(key, defaults)

    def build_controls():
        cmds.columnLayout(adj=True, rs=8, cw=280)
        omode = cmds.optionMenu(label="Mode :")
        for m in ("log", "window"):
            cmds.menuItem(l=m)
        cmds.optionMenu(omode, e=True, v=opts["mode"])
        t = cmds.textFieldGrp(label="Name :", text=opts["name"])

        def collect():
            return {
                "mode": cmds.optionMenu(omode, q=True, v=True),
                "name": cmds.textFieldGrp(t, q=True, text=True)
            }

        def reset_ui():
            cmds.optionMenu(omode, e=True, v=defaults["mode"])
            cmds.textFieldGrp(t, e=True, text=defaults["name"])

        return {"collect": collect, "reset_ui": reset_ui}

    def on_apply(values):
        _set_options(key, values)
        ACTIONS[key](values)

    def on_reset(ui):
        _set_options(key, dict(defaults))
        ui["reset_ui"]()

    _open_native_option_box(f"{window_title} Options", build_controls, on_apply, on_reset)


# Map clé -> constructeur de fenêtre d’options
OPTIONS_UI = {
    "parent":  options_ui_parent,
    "aim":     options_ui_aim,
    "manager": options_ui_manager,
}

# ----------------- insertion menu (avec icônes) -----------------

def _insert_items(menu_name):
    _delete_ui()

    insert_after = _find_matrix_constraints_divider(menu_name)
    if not insert_after:
        ia = cmds.menu(menu_name, q=True, ia=True) or []
        insert_after = ia[-1] if ia else None

    previous = insert_after
    for key, label, maya_icon in ITEMS:
        ids = _ids(key)
        icon = _icon_for(key, maya_icon)
        defaults = {
            "parent":  _PARENT_DEFAULTS,
            "aim":     {"axis": "X"},
            "manager": {"mode": "log", "name": "Atlas"},
        }[key]
        _ensure_options(key, defaults)

        kwargs = dict(parent=menu_name, label=label, image=icon)
        if previous:
            kwargs["insertAfter"] = previous

        # Action spécifique
        cmds.menuItem(ids["item"], **kwargs, c=(lambda *_, k=key, d=defaults: ACTIONS[k](_get_options(k, d))))
        # Option box spécifique
        cmds.menuItem(ids["opt"], parent=menu_name, optionBox=True, insertAfter=ids["item"],
                      c=(lambda *_, k=key, l=label: OPTIONS_UI[k](k, l)))
        previous = ids["opt"]

def _pmc_wrapper(*_):
    try:
        if isinstance(_ORIGINAL_PMC, str) and _ORIGINAL_PMC.strip():
            mel.eval(_ORIGINAL_PMC)
        elif callable(_ORIGINAL_PMC):
            _ORIGINAL_PMC()
    except Exception:
        pass
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        _insert_items(_MENU_NAME)

def _attach_to_constrain_menu():
    global _ORIGINAL_PMC, _MENU_NAME
    _MENU_NAME = _find_constrain_menu()
    if not _MENU_NAME:
        cmds.evalDeferred(_attach_to_constrain_menu, lp=True)
        return
    try:
        _ORIGINAL_PMC = cmds.menu(_MENU_NAME, q=True, pmc=True)
    except Exception:
        _ORIGINAL_PMC = None
    cmds.menu(_MENU_NAME, e=True, postMenuCommandOnce=False, pmc=_pmc_wrapper)

# ----------------- MPx command -----------------

class AtlasMatrixConstraintCmd(ompx.MPxCommand):
    def doIt(self, args):
        # Exemple : la commande déclenche l'action Parent avec ses options
        ACTIONS["parent"](_get_options("parent", _PARENT_DEFAULTS))

def _cmd_creator():
    return ompx.asMPxPtr(AtlasMatrixConstraintCmd())

# ----------------- plugin entry points -----------------

def initializePlugin(mobj):
    plugin = ompx.MFnPlugin(mobj, "atlas", PLUGIN_VERSION, "Any")
    plugin.registerCommand(K_CMD, _cmd_creator)
    cmds.evalDeferred(_attach_to_constrain_menu, lp=True)
    om.MGlobal.displayInfo("%s loaded" % PLUGIN_NAME)

def uninitializePlugin(mobj):
    _delete_ui()
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        try:
            cmds.menu(_MENU_NAME, e=True, pmc=_ORIGINAL_PMC, postMenuCommandOnce=False)
        except Exception:
            pass
    plugin = ompx.MFnPlugin(mobj)
    plugin.deregisterCommand(K_CMD)
    om.MGlobal.displayInfo("%s unloaded" % PLUGIN_NAME)
