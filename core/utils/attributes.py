""" Utilities functions that facilitates attributes manipulation inside Maya

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""

# ---------- IMPORT ----------

from core.utils import verification


# ---------- FUNCTIONS ----------


def get_world_matrix(obj: str)-> str:
    return f"{obj}.worldMatrix[0]"


def get_world_inverse_matrix(obj: str)-> str:
    return f"{obj}.worldInverseMatrix[0]"


def get_offset_parent_matrix(obj: str)-> str:
    return f"{obj}.offsetParentMatrix"