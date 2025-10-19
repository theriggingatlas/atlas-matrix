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
        """Initialize the ParentCon constraint setup.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.
        """
        super().__init__(driven, drivers)
        self.constraint_type="parent"


    def con_hold_matrix(self, driver: str) -> str:
        """
        Create a hold matrix node to maintain offset between objects.

        Returns:
            str: Hold matrix name.
        """
        node_hold = self.mult_matrix(driver)

        in_hold = self.get_in_matrix(node_hold)
        out_hold = self.get_out_matrix(node_hold)

        return node_hold, in_hold, out_hold


    def con_mult_matrix(self, driver: str) -> str:
        """
        Create a mult matrix node to constrain object.

        Returns:
            str: mult matrix name.
        """
        node_mult = self.mult_matrix(driver)

        in_mult = self.get_in_matrix(node_mult)
        out_mult = self.get_out_matrix(node_mult)

        return node_mult, in_mult, out_mult


    def con_blend_matrix(self):
        """
        Create a blend matrix node to blend constrained objects.

        Returns:
            str: blend matrix name.
        """
        node_blend = self.blend_matrix()

        in_blend = self.get_in_matrix(node_blend)
        out_blend = self.get_out_matrix(node_blend)

        return node_blend, in_blend, out_blend