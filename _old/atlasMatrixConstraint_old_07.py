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

from matrix_parent_con_ui import Ui_atlas_matrix_parent

PLUGIN_NAME = "atlasMatrixConstraint"
PLUGIN_VERSION = "1.4.0"
K_CMD = "atlasMatrixConstraint"

# Définition des items (clé, label, icône fallback Maya)
ITEMS = [
    ("parent",  "Parent",  "parentConstraint.png"),
    ("aim",     "Aim",     "aimConstraint.png"),
    ("manager", "Manager", "out_container.png"),
]

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
    """
    Exécute l'action Parent.
    opts = {"message": "Hello world" | "Bonjour France"}
    """
    msg = opts.get("message", "Hello world")
    om.MGlobal.displayInfo(f"[Parent] {msg}")
    print(f"[Parent] {msg}")

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



# --- Parent / Aim / Manager Option UIs (native) ------------------------------

def options_ui_parent(key, label):
    """Hello/Bonjour in Maya's native Option Box."""
    defaults = {"message": "Hello world"}
    opts = _get_options(key, defaults)

    def build_controls():
        cmds.columnLayout(adj=True, rs=8, cw=260)
        rb = cmds.radioButtonGrp(
            numberOfRadioButtons=2,
            label="Message :",
            labelArray2=["Hello world", "Bonjour France"],
            sl=1 if opts["message"] == "Hello world" else 2
        )
        def collect():
            return {
                "message": "Hello world" if cmds.radioButtonGrp(rb, q=True, sl=True) == 1
                else "Bonjour France"
            }
        def reset_ui():
            cmds.radioButtonGrp(rb, e=True,
                                sl=1 if defaults["message"] == "Hello world" else 2)
        return {"collect": collect, "reset_ui": reset_ui}

    def on_apply(values):
        _set_options(key, values)
        ACTIONS[key](values)  # run the action, like native tools do on Apply

    def on_reset(ui):
        _set_options(key, dict(defaults))
        ui["reset_ui"]()

    _open_native_option_box(f"{label} Options", build_controls, on_apply, on_reset)


def options_ui_aim(key, label):
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

    _open_native_option_box(f"{label} Options", build_controls, on_apply, on_reset)


def options_ui_manager(key, label):
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

    _open_native_option_box(f"{label} Options", build_controls, on_apply, on_reset)


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
            "parent":  {"message": "Hello world"},
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
        defaults = {"message": "Hello world"}
        ACTIONS["parent"](_get_options("parent", defaults))

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
