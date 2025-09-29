# -*- coding: utf-8 -*-
# Plugin: atlasMatrixConstraint
# Constrain > (Matrix Constraints)
#   Parent   [□]
#   Aim      [□]
#   Manager  [□]
# Clic = exécute la dernière option ; □ = choix "Hello world"/"Bonjour France"

from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

PLUGIN_NAME = "atlasMatrixConstraint"
PLUGIN_VERSION = "1.2.0"
K_CMD = "atlasMatrixConstraint"    # commande exemple qui déclenche Parent

# --- définition des items ---
ITEMS = [("parent",  "Parent"),
         ("aim",     "Aim"),
         ("manager", "Manager")]

# Globals pour l'attache au menu Constrain
_ORIGINAL_PMC = None
_MENU_NAME = None


# ----------------- helpers -----------------

def _ids(key):
    """Fabrique les ids / optionVar / fenêtre pour un item."""
    return {
        "item":   f"atlasMC_{key}Item",
        "opt":    f"atlasMC_{key}Option",
        "win":    f"atlasMC_{key}OptionsWin",
        "ov":     f"atlasMC_{key}_lastChoice",  # 1: Hello world, 2: Bonjour France
    }

def _ensure_optionvar(key):
    ov = _ids(key)["ov"]
    if not cmds.optionVar(exists=ov):
        cmds.optionVar(iv=(ov, 1))

def _find_constrain_menu():
    """Trouve le menu top-level 'Constrain' (anglais/français)."""
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
    """Retourne l'item divider 'Matrix Constraints' si présent."""
    for it in (cmds.menu(menu_name, q=True, ia=True) or []):
        if cmds.menuItem(it, q=True, exists=True) and cmds.menuItem(it, q=True, divider=True):
            label = (cmds.menuItem(it, q=True, label=True) or "").strip().lower()
            if label == "matrix constraints":
                return it
    return None

def _delete_ui():
    """Supprime toutes nos entrées et fenêtres si présentes."""
    for key, _ in ITEMS:
        i = _ids(key)
        for mid in (i["item"], i["opt"]):
            if cmds.menuItem(mid, exists=True):
                cmds.deleteUI(mid)
        if cmds.window(i["win"], exists=True):
            cmds.deleteUI(i["win"])


# ----------------- actions -----------------

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


# ----------------- insertion menu -----------------

def _insert_items(menu_name):
    """Insère nos items, dans l'ordre, sous 'Matrix Constraints'."""
    _delete_ui()

    insert_after = _find_matrix_constraints_divider(menu_name)
    # Si le divider n'existe pas (menu différent), on insère en fin de menu
    if not insert_after:
        ia = cmds.menu(menu_name, q=True, ia=True) or []
        insert_after = ia[-1] if ia else None

    prev = insert_after
    for key, label in ITEMS:
        ids = _ids(key)
        _ensure_optionvar(key)

        kwargs = dict(parent=menu_name, label=label)
        if prev:
            kwargs["insertAfter"] = prev

        # Main item
        cmds.menuItem(
            ids["item"],
            **kwargs,
            c=(lambda k=key: _run_action(k))
        )

        # Option box
        cmds.menuItem(
            ids["opt"],
            parent=menu_name,
            optionBox=True,
            insertAfter=ids["item"],
            c=(lambda k=key, l=label: _show_options(k, l))
        )

        # Le prochain item s'insèrera après l'option box du précédent
        prev = ids["opt"]


def _pmc_wrapper(*_):
    """Chaîne le postMenuCommand original puis ajoute nos items."""
    try:
        orig = _ORIGINAL_PMC
        if isinstance(orig, str) and orig.strip():
            mel.eval(orig)
        elif callable(orig):
            orig()
    except Exception:
        pass
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        _insert_items(_MENU_NAME)

def _attach_to_constrain_menu():
    """Attache notre pmc au menu Constrain, sans écraser définitivement l'original."""
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
        # Exemple : la commande exécute l'action "Parent"
        _run_action("parent")

def _cmd_creator():
    return ompx.asMPxPtr(AtlasMatrixConstraintCmd())


# ----------------- plugin entry points -----------------

def initializePlugin(mobj):
    plugin = ompx.MFnPlugin(mobj, "atlas", PLUGIN_VERSION, "Any")
    plugin.registerCommand(K_CMD, _cmd_creator)
    cmds.evalDeferred(_attach_to_constrain_menu, lp=True)
    om.MGlobal.displayInfo("%s loaded" % PLUGIN_NAME)

def uninitializePlugin(mobj):
    # Nettoyage et restauration
    _delete_ui()
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        try:
            cmds.menu(_MENU_NAME, e=True, pmc=_ORIGINAL_PMC, postMenuCommandOnce=False)
        except Exception:
            pass
    plugin = ompx.MFnPlugin(mobj)
    plugin.deregisterCommand(K_CMD)
    om.MGlobal.displayInfo("%s unloaded" % PLUGIN_NAME)
