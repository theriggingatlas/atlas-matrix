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


from typing import Optional, List, Union, Tuple

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


    def _mount_offset(self, driver: str, mult_tmp: List[str]):
        """
        Mount the necessary setup for the offset system

        Args:
            driver (str): The name of the driver object
            mult_tmp(List[str]): list of the temporary multMatrix
        """
        mult_node, mult_in, mult_out = mult_tmp[0], mult_tmp[1], mult_tmp[2]

        self.connect_attr(self.get_world_matrix(self.driven), mult_in[0])
        self.connect_attr(self.get_inverse_world_matrix(driver), mult_in[1])


    def create_offset(self, driver: str, mult: List[str], mult_tmp: List[str]):
        """
        Create the wanted offset type

        Args:
            driver (str): The name of the driver object name
            mult(List[str]): If offset is wanted or not.
            mult_tmp(List[str]): If the offset need to keep the hold or not
        """
        mult_node, mult_in, mult_out = mult[0], mult[1], mult[2]
        mult_tmp_node, mult_tmp_in, mult_tmp_out = mult_tmp[0], mult_tmp[1], mult_tmp[2]

        if self.offset:
            self._mount_offset(driver, mult_tmp)
            if self.keep_hold:
                hold_node, hold_in, hold_out = self.hold_matrix(driver)
                self.get_set_attr(mult_tmp_out, hold_in)
                self.connect_attr(hold_out, mult_in[0])
            else:
                self.get_set_attr(mult_tmp_out, mult_in[0])
        else:
            pass


    def create_blend(self, mult_list: List[str]) -> Union[Tuple[str, str, str, str] | None]:
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


    def create_mult_matrix(self):
        """
        Create multMatrix for constraint
        """
        mult_list = []
        mult_tmp_list = []

        for driver in self.drivers:

            mult_node, mult_in, mult_out = self.mult_matrix(driver)
            driver_mult_list = [mult_node, mult_in, mult_out]
            mult_list.append(driver_mult_list)

            if self.offset:
                mult_tmp_node, mult_tmp_in, mult_tmp_out = self.mult_matrix(driver)
                driver_mult_tmp_list = [mult_tmp_node, mult_tmp_in, mult_tmp_out]
                mult_tmp_list.append(driver_mult_tmp_list)

        return mult_list, mult_tmp_list


    def _mount_system(self):
        """
        Internal setup to create the constraint chain and connect it.
        """
        mult_list, mult_tmp_list = self.create_mult_matrix()

        parent_node = self.get_parent_driven()[0]
        parent_inverse = self.get_inverse_world_matrix(parent_node)

        for mult in mult_list:

            mult_node, mult_in, mult_out = mult[0], mult[1], mult[2]

            for driver in self.drivers:
                self.connect_attr(self.get_world_matrix(driver), mult_in[1])
                self.connect_attr(parent_inverse, mult_in[2])

                if self.offset:
                    for mult_tmp in mult_tmp_list:
                        mult_tmp_node, mult_tmp_in, mult_tmp_out = mult_tmp[0], mult_tmp[1], mult_tmp[2]
                        self.create_offset(driver, mult_in, mult_tmp_out)

        if len(self.drivers) > 1 or self.envelope:
            blend_node, blend_input, blend_in, blend_out = self.create_blend(mult_list)
            self.connect_attr(blend_out, self.get_offset_parent_matrix(self.driven))
        else:
            self.connect_attr(mult_list[0][2], self.get_offset_parent_matrix(self.driven))