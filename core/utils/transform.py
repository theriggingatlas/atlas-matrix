import maya.cmds as cmds
from core.utils import verification


def idtransform(obj):

    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)

    if verification.is_joint(obj):
        cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)