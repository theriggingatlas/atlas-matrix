"""

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
About: A utility function that allow verifying identity of object"

"""
import maya.api.OpenMaya as om
import maya.cmds as cmds
from core.utils import nodes


def is_multmatrix(name: str)-> bool:
    """Check if the node is a multMatrix."""
    result = nodes.get_node_type(name)
    return result == "multMatrix"


def is_addmatrix(name: str)-> bool:
    """Check if the node is a multMatrix."""
    result = nodes.get_node_type(name)
    return result == "addMatrix"


def is_wtaddmatrix(name: str)-> bool:
    """Check if the node is a multMatrix."""
    result = nodes.get_node_type(name)
    return result == "wtAddMatrix"


def is_holdmatrix(name: str)-> bool:
    """Check if the node is a holdMatrix."""
    result = nodes.get_node_type(name)
    return result == "multMatrix"


def is_joint(name: str) -> bool:
    """Check if the node is a joint."""
    result = nodes.get_node_type(name)
    return result == "joint"


def is_inversematrix(name: str)-> bool:
    """Check if the node is an inverseMatrix."""
    result = nodes.get_node_type(name)
    return result == "inverseMatrix"


def is_composematrix(name: str)-> bool:
    """Check if the node is a composeMatrix."""
    result = nodes.get_node_type(name)
    return result == "composeMatrix"


def is_decomposematrix(name: str)-> bool:
    """Check if the node is a decomposeMatrix."""
    result = nodes.get_node_type(name)
    return result == "decomposeMatrix"


def is_holdmatrix(name: str)-> bool:
    """Check if the node is a holdMatrix."""
    result = nodes.get_node_type(name)
    return result == "holdMatrix"


def is_pickmatrix(name: str)-> bool:
    """Check if the node is a pickMatrix."""
    result = nodes.get_node_type(name)
    return result == "pickMatrix"


def is_attribute(attr):
    """Return True if string points to a valid (built-in or custom) attribute."""
    if not isinstance(attr, str) or '.' not in attr:
        return False

    node, plug = attr.split('.', 1)

    # Check if node exists
    if not cmds.objExists(node):
        return False

    # Check if attribute exists (includes user-defined ones)
    return cmds.attributeQuery(plug, node=node, exists=True)


def is_attribute_api(attr):
    """Check if an attribute (built-in or custom) exists using OpenMaya API."""
    if not isinstance(attr, str) or '.' not in attr:
        return False
    try:
        sel = om.MSelectionList()
        sel.add(attr)
        plug = sel.getPlug(0)
        return plug.isValid
    except:
        return False