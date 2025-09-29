# -*- coding: utf-8 -*-
# Constrain > Matrix Constraints
#   Parent   [□]   (icon)
#   Aim      [□]   (icon)
#   Manager  [□]   (icon)

from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import os

PLUGIN_NAME = "atlasMatrixConstraint"
PLUGIN_VERSION = "1.3.0"
K_CMD = "atlasMatrixConstraint"

# Définition des items (clé interne, label, icône par défaut côté Maya)
ITEMS = [
    ("parent",  "Parent",  "parentConstraint.png"),
    ("aim",     "Aim",     "aimConstraint.png"),
    ("manager", "Manager", "out_container.png"),  # remplace par l'icône que tu veux
]

_ORIGINAL_PMC = None
_MENU_NAME = None

# ---------- helpers ----------

def _ids(key):
    return {
        "item": f"atlasMC_{key}Item",
        "opt":  f"atlasMC_{key}Option",
        "win":  f"atlasMC_{key}OptionsWin",
        "ov":   f"atlasMC_{key}_lastChoice",
    }

def _ensure_optionvar(key):
    ov = _ids(key)["ov"]
    if not cmds.optionVar(exists=ov):
        cmds.optionVar(iv=(ov, 1))

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

# --- icônes ---

def _plugin_icons_dir():
    # <...>/plug-ins/icons
    try:
        return os.path.join(os.path.dirname(__file__), "icons")
    except Exception:
        return None

def _icon_for(key, maya_fallback):
    """
    Renvoie le chemin de l'icône à utiliser :
    1) si un fichier existe dans <plugin>/icons pour cette clé (ex: parent.png/aim.png/manager.png)
    2) sinon, on renvoie l'icône native de Maya (maya_fallback)
    """
    icons_dir = _plugin_icons_dir()
    if icons_dir and os.path.isdir(icons_dir):
        # essaie quelques noms usuels
        for name in (f"{key}.png", f"{key}.xpm", f"{key}.svg"):
            p = os.path.join(icons_dir, name)
            if os.path.exists(p):
                return p
    return maya_fallback  # Maya cherchera dans XBMLANGPATH

# ---------- actions ----------

def _run_action(key):
    _ensure_optionvar(key)
    ov = _ids(key)["ov"]
    val = int(cmds.optionVar(q=ov))
    if val == 2:
        om.MGlobal.displayInfo("Bonjour France")
        print("Bonjour France")
    else:
        om.MGlobal.displayInfo("Hello world")
        print("Hello world")

def _show_options(key, label):
    _ensure_optionvar(key)
    i = _ids(key)
    if cmds.window(i["win"], exists=True):
        cmds.deleteUI(i["win"])
    win = cmds.window(i["win"], title=f"{label} Options", sizeable=False)
    cmds.columnLayout(adj=True, rs=8, cw=260)
    rb = cmds.radioButtonGrp(
        numberOfRadioButtons=2,
        label="Action :",
        labelArray2=["Hello world", "Bonjour France"],
        sl=int(cmds.optionVar(q=i["ov"]))
    )
    def _apply(*_):
        cmds.optionVar(iv=(i["ov"], cmds.radioButtonGrp(rb, q=True, sl=True)))
    cmds.button(label="Apply and Close", c=lambda *_: (_apply(), cmds.deleteUI(win)))
    cmds.button(label="Apply", c=_apply)
    cmds.button(label="Close", c=lambda *_: cmds.deleteUI(win))
    cmds.showWindow(win)

# ---------- insertion menu ----------

def _insert_items(menu_name):
    _delete_ui()

    insert_after = _find_matrix_constraints_divider(menu_name)
    if not insert_after:
        ia = cmds.menu(menu_name, q=True, ia=True) or []
        insert_after = ia[-1] if ia else None

    previous = insert_after
    for key, label, maya_icon in ITEMS:
        ids = _ids(key)
        _ensure_optionvar(key)
        icon = _icon_for(key, maya_icon)

        kwargs = dict(parent=menu_name, label=label, image=icon)
        if previous:
            kwargs["insertAfter"] = previous

        cmds.menuItem(ids["item"], **kwargs, c=(lambda k=key: _run_action(k)))
        cmds.menuItem(
            ids["opt"],
            parent=menu_name,
            optionBox=True,
            insertAfter=ids["item"],
            c=(lambda k=key, l=label: _show_options(k, l))
        )
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

# ---------- MPx command ----------

class AtlasMatrixConstraintCmd(ompx.MPxCommand):
    def doIt(self, args):
        _run_action("parent")

def _cmd_creator():
    return ompx.asMPxPtr(AtlasMatrixConstraintCmd())

# ---------- plugin entry points ----------

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
