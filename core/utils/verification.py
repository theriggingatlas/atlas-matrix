"""

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
About: A utility function that allow verifying identity of object"

"""

from core.utils import nodes

def is_multmatrix(name: str)-> bool:
    """Check if the node is a multmatrix."""
    result = nodes.get_node_type(name)
    return result == "multMatrix"

def is_joint(name: str) -> bool:
    """Check if the node is a joint."""
    result = nodes.get_node_type(name)
    return result == "joint"

def is_inversematrix(name: str)-> bool:
    """Check if the node is an inversematrix."""
    result = nodes.get_node_type(name)
    return result == "inverseMatrix"

def is_composematrix(name: str)-> bool:
    """Check if the node is a composematrix."""
    result = nodes.get_node_type(name)
    return result == "composeMatrix"

def is_decomposematrix(name: str)-> bool:
    """Check if the node is a decomposematrix."""
    result = nodes.get_node_type(name)
    return result == "decomposeMatrix"

def is_holdmatrix(name: str)-> bool:
    """Check if the node is a holdmatrix."""
    result = nodes.get_node_type(name)
    return result == "holdMatrix"

def is_pickmatrix(name: str)-> bool:
    """Check if the node is a pickmatrix."""
    result = nodes.get_node_type(name)
    return result == "pickMatrix"