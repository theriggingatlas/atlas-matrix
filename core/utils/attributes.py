# -*- coding: utf-8 -*-
""" Utilities functions that facilitates attributes manipulation inside Maya

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

# ---------- IMPORT ----------

from typing import List, Tuple, Optional, Any

import maya.cmds as cmds

from core.utils import verification

# ---------- FUNCTIONS ----------


def _split_attr(attr: str) -> List[str]:
    """
    Parse the full attribute path into node and attribute name.

    Args:
        attr (str): The attribute path in the form "node.attr".

    Returns:
        List[str, str]: A pair containing the node name and the attribute name.

    Raises:
        ValueError: If `attr` is not a string in the form "node.attr".
    """
    if verification.is_attribute_api(attr):
        raise ValueError(f"Invalid attributes detected: {attr}")

    return attr.rsplit('.', 1)


def _enum_signature(node: str, attr_name: str) -> Tuple[str, Optional[Tuple[str, ...]]]:
    """
    Build the enum type signature for a given attribute.

    Args:
        node (str): The node name hosting the attribute.
        attr_name (str): The enum attribute name on the node.

    Returns:
        Tuple[str, Optional[Tuple[str, ...]]]: A signature in the form
            ('enum', (<item1>, <item2>, ...)) if items are retrievable, otherwise
            ('enum', None).
    """
    try:
        enum_def = cmds.attributeQuery(attr_name, node=node, listEnum=True)

        if enum_def and isinstance(enum_def, list):
            return ('enum', tuple(enum_def[0].split(':')))

    except Exception:
        pass

    return ('enum', None)


def _type_string(full_attr: str) -> str:
    """Retrieve Maya's type string for an attribute.

    Args:
        full_attr (str): The attribute path in the form "node.attr".

    Returns:
        str: The Maya type string (e.g., "double", "double3", "string",
            "matrix", "message", "enum", "doubleAngle", "doubleLinear", "time").
    """
    return cmds.getAttr(full_attr, type=True)


def _attr_signature(full_attr: str) -> Tuple[Any, ...]:
    """
    Construct a stable, comparable signature of an attribute's data type.

    Args:
        full_attr (str): The attribute path in the form "node.attr".

    Returns:
        Tuple[Any, ...]: A hashable signature describing the attribute type and shape. Examples:
            - ('leaf', 'double')
            - ('leaf', 'string')
            - ('enum', (<item1>, <item2>, ...)) or ('enum', None)
            - ('compound', 'double3', (<child_sig1>, <child_sig2>, <child_sig3>))
            - ('array', <element_signature>)

    Raises:
        ValueError: If the attribute path is not in the form "node.attr".
        RuntimeError: If the attribute cannot be resolved or its type cannot be queried.
    """
    node, attr_name = _split_attr(full_attr)

    is_multi = False
    try:
        is_multi = bool(cmds.attributeQuery(attr_name, node=node, multi=True))
    except Exception:
        pass

    children = []
    try:
        children = cmds.attributeQuery(attr_name, node=node, listChildren=True) or []
    except Exception:
        pass

    try:
        base_t = _type_string(full_attr)
    except Exception:
        raise

    if base_t == 'enum':
        sig = _enum_signature(node, attr_name)
    elif children:
        child_sigs = []
        for ch in children:
            child_sigs.append(_attr_signature('{}.{}'.format(node, ch)))
        sig = ('compound', base_t, tuple(child_sigs))
    else:
        sig = ('leaf', base_t)

    if is_multi:
        sig = ('array', sig)

    return sig


