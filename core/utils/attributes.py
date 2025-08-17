"""

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
About: A utility function that facilitates attributes manipulation
        inside Maya

"""
from core.utils import verification

def get_world_matrix(obj):
    return f"{obj}.worldMatrix[0]"


def get_world_inverse_matrix(obj):
    return f"{obj}.worldInverseMatrix[0]"


def get_offset_parent_matrix(obj):
    return f"{obj}.offsetParentMatrix"


def get_in_matrix(obj):
    if verification.is_pickmatrix(obj) or verification.is_decomposematrix(obj) or verification.is_inversematrix(obj):
        return f"{obj}.inputMatrix"
    else:
        return f"{obj}.inMatrix"


def get_out_matrix(obj):
    if verification.is_pickmatrix(obj) or verification.is_composematrix(obj) or verification.is_inversematrix(obj):
        return f"{obj}.outputMatrix"
    elif verification.is_multmatrix(obj):
        return f"{obj}.matrixSum"
    else:
        return f"{obj}.outMatrix"