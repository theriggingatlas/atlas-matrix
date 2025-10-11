""" Utilities functions that facilitates node manipulation inside Maya

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

# ---------- IMPORT ----------

import maya.cmds as cmds
import maya.api.OpenMaya as om


# ---------- FUNCTIONS ----------


def get_node_type(name:str)-> str:
    """Return the type of Maya node given its name.

    This function uses the OpenMaya API to query the dependency node
    corresponding to the provided name and retrieves its type.

    Args:
        name (str): The name of the Maya node.

    Returns:
        str: The type of the node (e.g., "transform", "joint", "multMatrix").

    Raises:
        RuntimeError: If the node does not exist in the scene.
    """
    selection_list = om.MSelectionList()
    selection_list.add(name)
    node_obj = selection_list.getDependNode(0)

    dependency_node = om.MFnDependencyNode(node_obj)

    node_type = dependency_node.typeName
    return node_type