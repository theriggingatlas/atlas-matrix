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


from typing import Optional, List, Union, Tuple, Callable

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
        self.offset = False
        self.keep_hold = False
        self.envelope = False


    def _mount_offset(self, driver: str):
        """
        Mount the necessary setup for the offset system

        Args:
            driver (str): The name of the driver object
        """
        mult_tmp_node, mult_tmp_in, mult_tmp_out = self.con_mult_matrix(f"tmp_{driver}")

        self.connect_attr(self.get_world_matrix(self.driven), mult_tmp_in(0))
        self.connect_attr(self.get_inverse_world_matrix(driver), mult_tmp_in(1))

        return mult_tmp_node, mult_tmp_in, mult_tmp_out


    def create_offset(self, driver: str, mult_in: Callable[[int], str]):
        """
        Create the wanted offset type

        Args:
            driver (str): The name of the driver object name
            mult_in(str): The in attribute of the multMatrix with great index.
        """
        if self.offset:
            mult_tmp_node, mult_tmp_in, mult_tmp_out = self._mount_offset(driver)
            if self.keep_hold:
                hold_node, hold_in, hold_out = self.hold_matrix(driver)
                self.get_set_attr(mult_tmp_out, hold_in)
                self.connect_attr(hold_out, mult_in(0))
            else:
                self.get_set_attr(mult_tmp_out, mult_in(0))
        else:
            pass


    def create_blend(self, mult_list: List[str]) -> Tuple[str, str, str, str]:
        """
        Create a blendMatrix if needed

        Args:
            mult_list(List[str]): list of the mult to connect to the blendMatrix

        Returns:
            blend_node(str) : name of the blendMatrix node
            blend_input(str) : inputMatrix attribute of the blendMatrix node
            blend_in(str) : target[index].targetMatrix attribute of the blendMatrix node
            blend_out(str) : outputMatrix attribute of the blendMatrix node
        """
        blend_node, blend_input, blend_in, blend_out = self.con_blend_matrix()

        if self.envelope:
            self.get_set_attr(self.get_matrix(self.driven), blend_input)

        for index, mult in enumerate, mult_list:
            mult_out = mult[2]
            self.connect_attr(mult_out, blend_in[index])

        return blend_node, blend_input, blend_in, blend_out


    def create_compose(self):
        """
        Create a composeMatrix if needed
        """
        pass


    def _mount_system(self):
        """
        Internal setup to create the constraint chain and connect it.
        """
        parent_node = self.get_parent_driven()[0]
        parent_inverse = self.get_inverse_world_matrix(parent_node)

        mult_nodes = []

        for index, driver in enumerate(self.drivers):
            mult_node, mult_in, mult_out = self.con_mult_matrix(driver)
            self.connect_attr(self.get_world_matrix(driver), mult_in(1))
            self.connect_attr(parent_inverse, mult_in(2))

            self.create_offset(driver, mult_in)

            mult_nodes.append(mult_node)

        if len(self.drivers) > 1 or self.envelope:
            blend_node, blend_input, blend_in, blend_out = self.create_blend(mult_nodes)
            self.connect_attr(blend_out, self.get_offset_parent_matrix(self.driven))
        else:
            self.connect_attr(mult_nodes[0], self.get_offset_parent_matrix(self.driven))