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
        node_multmatrix = "tmp_multmatrix"

        out_multmatrix = self.matrix_node.mult_matrix([attributes.get_world_matrix(constrained), attributes.get_world_inverse_matrix(constrainer)], name=node_multmatrix)
        self.matrix_node.hold_matrix(input=node_multmatrix, name=name_hold_matrix)

        self.disconnect_input(attributes.get_in_matrix(name_hold_matrix))
        cmds.delete(node_multmatrix)
        return f"{name_hold_matrix}.outMatrix"