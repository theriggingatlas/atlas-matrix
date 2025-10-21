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
        self.offset = ""
        self.keep_hold = ""


    def create_offset(self, driver: str, mult_in: List[str], mult_tmp_out: str):
        """
        Create the wanted offset type

        Args:
            driver (str): The name of the driver object name
            mult_in List[str]: If offset is wanted or not.
            mult_tmp_out (str): If the offset need to keep the hold or not
        """
        if self.offset:
            if self.keep_hold:
                hold_node, hold_in, hold_out = self.hold_matrix(driver)
                self.get_set_attr(mult_tmp_out, hold_in)
                self.connect_attr(hold_out, mult_in[0])
            else:
                self.get_set_attr(mult_tmp_out, mult_in[0])
        else:
            pass


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

                self.connect_attr(mult_out, self.get_offset_parent_matrix(self.driven))

                if self.offset:
                    for mult_tmp in mult_tmp_list:
                        mult_tmp_node, mult_tmp_in, mult_tmp_out = mult_tmp[0], mult_tmp[1], mult_tmp[2]
                        self.create_offset(driver, mult_in, mult_tmp_out)


