# -*- coding: utf-8 -*-
""" DEP class to use constraint parent matrix inside Maya

This module provides the `ParentCon` class, which allows precise matrix-based constraint
over objects using matrix nodes in Maya. It inherits from Matrix class.

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""


# ---------- IMPORT ----------


from typing import Optional, List, Union

from core.matrix import Matrix


# ---------- MAIN CLASS ----------


class ParentCon(Matrix):
    """"
    Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.

    Attributes:
        object_list (list): List of selected objects. Last is the constrained.
        translate_blend_matrix (float): Blend weight for translation.
        rotate_blend_matrix (float): Blend weight for rotation.
        scale_blend_matrix (float): Blend weight for scale.
        offset (bool): Whether to maintain offset between objects.
        hold (bool): Whether to keep initial offset in place using holdMatrix.
        pick_matrix (bool): Whether to use pickMatrix for filtering transformations.
        translate_all (bool): Enable translation filter on constraint.
        rotate_all (bool): Enable rotation filter on constraint.
        scale_all (bool): Enable scale filter on constraint.
        shear_all (bool): Enable shear filter on constraint.
    """
    def __init__(self, driven: Optional[str] = None, drivers: Optional[List[str]] = None):
        """
        Initialize the ParentCon constraint setup.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.
        """
        super().__init__(driven, drivers)
        self.constraint_type="parent"


    def create_offset(self, offset: bool):
        """
        Create the wanted offset type

        Args:
            offset (bool): If offset is wanted or not.
        """




