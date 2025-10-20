# -*- coding: utf-8 -*-
""" Utilities functions that facilitates transform manipulation inside Maya

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

# ---------- IMPORT ----------

import maya.cmds as cmds

from core.utils import verification


# ---------- FUNCTIONS ----------


def idtransform(obj: str)-> None:
    """Reset the transformations of a Maya object to the identity values.

    This function sets the following attributes to default values:
        - translate: (0, 0, 0)
        - rotate: (0, 0, 0)
        - scale: (1, 1, 1)
    If the object is a joint, it also resets:
        - jointOrient: (0, 0, 0)

    Args:
        obj (str): The name of the Maya object to reset.
    """
    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)

    if verification.is_joint(obj):
        cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)