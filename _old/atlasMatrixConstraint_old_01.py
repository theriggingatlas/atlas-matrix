# -*- coding: utf-8 -*-
# Plugin: atlasMatrixConstraint
# Ajoute "Parent" sous "Matrix Constraints" dans Constrain.
# Clic direct = exécute la dernière option choisie.
# Option box = choix entre "Hello world" et "Bonjour France".

from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

PLUGIN_NAME = "atlasMatrixConstraint"
PLUGIN_VERSION = "1.1.0"
K_CMD = "atlasMatrixConstraint"

MENU_ITEM_ID = "atlasMC_parentItem"
OPTION_ITEM_ID = "atlasMC_parentItemOption"
OPTION_WIN = "atlasMC_optionsWin"
OPTION_VAR = "atlasMC_lastChoice"  # 1: Hello world, 2: Bonjour France

_ORIGINAL_PMC = None        # postMenuCommand d'origine du menu Constrain
_MENU_NAME = None           # nom du menu Constrain


# ----------------- helpers -----------------

def _ensure_optionvar():
    if not cmds.optionVar(exists=OPTION_VAR):
        cmds.optionVar(iv=(OPTION_VAR, 1))

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
    if cmds.menuItem(MENU_ITEM_ID, exists=True):
        cmds.deleteUI(MENU_ITEM_ID)
    if cmds.menuItem(OPTION_ITEM_ID, exists=True):
        cmds.deleteUI(OPTION_ITEM_ID)
    if cmds.window(OPTION_WIN, exists=True):
        cmds.deleteUI(OPTION_WIN)

# ----------------- actions -----------------

def run_last_option(*_):
    _ensure_optionvar()
    val = int(cmds.optionVar(q=OPTION_VAR))
    if val == 2:
        om.MGlobal.displayInfo("Bonjour France")
        print("Bonjour France")
    else:
        om.MGlobal.displayInfo("Hello world")
        print("Hello world")

def show_options(*_):
    _ensure_optionvar()
    if cmds.window(OPTION_WIN, exists=True):
        cmds.deleteUI(OPTION_WIN)
    win = cmds.window(OPTION_WIN, title="atlasMatrixConstraint Options", sizeable=False)
    cmds.columnLayout(adj=True, rs=8, cw=260)
    rb = cmds.radioButtonGrp(
        numberOfRadioButtons=2,
        label="Action :",
        labelArray2=["Hello world", "Bonjour France"],
        sl=int(cmds.optionVar(q=OPTION_VAR))
    )
    def _apply(*__):
        cmds.optionVar(iv=(OPTION_VAR, cmds.radioButtonGrp(rb, q=True, sl=True)))
    cmds.button(label="Apply and Close", c=lambda *_: (_apply(), cmds.deleteUI(win)))
    cmds.button(label="Apply", c=_apply)
    cmds.button(label="Close", c=lambda *_: cmds.deleteUI(win))
    cmds.showWindow(win)

# ----------------- insertion menu -----------------

def _insert_items(menu_name):
    """Insère/replace notre item après le divider 'Matrix Constraints'."""
    _delete_ui()
    _ensure_optionvar()

    insert_after = _find_matrix_constraints_divider(menu_name)
    kwargs = dict(parent=menu_name, label="Parent")
    if insert_after:
        kwargs["insertAfter"] = insert_after

    # callbacks Python directs (pas d'import dynamique)
    cmds.menuItem(MENU_ITEM_ID, **kwargs, c=lambda *_: run_last_option())
    cmds.menuItem(
        OPTION_ITEM_ID,
        parent=menu_name,
        optionBox=True,
        insertAfter=MENU_ITEM_ID,
        c=lambda *_: show_options()
    )

def _pmc_wrapper(*_):
    """postMenuCommand : appelle d'abord le builder original, puis insère notre item."""
    try:
        if isinstance(_ORIGINAL_PMC, str) and _ORIGINAL_PMC.strip():
            mel.eval(_ORIGINAL_PMC)
        elif callable(_ORIGINAL_PMC):
            _ORIGINAL_PMC()
    except Exception:
        # On ne bloque jamais la construction du menu par défaut
        pass
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        _insert_items(_MENU_NAME)

def _attach_to_constrain_menu():
    """Attache notre pmc au menu Constrain, sans écraser définitivement l'original."""
    global _ORIGINAL_PMC, _MENU_NAME
    _MENU_NAME = _find_constrain_menu()
    if not _MENU_NAME:
        # Retente plus tard tant que l'UI n'est pas prête
        cmds.evalDeferred(_attach_to_constrain_menu, lp=True)
        return

    # Sauvegarde et chaîne le pmc d'origine
    try:
        _ORIGINAL_PMC = cmds.menu(_MENU_NAME, q=True, pmc=True)
    except Exception:
        _ORIGINAL_PMC = None

    cmds.menu(_MENU_NAME, e=True, postMenuCommandOnce=False, pmc=_pmc_wrapper)

# ----------------- MPx command -----------------

class AtlasMatrixConstraintCmd(ompx.MPxCommand):
    def doIt(self, args):
        run_last_option()

def _cmd_creator():
    return ompx.asMPxPtr(AtlasMatrixConstraintCmd())

# ----------------- plugin entry points -----------------

def initializePlugin(mobj):
    plugin = ompx.MFnPlugin(mobj, "atlas", PLUGIN_VERSION, "Any")
    plugin.registerCommand(K_CMD, _cmd_creator)
    cmds.evalDeferred(_attach_to_constrain_menu, lp=True)
    om.MGlobal.displayInfo("%s loaded" % PLUGIN_NAME)

def uninitializePlugin(mobj):
    # Nettoyage UI
    _delete_ui()
    # Restaure le pmc original si possible
    if _MENU_NAME and cmds.menu(_MENU_NAME, exists=True):
        try:
            cmds.menu(_MENU_NAME, e=True, pmc=_ORIGINAL_PMC, postMenuCommandOnce=False)
        except Exception:
            pass
    plugin = ompx.MFnPlugin(mobj)
    plugin.deregisterCommand(K_CMD)
    om.MGlobal.displayInfo("%s unloaded" % PLUGIN_NAME)