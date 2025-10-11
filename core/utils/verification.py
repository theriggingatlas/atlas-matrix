""" Utilities functions that allow verifying identity of object

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

# ---------- IMPORT ----------

import maya.api.OpenMaya as om
import maya.cmds as cmds

from core.utils import nodes


# ---------- FUNCTIONS ----------


def is_multmatrix(name: str)-> bool:
    """Check if the given node is a multMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'multMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "multMatrix"


def is_addmatrix(name: str)-> bool:
    """Check if the given node is an addMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'addMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "addMatrix"


def is_wtaddmatrix(name: str)-> bool:
    """Check if the given node is a wtAddMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'wtAddMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "wtAddMatrix"


def is_holdmatrix(name: str)-> bool:
    """Check if the given node is a holdMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'holdMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "multMatrix"


def is_joint(name: str) -> bool:
    """Check if the given node is a joint node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'joint', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "joint"


def is_inversematrix(name: str)-> bool:
    """Check if the given node is an inverseMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'inverseMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "inverseMatrix"


def is_composematrix(name: str)-> bool:
    """Check if the given node is a composeMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'composeMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "composeMatrix"


def is_decomposematrix(name: str)-> bool:
    """Check if the given node is a decomposeMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'decomposeMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "decomposeMatrix"


def is_holdmatrix(name: str)-> bool:
    """Check if the given node is a holdMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'holdMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "holdMatrix"


def is_pickmatrix(name: str)-> bool:
    """Check if the given node is a pickMatrix node.

    Args:
        name (str): The name of the node.

    Returns:
        bool: True if the node is of type 'pickMatrix', False otherwise.
    """
    result = nodes.get_node_type(name)
    return result == "pickMatrix"


def is_attribute(attr):
    """Check if a string points to a valid attribute on a Maya node.

    Args:
        attr (str): Attribute string in the form 'nodeName.attributeName'.

    Returns:
        bool: True if the attribute exists, False otherwise.
    """
    if not isinstance(attr, str) or '.' not in attr:
        return False

    node, plug = attr.split('.', 1)

    # Check if node exists
    if not cmds.objExists(node):
        return False

    # Check if attribute exists (includes user-defined ones)
    return cmds.attributeQuery(plug, node=node, exists=True)


def is_attribute_api(attr):
    """Check if a string points to a valid attribute using the OpenMaya API.

    Args:
        attr (str): Attribute string in the form 'nodeName.attributeName'.

    Returns:
        bool: True if the attribute exists and is valid, False otherwise.
    """
    if not isinstance(attr, str) or '.' not in attr:
        return False
    try:
        sel = om.MSelectionList()
        sel.add(attr)
        plug = sel.getPlug(0)
        return plug.isValid
    except:
        return False